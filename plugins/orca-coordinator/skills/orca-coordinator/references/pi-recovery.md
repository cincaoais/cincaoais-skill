# Worker recovery (mostly pi)

Fixes that worked in past runs. Orca's own `references/recovery-and-cleanup.md`
covers failed starts and lost workers. Use this file for the cases below. `ORCA`
is the executable Orca's guide resolved.

## Prompt never submitted (idle at 0% context after worker-start)

Pi workers sometimes sit at `input_accepted` with the spec never submitted. Send a
short nudge that points at the spec file and names the IDs, because a worker
started this way otherwise sends `worker_done` without them and Orca rejects it:

```text
ORCA orchestration send --to dispatch:<dispatch_id> --subject "start" --body-file <nudge.md>
```

`nudge.md`: "Your task is in <spec path>. Start now. When done, send worker_done
with --task <task_id> --dispatch <dispatch_id>."

## Stalled mid-task, or provider error (HTTP 400 server_error)

Read the worker first: `ORCA orchestration worker-read --dispatch <dispatch_id>`.

| Context used | Action |
|---|---|
| Under about 70% | `send` a nudge naming the missing sections and repeating: write to the file one section per tool call, then worker_done |
| Over about 70% | `worker-stop`, keep its partial output, dispatch a continuation worker that starts from those files |

Common causes to fix in the next spec:
- The worker drafted a large file as prose in chat: add "write incrementally, one
  section per tool call".
- The worker ended its turn after announcing "Now I'll write...": add "do not end
  your turn before worker_done".
- The task read too much: split it (about 100 KB of reading per pi worker).

## New coordinator session refuses task-create ("consumer_fenced")

The Run is still bound to the old coordinator. Run
`ORCA orchestration run-use --id <run_id>` first. Scripts that grep task IDs out
of command output get empty IDs silently after this error, so check that an ID
exists before starting workers.

## Long jobs killed when a worker is released

Releasing a worker closes its terminal and kills background children it started
(`nohup ... &`). Downloads and demo runs that must outlive the worker go in their
own Orca terminal. Check for running children before releasing.

## Footprint checks

- Use `git --no-optional-locks status`; plain `git status` touches `.git`.
- Scope `find` to the touched folders, with `timeout 300` and
  `-not -path '*/node_modules/*'`. A `find` over a whole GitHub folder has hung
  workers for 15-40 minutes.

## Paths

- Workers sometimes rename outputs; check the exact path in acceptance.
- Some PDF tools (poppler `pdftotext`) cannot open non-ASCII paths: copy to an
  ASCII temp name first.
