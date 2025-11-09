# hephaestus status

## Overview

`hephaestus status` displays the current state of Hephaestus.

## Usage

```bash
hephaestus status
```

## Display Contents

The following information is displayed:

- **Work Directory**: Path to .hephaestus-work directory
- **Tmux Session**: Tmux session name
- **Session Active**: Whether the session is running
- **Worker Count**: Number of worker agents

## Output Example

```
                Hephaestus Status
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Component      ┃ Status                           ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Work Directory │ /path/to/.hephaestus-work         │
│ Tmux Session   │ hephaestus                       │
│ Session Active │ Yes                              │
│ Worker Count   │ 3                                │
└────────────────┴──────────────────────────────────┘
```

## Examples

### Basic Usage

```bash
hephaestus status
```

### Usage in Scripts

```bash
# Check if session is running
if hephaestus status | grep -q "Session Active.*Yes"; then
    echo "Hephaestus is running"
else
    echo "Hephaestus is not running"
fi
```

## Session Status

### Running

```
Session Active │ Yes
```

Session is running normally and agents are operating.

### Stopped

```
Session Active │ No
```

Session is not running. Can be started with `hephaestus attach --create`.

## Errors and Solutions

### Not Initialized

```
Not initialized. Run 'hephaestus init' first.
```

**Solution**: First run `hephaestus init`.

## Related Commands

- [hephaestus init](./init_en.md) - Initialize environment
- [hephaestus attach](./attach_en.md) - Start/attach session
- [hephaestus dashboard](./dashboard_en.md) - Detailed status monitoring
- [hephaestus logs](./logs_en.md) - Check logs
