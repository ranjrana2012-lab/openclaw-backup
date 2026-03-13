---
id: gpu-temperature-monitor
name: GPU Temperature Monitor
category: devops
version: 1.0.0
status: ready
owner: internal-team
tags:
  - gpu
  - monitoring
  - health
  - devops

# GPU Temperature Monitor

Continuously monitors thermal throttling and memory utilization of NVIDIA GPUs to ensure the DGX Spark system operates within safe thermal limits.

## User Prompts
- "Check GPU temperature"
- "Is my GPU overheating?"
- "Show me thermal metrics for all GPUs"
- "Alert if temperature exceeds 80 degrees"
- "What is the current fan speed?"
- "Monitor VRAM usage"
- "Show GPU temperature history"
- "Are my GPUs thermal throttling?"

## Actions

### check
Check current GPU temperature and health status for all GPUs or a specific GPU.

**Parameters:**
- `gpu_id` (optional, integer): Specific GPU index to check. If not provided, checks all GPUs.
- `threshold` (optional, float): Critical temperature threshold in Celsius (default: 80.0).
- `hysteresis` (optional, float): Warning band below threshold (default: 10.0).

**Examples:**
\`\`\`bash
# Check all GPUs
skill-run devops gpu-temperature-monitor check

# Check specific GPU with custom threshold
skill-run devops gpu-temperature-monitor check gpu_id=0 threshold=85.0
\`\`\`

### monitor
Run continuous monitoring loop with alerts.

**Parameters:**
- `iterations` (optional, integer): Number of checks to perform (default: 10).
- `polling_interval` (optional, integer): Seconds between checks (default: 5).
- `threshold` (optional, float): Temperature threshold (default: 80.0).

**Examples:**
\`\`\`bash
# Monitor for 20 iterations
skill-run devops gpu-temperature-monitor monitor iterations=20 polling_interval=10

# Monitor with custom threshold
skill-run devops gpu-temperature-monitor monitor threshold=75.0
\`\`\`

### alert
Check if temperature exceeds threshold and get alert status with recommendations.

**Parameters:**
- `threshold` (optional, float): Temperature threshold (default: 80.0).
- `gpu_id` (optional, integer): Specific GPU to check.

**Examples:**
\`\`\`bash
# Check for alerts
skill-run devops gpu-temperature-monitor alert threshold=85.0

# Check specific GPU
skill-run devops gpu-temperature-monitor alert gpu_id=0
\`\`\`

### history
View temperature history and trends from previous checks.

**Examples:**
\`\`\`bash
skill-run devops gpu-temperature-monitor history
\`\`\`

## Outputs

Each action returns:

- **status** (string): Overall status ("OK", "WARNING", "CRITICAL")
- **gpus** (array): Array of GPU objects with:
  - **id** (integer): GPU index
  - **name** (string): GPU name
  - **temperature_celsius** (float): Current temperature
  - **utilization_percent** (integer): GPU utilization
  - **fan_speed_percent** (integer): Fan speed
  - **memory_used_mb** (integer): VRAM used
  - **memory_total_mb** (integer): Total VRAM
  - **memory_percent** (float): VRAM utilization
  - **status** (string): Individual GPU status
  - **alert_message** (string): Alert if any
- **alert_message** (string): Overall alert message
- **threshold** (float): Threshold used
- **timestamp** (string): ISO timestamp

## Status Levels

- **OK**: Temperature below warning threshold (threshold - 10°C)
- **WARNING**: Temperature in warning band (threshold - 10°C to threshold)
- **CRITICAL**: Temperature at or above threshold

## Dependencies

- **nvidia-smi**: CLI tool for querying GPU status
- **Python**: Standard library only (no additional packages required)

## Safety Guardrails

- **Risk Level**: Medium
- **Approval Required**: No (read-only monitoring)
- **Sensitive Data**: None
- **Failure Mode**: Returns error if nvidia-smi not found

## Examples

### Example 1: Check All GPUs
**Input:**
\`\`\`json
{
  "action": "check",
  "threshold": 75.0
}
\`\`\`

**Output:**
\`\`\`json
{
  "status": "OK",
  "gpus": [
    {
      "id": 0,
      "name": "NVIDIA GB10",
      "temperature_celsius": 62.0,
      "utilization_percent": 45,
      "fan_speed_percent": 34,
      "memory_used_mb": 1024,
      "memory_total_mb": 8192,
      "memory_percent": 12.5,
      "status": "OK",
      "alert_message": null
    }
  ],
  "alert_message": "All GPUs operating normally.",
  "threshold": 75.0,
  "timestamp": "2026-02-05T22:45:00.000Z"
}
\`\`\`

### Example 2: Critical Temperature Alert
**Input:**
\`\`\`json
{
  "action": "check",
  "threshold": 85.0
}
\`\`\`

**Output:**
\`\`\`json
{
  "status": "CRITICAL",
  "gpus": [
    {
      "id": 0,
      "name": "NVIDIA GB10",
      "temperature_celsius": 88.0,
      "utilization_percent": 95,
      "fan_speed_percent": 100,
      "memory_used_mb": 7800,
      "memory_total_mb": 8192,
      "memory_percent": 95.2,
      "status": "CRITICAL",
      "alert_message": "CRITICAL: NVIDIA GB10 temperature is 88.0°C (Threshold: 85.0°C). Thermal throttling likely imminent."
    }
  ],
  "alert_message": "CRITICAL: NVIDIA GB10 exceeded thermal threshold.",
  "threshold": 85.0,
  "timestamp": "2026-02-05T22:45:00.000Z"
}
\`\`\`

## Implementation Notes

- Uses `nvidia-smi` with CSV format for reliable parsing
- Implements safe type conversion for N/A values
- Saves last 100 readings to history file
- Hysteresis band prevents alert flapping
- Compatible with DGX Spark and standard NVIDIA GPUs

## Related Skills

- **gpu-health-auditor** (observability): Comprehensive GPU health monitoring
- **nvidia-driver-update** (devops): Driver management
- **process-hog-finder** (devops): Find GPU-intensive processes
