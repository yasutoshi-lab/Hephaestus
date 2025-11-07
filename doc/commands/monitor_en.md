# hephaestus monitor

## Overview

`hephaestus monitor` monitors task distribution and automatically notifies Worker agents.

## Usage

```bash
hephaestus monitor [OPTIONS]
```

## Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--interval` | `-i` | 5 | Task check interval (seconds) |
| `--max-iterations` | `-m` | 120 | Maximum monitoring iterations (~10 minutes) |
| `--help` | - | - | Show help message |

## Behavior

1. Monitor `communication/master_to_worker/` directory
2. Detect new task assignment files
3. Notify relevant Worker via tmux
4. Worker receives and executes task
5. Periodically display status

## Examples

### Basic Monitoring

```bash
hephaestus monitor
```

Start monitoring with default settings (5 second interval, up to 120 times).

### Custom Interval Monitoring

```bash
# Check every 10 seconds
hephaestus monitor --interval 10

# Check every 2 seconds (high frequency)
hephaestus monitor -i 2
```

### Long-term Monitoring

```bash
# Monitor up to 300 times (~25 minutes at 5 second interval)
hephaestus monitor --max-iterations 300

# Monitor up to 600 times (~50 minutes at 5 second interval)
hephaestus monitor -m 600
```

## Monitoring Output

```
┌─────────────────── Task Monitor Started ───────────────────┐
│ Monitoring task distribution                               │
│                                                            │
│ Session: hephaestus                                        │
│ Workers: 3                                                 │
│ Check interval: 5s                                         │
│ Max duration: ~10 minutes                                  │
└────────────────────────────────────────────────────────────┘

Press Ctrl+C to stop monitoring

[10:15:30] New task detected: task_001.md → worker-1
[10:15:35] Task acknowledged by worker-1
[10:16:20] Task completed by worker-1
[10:16:25] New task detected: task_002.md → worker-2
...
```

## Stopping

### Manual Stop

Press `Ctrl+C` to stop monitoring and display status summary:

```
Monitoring stopped by user
Tasks: 5 total, 3 completed
```

### Automatic Stop

Automatically stops when maximum iterations are reached:

```
✓ Monitoring completed
Tasks: 5 total, 5 completed
```

## Notification Method

Monitor notifies Workers using:

1. **tmux send-keys**: Send message directly to Worker pane
2. **Notification message**: `"New task assigned! Please read [filename]..."`
3. **File path specification**: Explicitly state task file location

## Errors and Solutions

### Session Not Running

```
No active session found: hephaestus

Start the session first with: hephaestus attach --create
```

**Solution**: First start the session.

### Not Initialized

```
Not initialized. Run 'hephaestus init' first.
```

**Solution**: Run `hephaestus init`.

## Use Cases

### Development/Debugging

```bash
# Monitor with short interval
hephaestus monitor -i 2 -m 30
```

### Production

```bash
# Stable long-term monitoring
hephaestus monitor -i 10 -m 1000
```

### Background Execution

```bash
# Run in background with nohup
nohup hephaestus monitor -i 5 -m 500 > monitor.log 2>&1 &
```

## Monitored Information

- New task assignments
- Worker responses
- Task completion notifications
- Error occurrences

## Notes

- Monitor is read-only and doesn't modify tasks
- Multiple Monitors can run simultaneously without issues
- Operates independently from tmux session

## Related Commands

- [hephaestus attach](./attach_en.md) - Start session (required)
- [hephaestus dashboard](./dashboard_en.md) - Graphical monitoring
- [hephaestus logs](./logs_en.md) - Detailed log checking
- [hephaestus status](./status_en.md) - Check current status
