#!/usr/bin/env python3
"""
Token Burn Optimizer - Main Entry Point
Optimizes z.ai GLM 4.7 token usage with automated burning and monitoring
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add templates path for SkillBase
sys.path.insert(0, '/workspace/skills/_templates')

from src.monitor import TokenMonitor
from src.burner import TokenBurner
from src.heartbeat import HeartbeatManager
from src.scheduler import BurnScheduler


class TokenBurnOptimizer:
    """Main orchestrator for token burn optimization"""

    def __init__(self, config_path: str = None):
        """Initialize the optimizer with configuration"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config.json"

        with open(config_path) as f:
            self.config = json.load(f)["token_burn_optimizer"]

        self.monitor = TokenMonitor(self.config)
        self.burner = TokenBurner(self.config)
        self.heartbeat = HeartbeatManager(self.config)
        self.scheduler = None  # Initialized on start
        self.running = False

    def start(self):
        """Start the optimizer daemon"""
        print(f"🔥 Token Burn Optimizer Starting...")
        print(f"   Target: {self.config['target_burn_rate']*100}% burn rate")
        print(f"   Volume: {self.config['prompts_per_cycle']} prompts/cycle")
        print(f"   Cycle: {self.config['cycle_duration_hours']} hours")
        print(f"   Until: {self.config['end_date']}")

        self.scheduler = BurnScheduler(self.config, self.monitor, self.burner, self.heartbeat)
        self.running = True

        # Start all components
        asyncio.run(self._run_async())

    async def _run_async(self):
        """Run all components asynchronously"""
        import asyncio

        tasks = [
            self.scheduler.run_cycle(),
            self.heartbeat.run() if self.config.get("enable_heartbeat", True) else None
        ]

        # Filter out None tasks
        tasks = [t for t in tasks if t is not None]

        await asyncio.gather(*tasks)

    def stop(self):
        """Stop the optimizer daemon"""
        print("🛑 Stopping Token Burn Optimizer...")
        self.running = False

        if self.scheduler:
            self.scheduler.stop()

        print("✓ Optimizer stopped")

    def status(self):
        """Get current status and metrics"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "running": self.running,
            "config": {
                "target_burn_rate": self.config["target_burn_rate"],
                "prompts_per_cycle": self.config["prompts_per_cycle"],
                "cycle_duration_hours": self.config["cycle_duration_hours"],
                "end_date": self.config["end_date"]
            }
        }

        if self.scheduler:
            status.update(self.scheduler.get_status())

        # Get current balance
        balance = self.monitor.get_balance()
        status["balance"] = balance

        return status

    def balance(self):
        """Check current token balance"""
        return self.monitor.get_balance()

    def burn(self, amount: int = None):
        """Manually trigger token burn"""
        if amount is None:
            # Calculate default amount based on config
            balance = self.monitor.get_balance()
            amount = int(balance.get("available_tokens", 0) * 0.01)  # 1% of balance

        print(f"🔥 Burning {amount} tokens...")
        result = self.burner.execute_burn(amount)
        return result

    def logs(self, lines: int = 50):
        """View recent activity logs"""
        log_path = Path(self.config.get("log_file", "/workspace/logs/token-burn-optimizer.log"))

        if not log_path.exists():
            return {"error": "Log file not found"}

        with open(log_path) as f:
            all_lines = f.readlines()

        recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines

        return {
            "log_file": str(log_path),
            "total_lines": len(all_lines),
            "showing": len(recent_lines),
            "entries": [line.strip() for line in recent_lines]
        }

    def config_get(self):
        """Get current configuration"""
        return self.config

    def config_set(self, key: str, value):
        """Update configuration value"""
        # Navigate through nested config keys
        keys = key.split(".")
        current = self.config

        for k in keys[:-1]:
            if k not in current:
                return {"error": f"Key path {key} not found"}
            current = current[k]

        # Type conversion
        if isinstance(current[keys[-1]], bool):
            value = value.lower() in ("true", "1", "yes")
        elif isinstance(current[keys[-1]], int):
            value = int(value)
        elif isinstance(current[keys[-1]], float):
            value = float(value)

        current[keys[-1]] = value

        return {"success": True, "key": key, "value": value}


def run(action: str = "status", **kwargs):
    """Main entry point for skill execution"""
    optimizer = TokenBurnOptimizer()

    try:
        if action == "start":
            optimizer.start()
        elif action == "stop":
            optimizer.stop()
        elif action == "status":
            result = optimizer.status()
            print(json.dumps(result, indent=2))
            return result
        elif action == "balance":
            result = optimizer.balance()
            print(json.dumps(result, indent=2))
            return result
        elif action == "burn":
            amount = kwargs.get("amount")
            result = optimizer.burn(amount)
            print(json.dumps(result, indent=2))
            return result
        elif action == "logs":
            lines = int(kwargs.get("lines", 50))
            result = optimizer.logs(lines)
            print(json.dumps(result, indent=2))
            return result
        elif action == "config":
            if "key" in kwargs and "value" in kwargs:
                result = optimizer.config_set(kwargs["key"], kwargs["value"])
            else:
                result = optimizer.config_get()
            print(json.dumps(result, indent=2))
            return result
        else:
            return {"error": f"Unknown action: {action}"}

    except KeyboardInterrupt:
        print("\n⚠ Interrupted by user")
        optimizer.stop()
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Token Burn Optimizer")
    parser.add_argument("action", choices=["start", "stop", "status", "balance", "burn", "logs", "config"],
                       help="Action to perform")
    parser.add_argument("--amount", type=int, help="Amount of tokens to burn (for burn action)")
    parser.add_argument("--lines", type=int, default=50, help="Number of log lines to show (for logs action)")
    parser.add_argument("--key", type=str, help="Config key to set (for config action)")
    parser.add_argument("--value", type=str, help="Config value to set (for config action)")

    args = parser.parse_args()

    kwargs = {}
    if args.amount:
        kwargs["amount"] = args.amount
    if args.lines:
        kwargs["lines"] = args.lines
    if args.key:
        kwargs["key"] = args.key
    if args.value:
        kwargs["value"] = args.value

    run(args.action, **kwargs)
