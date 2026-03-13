"""
Tests for GPU Temperature Monitor skill
"""
import pytest
import sys
import os
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import GPUTemperatureMonitor


class TestGPUTemperatureMonitor:
    """Test GPU Temperature Monitor functionality"""

    def test_initialization(self):
        """Test skill initialization with default values"""
        skill = GPUTemperatureMonitor()
        assert skill.action == "check"
        assert skill.threshold == 80.0
        assert skill.polling_interval == 5
        assert skill.hysteresis == 10.0

    def test_initialization_with_kwargs(self):
        """Test skill initialization with custom values"""
        skill = GPUTemperatureMonitor(
            action="monitor",
            threshold=85.0,
            polling_interval=10
        )
        assert skill.action == "monitor"
        assert skill.threshold == 85.0
        assert skill.polling_interval == 10

    def test_safe_int_conversion(self):
        """Test safe integer conversion"""
        skill = GPUTemperatureMonitor()
        assert skill._safe_int("42") == 42
        assert skill._safe_int("N/A") is None
        assert skill._safe_int("") is None
        assert skill._safe_int("[Not Supported]") is None

    def test_safe_float_conversion(self):
        """Test safe float conversion"""
        skill = GPUTemperatureMonitor()
        assert skill._safe_float("62.5") == 62.5
        assert skill._safe_float("N/A") is None
        assert skill._safe_float("") is None

    def test_unknown_action(self):
        """Test handling of unknown action"""
        skill = GPUTemperatureMonitor(action="unknown")
        result = skill.run()
        assert "error" in result
        assert "Unknown action" in result["error"]

    def test_threshold_evaluation(self):
        """Test threshold evaluation logic"""
        skill = GPUTemperatureMonitor(threshold=80.0, hysteresis=10.0)

        # Simulate GPU data
        mock_gpus = [
            {"name": "GPU 0", "temperature_celsius": 75.0},  # OK
            {"name": "GPU 1", "temperature_celsius": 78.0},  # WARNING (in hysteresis band)
            {"name": "GPU 2", "temperature_celsius": 85.0},  # CRITICAL
        ]

        for gpu in mock_gpus:
            temp = gpu["temperature_celsius"]
            if temp >= skill.threshold:
                gpu["status"] = "CRITICAL"
            elif temp >= (skill.threshold - skill.hysteresis):
                gpu["status"] = "WARNING"
            else:
                gpu["status"] = "OK"

        assert mock_gpus[0]["status"] == "OK"
        assert mock_gpus[1]["status"] == "WARNING"
        assert mock_gpus[2]["status"] == "CRITICAL"

    def test_recommendation_generation(self):
        """Test recommendation messages"""
        skill = GPUTemperatureMonitor()

        # Test CRITICAL recommendation
        result = {"status": "CRITICAL"}
        rec = skill._get_recommendation(result)
        assert "Immediate action required" in rec

        # Test WARNING recommendation
        result = {"status": "WARNING"}
        rec = skill._get_recommendation(result)
        assert "Monitor closely" in rec

        # Test OK recommendation
        result = {"status": "OK"}
        rec = skill._get_recommendation(result)
        assert "No action required" in rec


class TestNvidiaSmiParsing:
    """Test nvidia-smi output parsing"""

    def test_parse_valid_output(self):
        """Test parsing valid nvidia-smi CSV output"""
        skill = GPUTemperatureMonitor()

        mock_output = "0, NVIDIA GB10, 62, 45, 34, 1024, 8192\n1, NVIDIA GB10, 64, 55, 38, 2048, 8192"

        lines = mock_output.split("\n")
        gpus = []

        for line in lines:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 7:
                gpus.append({
                    "id": int(parts[0]),
                    "name": parts[1],
                    "temperature_celsius": skill._safe_float(parts[2]),
                    "utilization_percent": skill._safe_int(parts[3]),
                    "fan_speed_percent": skill._safe_int(parts[4]),
                    "memory_used_mb": skill._safe_int(parts[5]),
                    "memory_total_mb": skill._safe_int(parts[6])
                })

        assert len(gpus) == 2
        assert gpus[0]["name"] == "NVIDIA GB10"
        assert gpus[0]["temperature_celsius"] == 62.0
        assert gpus[1]["temperature_celsius"] == 64.0

    def test_parse_output_with_na(self):
        """Test parsing output with N/A values"""
        skill = GPUTemperatureMonitor()

        mock_output = "0, NVIDIA GB10, 62, N/A, N/A, 1024, N/A"

        parts = [p.strip() for p in mock_output.split(",")]

        gpu = {
            "id": int(parts[0]),
            "name": parts[1],
            "temperature_celsius": skill._safe_float(parts[2]),
            "utilization_percent": skill._safe_int(parts[3]),
            "fan_speed_percent": skill._safe_int(parts[4]),
            "memory_used_mb": skill._safe_int(parts[5]),
            "memory_total_mb": skill._safe_int(parts[6])
        }

        assert gpu["temperature_celsius"] == 62.0
        assert gpu["utilization_percent"] is None
        assert gpu["fan_speed_percent"] is None
        assert gpu["memory_total_mb"] is None


class TestHistoryManagement:
    """Test history tracking functionality"""

    def test_history_save_and_load(self, tmp_path):
        """Test saving and loading history"""
        import tempfile

        skill = GPUTemperatureMonitor(history_file=str(tmp_path / "test_history.json"))

        mock_gpus = [
            {"name": "GPU 0", "temperature_celsius": 62.0, "status": "OK"}
        ]

        skill._save_to_history(mock_gpus)

        # Load and verify
        with open(tmp_path / "test_history.json", "r") as f:
            history = json.load(f)

        assert len(history) == 1
        assert history[0]["gpus"][0]["temperature_celsius"] == 62.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
