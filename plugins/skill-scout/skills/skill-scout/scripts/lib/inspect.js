// Security inspection of one GitHub-hosted skill: pins the commit, lists its files, and
// pattern-scans them. The rating is a floor for Claude's own reading, not a verdict.
const path = require('node:path');
const { computeScore } = require('./match');

const MAX_SCANNED_FILES = 25;
const MAX_SCANNED_BYTES = 300 * 1024;
const EXECUTABLE = /\.(exe|dll|so|dylib|bin|jar|class|pyc|wasm|msi|deb|rpm|appimage|scr)$/i;
const MEDIA = /\.(png|jpe?g|gif|webp|ico|svg|pdf|ttf|otf|woff2?|mp3|mp4|mov|wav)$/i;
const ARCHIVE = /\.(zip|tar|gz|tgz|bz2|xz|7z|rar)$/i;
const SCRIPT = /\.(sh|bash|zsh|fish|ps1|psm1|bat|cmd|py|js|mjs|cjs|ts|rb|pl|php|go|rs|lua)$/i;

// `scope` is where a rule applies: scripts, docs (Markdown and other text), or both.
const RULES = [
  { level: 'high', label: 'download and execute', scope: 'all', pattern: /\b(curl|wget)\b[^\n]*\|\s*(sudo\s+)?(ba|z|da)?sh\b|\bInvoke-Expression\b|\biex\b/i },
  { level: 'high', label: 'reads credential stores', scope: 'all', pattern: /\.ssh\/|id_rsa|id_ed25519|\.aws\/credentials|\.netrc|\.git-credentials|\.docker\/config\.json|\.kube\/config|find-generic-password|\bkeychain\b|\.npmrc|\.pypirc/i },
  { level: 'high', label: 'bypasses agent permissions', scope: 'all', pattern: /dangerously-skip-permissions|bypassPermissions|--no-verify|disable[- ]?(the )?(sandbox|permissions)/i },
  { level: 'high', label: 'obfuscated payload', scope: 'all', pattern: /base64\s+(-d|--decode)|\batob\(|FromBase64String|b64decode|Buffer\.from\([^)]*['"]base64['"]|(\\x[0-9a-f]{2}){8,}/i },
  { level: 'high', label: 'destructive delete', scope: 'all', pattern: /\brm\s+-[a-z]*r[a-z]*\s+(\/|~|\$HOME|%USERPROFILE%)(\s|$)|Remove-Item[^\n]*-Recurse[^\n]*(C:\\|\$HOME|~)/i },
  { level: 'high', label: 'elevated privileges', scope: 'script', pattern: /\bsudo\b|\bdoas\b|\brunas\b|Set-ExecutionPolicy\s+(Bypass|Unrestricted)|chmod\s+(-R\s+)?777/i },
  { level: 'high', label: 'instructions hidden from the user', scope: 'doc', pattern: /ignore (all |any )?(previous|prior|above) instructions|do not (tell|inform|show) the user|without (asking|telling|informing) the user|don'?t mention (this|it) to the user/i },
  { level: 'high', label: 'invisible unicode', scope: 'doc', pattern: /[\u200B-\u200F\u202A-\u202E\u2066-\u2069]/ },
  { level: 'medium', label: 'elevated privileges', scope: 'doc', pattern: /\bsudo\b|\brunas\b|Set-ExecutionPolicy/i },
  { level: 'medium', label: 'network call', scope: 'script', pattern: /\b(curl|wget|axios|urllib|httpx|aiohttp|XMLHttpRequest|WebSocket|Invoke-WebRequest|Invoke-RestMethod)\b|\bfetch\(|\brequests\.(get|post|put|patch|delete)\(|http\.client|net\/http|Net\.WebClient|https?:\/\//i },
  { level: 'medium', label: 'network call', scope: 'doc', pattern: /\b(curl|wget)\s|Invoke-WebRequest|Invoke-RestMethod/i },
  { level: 'medium', label: 'reads env vars or secrets', scope: 'script', pattern: /process\.env|os\.environ|os\.getenv|getenv\(|\$env:|ENV\[|\$\{?[A-Z_]*(TOKEN|SECRET|API_KEY|PASSWORD|CREDENTIAL)[A-Z_]*\}?/ },
  { level: 'medium', label: 'asks for secrets', scope: 'doc', pattern: /\b[A-Z][A-Z0-9_]*(API_KEY|TOKEN|SECRET|PASSWORD)\b/ },
  { level: 'medium', label: 'runs shell commands', scope: 'script', pattern: /child_process|\bexecSync\b|\bspawn(Sync)?\(|\bsubprocess\b|os\.system|os\.popen|shell\s*=\s*True|Start-Process|\beval\(|\bexec\(/ },
  { level: 'medium', label: 'downloads further code', scope: 'all', pattern: /\b(npm|pnpm|yarn|bun)\s+(i|install|add)\b|\bpip3?\s+install\b|\buv\s+(pip\s+install|add|tool\s+install)\b|\bnpx\s|\buvx\s|\bgo\s+install\b|\bcargo\s+install\b|\bbrew\s+install\b|\bgem\s+install\b|\bgit\s+clone\b|\bapt(-get)?\s+install\b|\bwinget\s+install\b|\bchoco\s+install\b/i },
  { level: 'medium', label: 'touches agent or shell config', scope: 'all', pattern: /settings(\.local)?\.json|\.claude\/(hooks|agents|commands)|\bCLAUDE\.md\b|\.bashrc|\.zshrc|\.profile\b|crontab|launchctl|systemctl|schtasks|HKCU:|HKLM:/i },
  { level: 'medium', label: 'hidden HTML comment', scope: 'doc', pattern: /<!--/ },
];

function resolveSkillDir(blobs, skill, dirPath) {
  const skillFiles = blobs.filter((b) => b.path === 'SKILL.md' || b.path.endsWith('/SKILL.md')).map((b) => b.path);
  const dirs = skillFiles.map((file) => (file === 'SKILL.md' ? '' : path.posix.dirname(file)));
  const wanted = dirPath !== undefined ? dirs.filter((dir) => dir === dirPath.replace(/^\/+|\/+$/g, '')) : dirs;
  const named = skill ? wanted.filter((dir) => path.posix.basename(dir) === skill) : wanted;
  const matches = named.length ? named : wanted;
  if (matches.length === 1) return matches[0];
  const nameParts = (skill || '').toLowerCase().split(/[-_\s]+/).filter(Boolean);
  const listing = [...dirs]
    .sort((a, b) => computeScore(nameParts, b) - computeScore(nameParts, a))
    .slice(0, 15)
    .map((dir) => `  --path "${dir}"`)
    .join('\n');
  if (!dirs.length) throw new Error('no SKILL.md anywhere in this repository');
  const reason = !matches.length
    ? `no SKILL.md at "${dirPath}"`
    : skill && !named.length
      ? `no folder named "${skill}" (skills.sh names can differ from folder names)`
      : `${matches.length} skills match`;
  throw new Error(`${reason}; rerun with one of these ${dirs.length} skill folders, closest first:\n${listing || '  (none)'}`);
}

function computeFindings(file, text) {
  const isScript = SCRIPT.test(file) || text.startsWith('#!');
  const findings = [];
  for (const rule of RULES) {
    if (rule.scope !== 'all' && (rule.scope === 'script') !== isScript) continue;
    const hits = text.split('\n').flatMap((line, i) => {
      const match = rule.pattern.exec(line);
      return match ? [{ line: i + 1, excerpt: line.slice(Math.max(0, match.index - 30), match.index + 70).trim() }] : [];
    });
    findings.push(...hits.slice(0, 3).map((hit) => ({ level: rule.level, label: rule.label, file, ...hit })));
  }
  return findings;
}

// Pre-approving bare `Bash` or `Bash(*)` lets the skill run any command without a prompt.
function computeFrontmatterFindings(skillMd) {
  const frontmatter = /^\uFEFF?---\r?\n([\s\S]*?)\r?\n---/.exec(skillMd)?.[1] || '';
  const tools = /allowed-tools:([\s\S]*?)(\n\S|$)/.exec(frontmatter)?.[1] || '';
  return /\bBash\b(?!\()|Bash\(\s*\*\s*\)/.test(tools)
    ? [{ level: 'medium', label: 'pre-approves unrestricted Bash', file: 'SKILL.md', line: 1, excerpt: tools.trim().slice(0, 100) }]
    : [];
}

function computeRating(findings) {
  if (findings.some((f) => f.level === 'high')) return 'Risky';
  return findings.length ? 'Review needed' : 'Clean';
}

function encodePath(file) {
  return file.split('/').map(encodeURIComponent).join('/');
}

async function inspectSkill(client, repo, { skill, dirPath }) {
  const meta = await client.getGithub(`repos/${repo}`);
  const branch = encodeURIComponent(meta.default_branch);
  const tree = await client.getGithub(`repos/${repo}/git/trees/${branch}?recursive=1`);
  const blobs = tree.tree.filter((entry) => entry.type === 'blob');
  const dir = resolveSkillDir(blobs, skill, dirPath);
  const [commit] = await client.getGithub(`repos/${repo}/commits?sha=${branch}&path=${encodeURIComponent(dir)}&per_page=1`);
  const prefix = dir ? `${dir}/` : '';
  const files = tree.tree
    .filter((entry) => entry.path.startsWith(prefix) && entry.type !== 'tree')
    .map((entry) => ({ path: entry.path.slice(prefix.length), size: entry.size || 0, mode: entry.mode, type: entry.type }));

  const findings = [];
  const notes = tree.truncated ? ['repository tree truncated by GitHub; file list may be incomplete'] : [];
  for (const file of files) {
    if (file.type === 'commit') findings.push({ level: 'medium', label: 'git submodule (not reviewed)', file: file.path, line: 0, excerpt: '' });
    if (file.mode === '120000') findings.push({ level: 'medium', label: 'symlink (skipped on install)', file: file.path, line: 0, excerpt: '' });
    if (EXECUTABLE.test(file.path)) findings.push({ level: 'high', label: 'opaque binary', file: file.path, line: 0, excerpt: '' });
    if (ARCHIVE.test(file.path)) findings.push({ level: 'medium', label: 'archive (contents not reviewed)', file: file.path, line: 0, excerpt: '' });
  }
  const scannable = files.filter((f) => f.type === 'blob' && f.mode !== '120000' && !EXECUTABLE.test(f.path) && !MEDIA.test(f.path) && !ARCHIVE.test(f.path));
  const scanned = scannable.filter((f) => f.size <= MAX_SCANNED_BYTES).slice(0, MAX_SCANNED_FILES);
  if (scanned.length < scannable.length) {
    notes.push(`${scannable.length - scanned.length} text files not scanned (size or count limit); read them before installing`);
  }
  const texts = await Promise.all(
    scanned.map((f) => client.getText(`https://raw.githubusercontent.com/${repo}/${commit.sha}/${encodePath(prefix + f.path)}`)),
  );
  scanned.forEach((f, i) => findings.push(...computeFindings(f.path, texts[i])));
  const skillMd = texts[scanned.findIndex((f) => f.path === 'SKILL.md')] || '';
  findings.push(...computeFrontmatterFindings(skillMd));

  return {
    repo,
    dir,
    sha: commit.sha,
    updated: commit.commit.committer.date.slice(0, 10),
    stars: meta.stargazers_count,
    isArchived: meta.archived,
    license: meta.license?.spdx_id || 'none',
    files,
    skillMd,
    findings,
    notes,
    rating: computeRating(findings),
  };
}

module.exports = { inspectSkill };
