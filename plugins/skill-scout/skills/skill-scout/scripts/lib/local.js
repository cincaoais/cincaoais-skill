// Local discovery: skills already installed on this machine, and plugins offered by
// marketplaces the user has added but not installed. No network access.
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { computeScore, parseFrontmatter } = require('./match');

function getClaudeHome() {
  return process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), '.claude');
}

function getJsonFile(file) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch {
    return undefined;
  }
}

function listSubdirs(dir) {
  try {
    return fs.readdirSync(dir).map((name) => path.join(dir, name)).filter((p) => fs.statSync(p).isDirectory());
  } catch {
    return [];
  }
}

// Skill folders directly under `root`; `synced/<bucket>/<skill>` holds skills synced from claude.ai.
function listSkillDirs(root) {
  return listSubdirs(root).flatMap((dir) =>
    path.basename(dir) === 'synced' ? listSubdirs(dir).flatMap(listSubdirs) : [dir],
  ).filter((dir) => fs.existsSync(path.join(dir, 'SKILL.md')));
}

function buildSkill(dir, scope) {
  const fields = parseFrontmatter(fs.readFileSync(path.join(dir, 'SKILL.md'), 'utf8'));
  return { scope, name: fields.name || path.basename(dir), description: fields.description || '', path: dir };
}

function listInstalledSkills(keywords, projectDir) {
  const claudeHome = getClaudeHome();
  const roots = [
    { scope: 'personal', dir: path.join(claudeHome, 'skills') },
    { scope: 'project', dir: path.join(projectDir, '.claude', 'skills') },
    { scope: 'skills CLI store, not loaded unless linked', dir: path.join(os.homedir(), '.agents', 'skills') },
  ];
  const installed = getJsonFile(path.join(claudeHome, 'plugins', 'installed_plugins.json'))?.plugins || {};
  for (const [id, installs] of Object.entries(installed)) {
    for (const { installPath } of installs) roots.push({ scope: `plugin ${id}`, dir: path.join(installPath, 'skills') });
  }
  const seen = new Set();
  return roots
    .flatMap(({ scope, dir }) => listSkillDirs(dir).map((skillDir) => buildSkill(skillDir, scope)))
    .filter((skill) => {
      const real = fs.realpathSync(skill.path);
      return seen.has(real) ? false : seen.add(real);
    })
    .map((skill) => ({ ...skill, score: computeScore(keywords, `${skill.name} ${skill.description}`) }))
    .filter((skill) => skill.score > 0)
    .sort((a, b) => b.score - a.score);
}

function listMarketplacePlugins(keywords) {
  const pluginsDir = path.join(getClaudeHome(), 'plugins');
  const known = getJsonFile(path.join(pluginsDir, 'known_marketplaces.json')) || {};
  const installed = getJsonFile(path.join(pluginsDir, 'installed_plugins.json'))?.plugins || {};
  return Object.entries(known).flatMap(([marketplace, { installLocation }]) => {
    const file = installLocation?.endsWith('.json')
      ? installLocation
      : path.join(installLocation || '', '.claude-plugin', 'marketplace.json');
    return (getJsonFile(file)?.plugins || [])
      .filter((entry) => !installed[`${entry.name}@${marketplace}`])
      .map((entry) => ({
        source: 'marketplace',
        repo: marketplace,
        skill: entry.name,
        description: entry.description || '',
        install: `claude plugin install ${entry.name}@${marketplace}`,
        score: computeScore(
          keywords,
          [entry.name, entry.description, entry.category, ...(entry.keywords || []), ...(entry.tags || [])].join(' '),
        ),
      }));
  }).filter((plugin) => plugin.score > 0);
}

module.exports = { getClaudeHome, listInstalledSkills, listMarketplacePlugins };
