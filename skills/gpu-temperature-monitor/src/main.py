#!/usr/bin/env python3
"""
GPU Temperature Monitor - Monitors NVIDIA GPU thermal status and utilization.

Actions:
- check: Check current GPU temperature and health status
- monitor: Continuous monitoring loop with alerts
- history: View temperature history and trends
- alert: Check if temperature exceeds threshold
"""
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List

# Add templates to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "_templates"))

from devops_template import DevOpsSkillBase


class GPUTemperatureMonitor(DevOpsSkillBase):
    """Monitors NVIDIA GPU temperature and thermal status"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.action = kwargs.get("action", "check")
        self.gpu_id = kwargs.get("gpu_id")
        self.threshold = self._safe_float(kwargs.get("threshold", 80.0))
        self.polling_interval = self._safe_int(kwargs.get("polling_interval", 5))
        self.history_file = kwargs.get("history_file", "/tmp/gpu_temp_history.json")
        self.hysteresis = self._safe_float(kwargs.get("hysteresis", 10.0))
        # Set defaults if conversion failed
        if self.threshold is None:
            self.threshold = 80.0
        if self.polling_interval is None:
            self.polling_interval = 5
        if self.hysteresis is None:
            self.hysteresis = 10.0

    def _execute(self, **kwargs) -> dict:
        """Execute GPU Temperature Monitor action"""

        if self.action == "check":
            return self._check_action()
        elif self.action == "monitor":
            return self._monitor_action()
        elif self.action == "history":
            return self._history_action()
        elif self.action == "alert":
            return self._alert_action()
        else:
            return {
                "status": "error",
                "error": f"Unknown action: {self.action}"
            }

    def _check_action(self) -> dict:
        """Check current GPU temperature and health status"""

        gpu_data = self._get_gpu_temperature_data()

        if "error" in gpu_data:
            return gpu_data

        # Evaluate each GPU against threshold
        gpus = []
        overall_status = "OK"
        alert_triggered = False
        critical_gpu = None

        for gpu in gpu_data.get("gpus", []):
            temp = gpu.get("temperature_celsius", 0)
            status = "OK"
            alert_message = None

            # Check against threshold
            if temp >= self.threshold:
                status = "CRITICAL"
                alert_message = (
                    f"CRITICAL: {gpu['name']} temperature is {temp}°C "
                    f"(Threshold: {self.threshold}°C). Thermal throttling likely imminent."
                )
                alert_triggered = True
                critical_gpu = gpu
            elif temp >= (self.threshold - self.hysteresis):
                status = "WARNING"
                alert_message = (
                    f"WARNING: {gpu['name']} temperature is {temp}°C. "
                    f"Approaching critical threshold."
                )

            gpu["status"] = status
            gpu["alert_message"] = alert_message
            gpus.append(gpu)

        # Determine overall status
        if alert_triggered:
            overall_status = "CRITICAL"
            overall_message = f"CRITICAL: {critical_gpu['name']} exceeded thermal threshold."
        elif any(g["status"] == "WARNING" for g in gpus):
            overall_status = "WARNING"
            overall_message = "Some GPUs are running hot. Monitor closely."
        else:
            overall_message = "All GPUs operating normally."

        # Save to history
        self._save_to_history(gpus)

        return {
            "status": overall_status,
            "gpus": gpus,
            "alert_message": overall_message,
            "threshold": self.threshold,
            "timestamp": datetime.utcnow().isoformat()
        }

    def _monitor_action(self) -> dict:
        """Run continuous monitoring loop"""

        iterations = kwargs.get("iterations", 10) if 'kwargs' in globals() else 10
        results = []

        for i in range(iterations):
            result = self._check_action()
            results.append({
                "iteration": i + 1,
                "timestamp": result.get("timestamp"),
                "status": result.get("status"),
                "temperatures": [g.get("temperature_celsius") for g in result.get("gpus", [])]
            })

            # Alert on critical
            if result.get("status") == "CRITICAL":
                print(f"[ALERT] {result.get('alert_message')}")

            time.sleep(self.polling_interval)

        return {
            "status": "complete",
            "iterations": iterations,
            "results": results,
            "summary": f"Monitoring complete. {iterations} checks performed."
        }

    def _history_action(self) -> dict:
        """View temperature history and trends"""

        try:
            with open(self.history_file, "r") as f:
                history = json.load(f)
        except FileNotFoundError:
            return {
                "status": "error",
                "error": "No history found. Run 'check' action first."
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Failed to read history: {str(e)}"
            }

        # Analyze trends
        if history:
            latest = history[-1]
            avg_temps = []
            for entry in history:
                for gpu in entry.get("gpus", []):
                    avg_temps.append(gpu.get("temperature_celsius", 0))

            if avg_temps:
                avg_temp = sum(avg_temps) / len(avg_temps)
                max_temp = max(avg_temps)
                min_temp = min(avg_temps)

                return {
                    "status": "success",
                    "history": history,
                    "summary": {
                        "entries": len(history),
                        "avg_temperature": round(avg_temp, 1),
                        "max_temperature": max_temp,
                        "min_temperature": min_temp,
                        "latest_check": latest.get("timestamp")
                    }
                }

        return {
            "status": "success",
            "history": history,
            "summary": {"entries": 0}
        }

    def _alert_action(self) -> dict:
        """Check if temperature exceeds threshold and return alert status"""

        result = self._check_action()

        return {
            "status": result.get("status"),
            "alert_triggered": result.get("status") in ["WARNING", "CRITICAL"],
            "alert_message": result.get("alert_message"),
            "gpus_over_threshold": [
                g for g in result.get("gpus", [])
                if g.get("temperature_celsius", 0) >= self.threshold
            ],
            "recommended_action": self._get_recommendation(result)
        }

    def _get_gpu_temperature_data(self) -> dict:
        """Get GPU temperature data from nvidia-smi"""

        # Use CSV format for easy parsing
        cmd = [
            "nvidia-smi",
            "--query-gpu=index,name,temperature.gpu,utilization.gpu,fan.speed,memory.used,memory.total",
            "--format=csv,noheader,nounits"
        ]

        result = self.execute_subprocess(cmd)

        if result.get("status") != "success":
            return {"error": "Failed to query GPU", "details": result.get("error", "Unknown error")}

        lines = result["stdout"].strip().split("\n")
        gpus = []

        for line in lines:
            if not line.strip():
                continue

            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 7:
                continue

            gpu = {
                "id": int(parts[0]) if parts[0].isdigit() else 0,
                "name": parts[1],
                "temperature_celsius": self._safe_float(parts[2]),
                "utilization_percent": self._safe_int(parts[3]),
                "fan_speed_percent": self._safe_int(parts[4]),
                "memory_used_mb": self._safe_int(parts[5]),
                "memory_total_mb": self._safe_int(parts[6])
            }

            # Calculate memory percent if both values present
            if gpu["memory_total_mb"] and gpu["memory_total_mb"] > 0:
                gpu["memory_percent"] = round(
                    gpu["memory_used_mb"] / gpu["memory_total_mb"] * 100, 1
                ) if gpu["memory_used_mb"] else 0
            else:
                gpu["memory_percent"] = 0

            gpus.append(gpu)

        if not gpus:
            return {"error": "No GPUs found"}

        return {"gpus": gpus, "count": len(gpus)}

    def _save_to_history(self, gpus: list) -> None:
        """Save current readings to history file"""

        history = []
        try:
            with open(self.history_file, "r") as f:
                history = json.load(f)
        except:
            pass

        # Keep last 100 entries
        history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "gpus": gpus
        })

        if len(history) > 100:
            history = history[-100:]

        try:
            with open(self.history_file, "w") as f:
                json.dump(history, f, indent=2)
        except:
            pass  # History save is optional

    def _get_recommendation(self, check_result: dict) -> str:
        """Get recommendation based on current status"""

        status = check_result.get("status")

        if status == "CRITICAL":
            return "Immediate action required: Check cooling system, reduce GPU load, or stop affected processes."
        elif status == "WARNING":
            return "Monitor closely. Consider reducing GPU load or checking airflow."
        else:
            return "No action required. GPU temperatures are within normal range."

    def _safe_int(self, val) -> Optional[int]:
        """Safely convert string to int"""
        if isinstance(val, int):
            return val
        if isinstance(val, float):
            return int(val)
        try:
            return int(val) if val and val not in ["N/A", "[N/A]"] else None
        except (ValueError, TypeError):
            return None

    def _safe_float(self, val) -> Optional[float]:
        """Safely convert string to float"""
        if isinstance(val, float):
            return val
        if isinstance(val, int):
            return float(val)
        try:
            return float(val) if val and val not in ["N/A", "[N/A]"] else None
        except (ValueError, TypeError):
            return None


def run(**kwargs) -> dict:
    """Entry point for skill execution"""
    skill = GPUTemperatureMonitor(**kwargs)
    return skill.run()


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2))
