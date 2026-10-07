// Network and subprocess access for skill-scout. GitHub goes through `gh api` when the
// user is logged in to gh (needed for code search), otherwise through anonymous HTTPS.
// Every request has a timeout and counts against the client's request budget.
const { execFile } = require('node:child_process');

const TIMEOUT_MS = 8000;

// Windows runs npm shims such as npx.cmd only through a shell; callers pass sanitized args.
function runFile(command, args, { timeout = TIMEOUT_MS } = {}) {
  return new Promise((resolve, reject) => {
    execFile(
      command,
      args,
      { timeout, maxBuffer: 32 * 1024 * 1024, windowsHide: true, shell: command.endsWith('.cmd') },
      (err, stdout, stderr) => (err ? reject(Object.assign(err, { stderr })) : resolve(stdout)),
    );
  });
}

function buildClient({ budget = Infinity } = {}) {
  let used = 0;
  let isGhUsable = true;

  function spend() {
    if (used >= budget) throw new Error(`request budget of ${budget} used up`);
    used += 1;
  }

  async function getResponse(url, accept) {
    spend();
    const res = await fetch(url, {
      headers: { 'User-Agent': 'skill-scout', Accept: accept },
      signal: AbortSignal.timeout(TIMEOUT_MS),
    });
    if (!res.ok) {
      const detail = /"message"\s*:\s*"([^"]+)"/.exec(await res.text().catch(() => ''))?.[1].split('. ')[0];
      throw new Error(`HTTP ${res.status} from ${new URL(url).host}${detail ? ` (${detail})` : ''}`);
    }
    return res;
  }

  async function getGhJson(apiPath) {
    spend();
    try {
      return JSON.parse(await runFile('gh', ['api', apiPath], { timeout: TIMEOUT_MS }));
    } catch (err) {
      const isUnavailable = err.code === 'ENOENT' || /gh auth login|GH_TOKEN/.test(err.stderr || '');
      if (!isUnavailable) throw new Error(`gh api: ${(err.stderr || err.message).trim().split('\n')[0]}`);
      used -= 1;
      isGhUsable = false;
      return undefined;
    }
  }

  return {
    getText: async (url) => (await getResponse(url, '*/*')).text(),
    getJson: async (url) => (await getResponse(url, 'application/json')).json(),
    getBuffer: async (url) => Buffer.from(await (await getResponse(url, '*/*')).arrayBuffer()),
    // `requiresAuth` is for endpoints GitHub refuses anonymously, such as code search.
    async getGithub(apiPath, { requiresAuth = false } = {}) {
      const viaGh = isGhUsable ? await getGhJson(apiPath) : undefined;
      if (viaGh !== undefined) return viaGh;
      if (requiresAuth) throw Object.assign(new Error('needs `gh auth login`'), { needsAuth: true });
      return (await getResponse(`https://api.github.com/${apiPath}`, 'application/vnd.github+json')).json();
    },
    get used() {
      return used;
    },
  };
}

module.exports = { buildClient, runFile };
