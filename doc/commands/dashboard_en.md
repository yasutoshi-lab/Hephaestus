# hephaestus dashboard

## Overview

`hephaestus dashboard` launches a TUI (Terminal User Interface) dashboard for real-time monitoring of agent status.

## Usage

```bash
hephaestus dashboard
```

## Features

The dashboard displays the following information in real-time:

### 1. Agent Status
- Current state of each agent (Master, Worker-1, Worker-2...)
- Status indicators:
  - 🟢 **Active**: Agent is operating normally
  - 🟡 **Idle**: Agent is running but has no tasks
  - 🔴 **Error**: Agent has encountered an error
  - ⚪ **Unknown**: Session is not running

### 2. Tasks Overview Table
- Task ID
- Status (pending/in_progress/completed)
- Priority
- Assigned agent

### 3. Communication Log Stream
- Real-time display of inter-agent communication messages
- Keeps up to 100 most recent lines

## Key Bindings

| Key | Function |
|-----|----------|
| `q` | Quit dashboard |
| `r` | Manually refresh screen |
| `^p` | Open command palette |

## Auto-refresh

The dashboard automatically updates information every 2 seconds.

## Examples

### Basic Usage

```bash
# Launch dashboard
hephaestus dashboard
```

### Dashboard with Running Session

```bash
# Start session in one terminal
terminal1$ hephaestus attach --create

# Display dashboard in another terminal
terminal2$ hephaestus dashboard
```

This allows you to monitor agent operations in real-time.

## Warnings and Errors

### When Session is Not Running

```
Warning: No active session found

The dashboard will show limited information.
Start the session with: hephaestus attach --create
```

In this case, the dashboard will start but all agents will be shown as "Unknown" state.

### When Not Initialized

```
Not initialized. Run 'hephaestus init' first.
```

**Solution**: First run `hephaestus init`.

## Dashboard Screen Layout

```
┌─────────────────────────────────────────────────────────┐
│            Hephaestus Dashboard              02:42:04   │
├─────────────────────────────────────────────────────────┤
│ Agent Status                                            │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │
│ │🟢 Master    │ │🟢 Worker-1  │ │🟢 Worker-2  │       │
│ │Status: Act..│ │Status: Act..│ │Status: Act..│       │
│ │Task: Analy..│ │Task: Execu..│ │Task: Gener..│       │
│ └─────────────┘ └─────────────┘ └─────────────┘       │
│                                                         │
│ Tasks Overview                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ ID    │ Status      │ Priority │ Assigned To      │ │
│ │ t-001 │ in_progress │ high     │ worker-1         │ │
│ │ t-002 │ pending     │ medium   │ worker-2         │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ Communication Log                                       │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 02:42:10 master -> worker-1: New task assigned...  │ │
│ │ 02:42:11 worker-1 -> master: Task acknowledged     │ │
│ │ 02:42:15 worker-1 -> master: Task completed        │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ q Quit  r Refresh                          ^p palette │
└─────────────────────────────────────────────────────────┘
```

## Performance

- The dashboard is lightweight and uses minimal system resources
- Fast even with many tasks or logs, as it only displays recent information

## Notes

- The dashboard is read-only (cannot control agents)
- Do not launch within a tmux session (recommend separate terminal window)
- Exiting the dashboard does not affect the agent session

## Troubleshooting

### Screen Not Displaying Correctly

Check your terminal size. Minimum recommended size:
- Width: 80+ characters
- Height: 24+ lines

### Information Not Updating

Press `r` key to try manual refresh.

## Related Commands

- [hephaestus attach](./attach_en.md) - Start agent session
- [hephaestus logs](./logs_en.md) - Detailed log viewing
- [hephaestus status](./status_en.md) - Quick status check
- [hephaestus monitor](./monitor_en.md) - Monitor task distribution

## Technical Details

The dashboard is implemented using the [Textual](https://github.com/Textualize/textual) framework.
