# hephaestus init

## Overview

`hephaestus init` initializes the Hephaestus working environment in the current directory.

## Usage

```bash
hephaestus init [OPTIONS]
```

## Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--workers` | `-w` | 3 | Specify the number of worker agents |
| `--force` | `-f` | - | Force reinitialization even if hephaestus-work exists |
| `--help` | - | - | Show help message |

## Behavior

When you run this command, the following operations are performed:

1. **Directory Structure Creation**
   ```
   hephaestus-work/
   ├── .claude/              # Agent configuration
   │   ├── CLAUDE.md         # Common configuration
   │   ├── master/           # Master configuration
   │   │   └── CLAUDE.md
   │   └── worker/           # Worker configuration
   │       └── CLAUDE.md
   ├── config.yaml           # System configuration
   ├── cache/                # Cache
   │   ├── agent_states/
   │   └── rate_limits/
   ├── tasks/                # Task management
   │   ├── pending/
   │   ├── in_progress/
   │   └── completed/
   ├── communication/        # Inter-agent communication
   │   ├── master_to_worker/
   │   └── worker_to_master/
   ├── logs/                 # Log files
   ├── checkpoints/          # Checkpoints
   └── progress/             # Progress tracking
   ```

2. **Configuration File Generation**
   - `config.yaml`: System-wide configuration
   - `.claude/CLAUDE.md`: Common agent configuration
   - `.claude/master/CLAUDE.md`: Master agent persona
   - `.claude/worker/CLAUDE.md`: Worker agent persona

3. **Initialization Confirmation**
   - Upon successful completion, information about created directories and files is displayed

## Examples

### Basic Initialization

```bash
hephaestus init
```

Creates an environment with 3 worker agents by default.

### Initialize with Specific Worker Count

```bash
hephaestus init --workers 5
```

Creates an environment with 5 worker agents.

### Force Reinitialization

```bash
hephaestus init --force
```

Overwrites existing `hephaestus-work` directory without warning.

## Errors and Solutions

### When hephaestus-work Directory Already Exists

```
hephaestus-work directory already exists at:
/path/to/hephaestus-work

Use --force to reinitialize.
```

**Solution**: Use `--force` option to reinitialize, or manually delete the directory and run again.

### Permission Denied

```
Permission denied: 'hephaestus-work'
```

**Solution**: Ensure you have write permissions in the current directory.

## Notes

- After initialization, you can edit `config.yaml` to customize worker count and other settings
- Using `--force` option will result in loss of all existing data including tasks and logs
- After initialization, you can start agents with `hephaestus attach --create`

## Related Commands

- [hephaestus attach](./attach_en.md) - Start agents
- [hephaestus status](./status_en.md) - Check initialization status
- [hephaestus kill](./kill_en.md) - Terminate session

## Configuration File

For details about `config.yaml` generated after initialization, see [Configuration Guide](../configuration_en.md).
