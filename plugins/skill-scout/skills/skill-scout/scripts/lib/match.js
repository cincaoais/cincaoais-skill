// Keyword handling shared by every source: cleaning, stemming, scoring, and SKILL.md frontmatter.

const MAX_KEYWORDS = 6;

function parseKeywords(args) {
  const cleaned = args
    .map((arg) => arg.toLowerCase().replace(/[^a-z0-9.+#_\- ]/g, ' ').replace(/\s+/g, ' ').trim())
    .filter(Boolean);
  return [...new Set(cleaned)].slice(0, MAX_KEYWORDS);
}

// Crude stem so "caching" meets "cache" and "strategies" meets "strategy".
function stem(word) {
  const base = word.length > 4 ? word.replace(/(ings?|ies|es|ed|ers?|s)$/, '') : word;
  return base.slice(0, 6);
}

function isKeywordHit(keyword, haystack) {
  return keyword.split(' ').every((token) => {
    const escaped = stem(token).replace(/[.+#]/g, '\\$&');
    return new RegExp(`(^|\\s)${escaped}`).test(haystack);
  });
}

function computeScore(keywords, text) {
  const haystack = ` ${String(text || '').toLowerCase().replace(/[^a-z0-9+#.]+/g, ' ')} `;
  return keywords.filter((keyword) => isKeywordHit(keyword, haystack)).length;
}

function parseFrontmatter(markdown) {
  const block = /^﻿?---\r?\n([\s\S]*?)\r?\n---/.exec(markdown);
  if (!block) return {};
  const fields = {};
  const lines = block[1].split(/\r?\n/);
  for (let i = 0; i < lines.length; i += 1) {
    const field = /^([A-Za-z_-]+):\s*(.*)$/.exec(lines[i]);
    if (!field) continue;
    const parts = [field[2].replace(/^[>|][+-]?$/, '')];
    while (i + 1 < lines.length && /^\s/.test(lines[i + 1])) parts.push(lines[(i += 1)].trim());
    fields[field[1]] = parts.join(' ').trim().replace(/^(["'])(.*)\1$/, '$2');
  }
  return fields;
}

module.exports = { parseKeywords, computeScore, parseFrontmatter, stem };
