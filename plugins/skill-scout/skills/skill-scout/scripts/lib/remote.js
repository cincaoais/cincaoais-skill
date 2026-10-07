// External sources: the skills.sh directory, GitHub search, and curated collections.
// Each lister returns { results, notes } or throws; scout.js reports a throw as a skipped source.
const path = require('node:path');
const { runFile } = require('./http');
const { computeScore } = require('./match');

// Curated collections searched on every run. `tree` lists a repo's SKILL.md folders;
// `list` scans an awesome-list README for GitHub links.
const COLLECTIONS = [
  { repo: 'anthropics/skills', kind: 'tree' },
  { repo: 'ComposioHQ/awesome-claude-skills', kind: 'list' },
  { repo: 'VoltAgent/awesome-agent-skills', kind: 'list' },
];

function buildQueries(keywords) {
  return [...new Set([keywords.join(' '), keywords.slice(0, 2).join(' ')])];
}

function parseInstalls(text) {
  const [, value, unit] = /^([\d.]+)([KM]?)$/.exec(text) || [];
  return value ? Math.round(Number(value) * ({ K: 1e3, M: 1e6 }[unit] || 1)) : undefined;
}

function buildSkillsShCandidate(repo, skill, installs) {
  return { source: 'skills.sh', repo, skill, installs, url: `https://skills.sh/${repo}/${skill}` };
}

// Uses the `skills` CLI only if it is already cached locally; never downloads it.
async function listSkillsCliMatches(query) {
  const npx = process.platform === 'win32' ? 'npx.cmd' : 'npx';
  const output = await runFile(npx, ['--no-install', 'skills', 'find', query], { timeout: 20000 });
  return output
    .replace(/\x1b\[[0-9;]*m/g, '')
    .split('\n')
    .map((line) => /^(\S+\/\S+?)@(\S+)\s+([\d.]+[KM]?) installs/.exec(line.trim()))
    .filter(Boolean)
    .map(([, repo, skill, installs]) => buildSkillsShCandidate(repo, skill, parseInstalls(installs)));
}

async function listSkillsShMatches(client, keywords) {
  const queries = buildQueries(keywords);
  try {
    const pages = await Promise.all(
      queries.map((q) => client.getJson(`https://skills.sh/api/search?q=${encodeURIComponent(q)}&limit=10`)),
    );
    const results = pages.flatMap((page) =>
      (page.skills || []).map((s) => buildSkillsShCandidate(s.source, s.skillId || s.name, s.installs)),
    );
    return { results, notes: [] };
  } catch (err) {
    const fallback = await listSkillsCliMatches(queries[0]).catch(() => undefined);
    if (!fallback) throw new Error(`${err.message}; \`npx skills\` is not cached locally either`);
    return { results: fallback, notes: [`skills.sh API failed (${err.message}); used the local \`npx skills\` CLI`] };
  }
}

function quoteTerm(keyword) {
  return keyword.includes(' ') ? `"${keyword}"` : keyword;
}

async function listGithubMatches(client, keywords) {
  const terms = keywords.slice(0, 2).map(quoteTerm);
  try {
    const pages = await Promise.all(
      terms.map((term) =>
        client.getGithub(`search/code?q=${encodeURIComponent(`${term} filename:SKILL.md`)}&per_page=10`, {
          requiresAuth: true,
        }),
      ),
    );
    const results = pages.flatMap((page) =>
      page.items.map((item) => {
        const dir = path.posix.dirname(item.path);
        return {
          source: 'github',
          repo: item.repository.full_name,
          path: dir === '.' ? '' : dir,
          skill: dir === '.' ? item.repository.name : path.posix.basename(dir),
          description: item.repository.description || '',
          url: item.html_url,
        };
      }),
    );
    return { results, notes: [] };
  } catch (err) {
    if (!err.needsAuth) throw err;
  }
  const pages = await Promise.all(
    terms.map((term) =>
      client.getGithub(`search/repositories?q=${encodeURIComponent(`${term} skill in:name,description,readme`)}&per_page=10`),
    ),
  );
  const results = pages.flatMap((page) =>
    page.items.map((repo) => ({
      source: 'github',
      repo: repo.full_name,
      stars: repo.stargazers_count,
      updated: repo.pushed_at?.slice(0, 10),
      description: repo.description || '',
      url: repo.html_url,
    })),
  );
  return { results, notes: ['GitHub code search needs `gh auth login`; searched repositories instead'] };
}

// Matches `[label](https://github.com/owner/repo/tree/<ref>/<path>)` and the rest of the line.
const LINK_PATTERN = /\[([^\]]+)\]\(https:\/\/github\.com\/([\w.-]+\/[\w.-]+)(?:\/tree\/[^/)]+\/([^)#?]+))?\/?\)(.*)$/;

async function listCollection(client, { repo, kind }) {
  if (kind === 'tree') {
    const tree = await client.getGithub(`repos/${repo}/git/trees/HEAD?recursive=1`);
    return tree.tree
      .filter((entry) => entry.path.endsWith('/SKILL.md'))
      .map((entry) => path.posix.dirname(entry.path))
      .map((dir) => ({ source: 'collection', repo, path: dir, skill: path.posix.basename(dir), description: '' }));
  }
  const readme = await client.getText(`https://raw.githubusercontent.com/${repo}/HEAD/README.md`);
  return readme
    .split('\n')
    .map((line) => LINK_PATTERN.exec(line))
    .filter(Boolean)
    .map(([, label, linked, dir, rest]) => ({
      source: 'collection',
      via: repo,
      repo: linked,
      path: dir ? decodeURIComponent(dir) : undefined,
      skill: label.replace(/[*`]/g, '').split('/').pop(),
      description: rest.replace(/[*_`]|\[([^\]]*)\]\([^)]*\)/g, '$1').replace(/^[\s:–—-]+/, '').slice(0, 160),
    }));
}

async function listCollectionMatches(client, keywords) {
  const settled = await Promise.allSettled(COLLECTIONS.map((collection) => listCollection(client, collection)));
  const failed = settled.flatMap((s, i) => (s.status === 'rejected' ? [`${COLLECTIONS[i].repo}: ${s.reason.message}`] : []));
  if (failed.length === COLLECTIONS.length) throw new Error(failed.join('; '));
  const results = settled
    .flatMap((s) => (s.status === 'fulfilled' ? s.value : []))
    .map((candidate) => ({
      ...candidate,
      score: computeScore(keywords, `${candidate.skill} ${candidate.path || ''} ${candidate.description}`),
    }))
    .filter((candidate) => candidate.score > 0);
  return { results, notes: failed.map((failure) => `collection skipped, ${failure}`) };
}

module.exports = { listSkillsShMatches, listGithubMatches, listCollectionMatches };
