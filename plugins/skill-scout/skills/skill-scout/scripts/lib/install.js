// Installs one approved skill folder from GitHub at the exact commit that was inspected.
// Never overwrites, skips symlinks and submodules, and writes only inside the target folder.
const fs = require('node:fs');
const path = require('node:path');

const MAX_FILES = 300;
const MAX_TOTAL_BYTES = 20 * 1024 * 1024;

function resolveTarget(root, repo, dirPath) {
  const name = path.posix.basename(dirPath) || repo.split('/')[1];
  if (!/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(name)) throw new Error(`unsafe skill folder name "${name}"`);
  return path.join(root, name);
}

function resolveFilePath(target, relative) {
  const file = path.resolve(target, ...relative.split('/'));
  if (!file.startsWith(target + path.sep)) throw new Error(`refusing path outside the skill folder: ${relative}`);
  return file;
}

async function mapWithLimit(items, limit, fn) {
  const results = new Array(items.length);
  let next = 0;
  const workers = Array.from({ length: Math.min(limit, items.length) }, async () => {
    while (next < items.length) {
      const i = next++;
      results[i] = await fn(items[i]);
    }
  });
  await Promise.all(workers);
  return results;
}

async function installSkill(client, repo, { dirPath = '', sha, root }) {
  if (!/^[0-9a-f]{40}$/.test(sha || '')) throw new Error('--sha must be the full 40-character commit printed by `inspect`');
  const dir = dirPath.replace(/^\/+|\/+$/g, '');
  const target = path.resolve(resolveTarget(root, repo, dir));
  if (fs.existsSync(target)) throw new Error(`${target} already exists; not overwriting. Remove it first or install elsewhere.`);

  const tree = await client.getGithub(`repos/${repo}/git/trees/${sha}?recursive=1`);
  if (tree.truncated) throw new Error('repository tree too large for GitHub to list in one response');
  const prefix = dir ? `${dir}/` : '';
  const entries = tree.tree.filter((entry) => entry.path.startsWith(prefix) && entry.type !== 'tree');
  const blobs = entries.filter((entry) => entry.type === 'blob' && entry.mode !== '120000');
  const skipped = entries.filter((entry) => !blobs.includes(entry)).map((entry) => entry.path.slice(prefix.length));
  if (!blobs.some((blob) => blob.path === `${prefix}SKILL.md`)) throw new Error(`no SKILL.md at ${repo}/${dir} @ ${sha}`);
  if (blobs.length > MAX_FILES) throw new Error(`${blobs.length} files exceeds the ${MAX_FILES}-file limit`);
  const totalBytes = blobs.reduce((sum, blob) => sum + (blob.size || 0), 0);
  if (totalBytes > MAX_TOTAL_BYTES) throw new Error(`${(totalBytes / 1048576).toFixed(1)} MB exceeds the 20 MB limit`);

  const contents = await mapWithLimit(blobs, 8, (blob) =>
    client.getBuffer(`https://raw.githubusercontent.com/${repo}/${sha}/${blob.path.split('/').map(encodeURIComponent).join('/')}`),
  );

  const hasRoot = fs.existsSync(root);
  const staging = `${target}.partial-${process.pid}`;
  try {
    blobs.forEach((blob, i) => {
      const file = resolveFilePath(staging, blob.path.slice(prefix.length));
      fs.mkdirSync(path.dirname(file), { recursive: true });
      fs.writeFileSync(file, contents[i]);
      if (blob.mode === '100755' && process.platform !== 'win32') fs.chmodSync(file, 0o755);
    });
    const provenance = { repo, path: dir, sha, installedAt: new Date().toISOString(), installedBy: 'skill-scout' };
    fs.writeFileSync(path.join(staging, '.skill-scout.json'), `${JSON.stringify(provenance, null, 2)}\n`);
    fs.renameSync(staging, target);
  } catch (err) {
    fs.rmSync(staging, { recursive: true, force: true });
    throw err;
  }
  return { target, count: blobs.length, skipped, hasRoot };
}

module.exports = { installSkill };
