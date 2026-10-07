// Search cache: keywords -> results, kept 7 days, so repeated domains skip the network.
// Entries carry the session id so a repeat search within one session is reported as such.
const fs = require('node:fs');
const path = require('node:path');
const { getClaudeHome } = require('./local');
const { stem } = require('./match');

const TTL_MS = 7 * 24 * 60 * 60 * 1000;

// An unsubstituted `${CLAUDE_PLUGIN_DATA}` means the skill runs outside a plugin.
function resolveDataDir(arg) {
  return arg && !arg.includes('${') ? arg : path.join(getClaudeHome(), 'skill-scout');
}

function getCacheFile(dataDir) {
  return path.join(dataDir, 'search-cache.json');
}

function listEntries(dataDir) {
  try {
    const entries = JSON.parse(fs.readFileSync(getCacheFile(dataDir), 'utf8'));
    return entries.filter((entry) => Date.now() - Date.parse(entry.date) < TTL_MS);
  } catch {
    return [];
  }
}

function computeOverlap(a, b) {
  const stems = new Set(b.map(stem));
  return a.filter((keyword) => stems.has(stem(keyword))).length / Math.max(a.length, 1);
}

// Exact keyword match from any session, or a half-overlapping search from this session.
function getCachedSearch(dataDir, keywords, session) {
  const key = [...keywords].sort().join('|');
  return listEntries(dataDir).find(
    (entry) => entry.key === key || (session && entry.session === session && computeOverlap(keywords, entry.keywords) >= 0.5),
  );
}

function updateCache(dataDir, entry) {
  const key = [...entry.keywords].sort().join('|');
  const entries = [{ ...entry, key }, ...listEntries(dataDir).filter((old) => old.key !== key)].slice(0, 50);
  try {
    fs.mkdirSync(dataDir, { recursive: true });
    fs.writeFileSync(getCacheFile(dataDir), JSON.stringify(entries));
  } catch {
    // The cache is an optimization; a read-only data dir must not fail the search.
  }
}

module.exports = { resolveDataDir, getCachedSearch, updateCache };
