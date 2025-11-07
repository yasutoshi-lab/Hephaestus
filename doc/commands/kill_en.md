# hephaestus kill

## Overview

`hephaestus kill` stops all agents and terminates the tmux session.

## Usage

```bash
hephaestus kill [OPTIONS]
```

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--force` | `-f` | Skip confirmation prompt and force termination |
| `--help` | - | Show help message |

## Behavior

1. Check if session exists
2. Display confirmation prompt (unless `--force` option is used)
3. Save session state
4. Terminate tmux session
5. Stop all agent processes

## Examples

### Normal Termination (with confirmation)

```bash
hephaestus kill
```

The following confirmation is displayed:
```
Are you sure you want to kill session 'hephaestus' and stop all agents? [y/N]:
```

### Force Termination (without confirmation)

```bash
hephaestus kill --force
```

Terminates session immediately without confirmation.

## Session State Saving

Before termination, the following information is saved to `hephaestus-work/cache/last_session_state.json`:

```json
{
  "session_name": "hephaestus",
  "terminated_at": 1699376400.123,
  "worker_count": 3
}
```

## Errors and Solutions

### Session Doesn't Exist

```
No active session found: hephaestus
```

In this case, the session has already terminated.

### Not Initialized

```
No hephaestus-work directory found. Nothing to kill.
```

Environment is not initialized or already in clean state.

## Notes

- Killing will interrupt running tasks
- Incomplete tasks will remain in `tasks/in_progress/`
- You can check incomplete tasks on next startup
- `--force` option is useful in scripts and CI/CD environments

## Data Retention

The following data is retained after termination:

- ✅ Task files (`tasks/`)
- ✅ Log files (`logs/`)
- ✅ Communication history (`communication/`)
- ✅ Configuration file (`config.yaml`)
- ✅ Agent configuration (`.claude/`)

## Restart

After termination, you can restart in the same environment:

```bash
hephaestus attach --create
```

## Related Commands

- [hephaestus attach](./attach_en.md) - Start session
- [hephaestus status](./status_en.md) - Check session status
- [hephaestus init](./init_en.md) - Reinitialize environment
