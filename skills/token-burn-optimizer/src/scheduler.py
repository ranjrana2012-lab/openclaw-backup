#!/usr/bin/env python3
"""
Burn Scheduler Module
Coordinates burn cycles and manages token distribution over time
"""

import asyncio
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional


class BurnScheduler:
    """Manages burn scheduling and cycle coordination"""

    def __init__(self, config: Dict, monitor, burner, heartbeat):
        """Initialize scheduler with components"""
        self.config = config
        self.monitor = monitor
        self.burner = burner
        self.heartbeat = heartbeat

        # Cycle settings
        self.prompts_per_cycle = config.get("prompts_per_cycle", 2400)
        self.cycle_hours = config.get("cycle_duration_hours", 5)
        self.target_burn_rate = config.get("target_burn_rate", 0.90)

        # State
        self.running = False
        self.current_cycle_start = None
        self.current_cycle_number = 0
        self.prompts_this_cycle = 0
        self.tokens_this_cycle = 0

        # State file
        self.state_file = Path(config.get("state_file", "/workspace/data/token-burn-optimizer-state.json"))
        self.log_file = config.get("log_file", "/workspace/logs/token-burn-optimizer.log")

        # Load previous state
        self.load_state()

    async def _log(self, message: str):
        """Write log message"""
        try:
            timestamp = datetime.now().isoformat()
            log_entry = f"[{timestamp}] {message}\n"

            with open(self.log_file, "a") as f:
                f.write(log_entry)
        except Exception:
            pass

    def load_state(self):
        """Load state from file"""
        try:
            if self.state_file.exists():
                with open(self.state_file) as f:
                    state = json.load(f)
                    self.current_cycle_number = state.get("cycle_number", 0)
                    self.prompts_this_cycle = state.get("prompts_this_cycle", 0)
                    self.tokens_this_cycle = state.get("tokens_this_cycle", 0)

                    if state.get("cycle_start"):
                        self.current_cycle_start = datetime.fromisoformat(state["cycle_start"])
        except Exception:
            pass

    def save_state(self):
        """Save state to file"""
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)

            state = {
                "cycle_number": self.current_cycle_number,
                "cycle_start": self.current_cycle_start.isoformat() if self.current_cycle_start else None,
                "prompts_this_cycle": self.prompts_this_cycle,
                "tokens_this_cycle": self.tokens_this_cycle,
                "last_updated": datetime.now().isoformat()
            }

            with open(self.state_file, "w") as f:
                json.dump(state, f, indent=2)
        except Exception:
            pass

    async def start_new_cycle(self):
        """Start a new burn cycle"""
        self.current_cycle_start = datetime.now()
        self.current_cycle_number += 1
        self.prompts_this_cycle = 0
        self.tokens_this_cycle = 0

        await self._log(f"🔄 Cycle {self.current_cycle_number} started | Target: {self.prompts_per_cycle} prompts")

        # Save state
        self.save_state()

    def get_cycle_progress(self) -> Dict:
        """Get current cycle progress"""
        if not self.current_cycle_start:
            return {
                "active": False,
                "cycle_number": 0,
                "prompts_this_cycle": 0,
                "tokens_this_cycle": 0,
                "progress_percent": 0
            }

        elapsed = (datetime.now() - self.current_cycle_start).total_seconds()
        cycle_duration_seconds = self.cycle_hours * 3600
        progress_percent = min(100, (elapsed / cycle_duration_seconds) * 100)

        return {
            "active": True,
            "cycle_number": self.current_cycle_number,
            "cycle_start": self.current_cycle_start.isoformat(),
            "prompts_this_cycle": self.prompts_this_cycle,
            "tokens_this_cycle": self.tokens_this_cycle,
            "target_prompts": self.prompts_per_cycle,
            "progress_percent": round(progress_percent, 2),
            "elapsed_seconds": round(elapsed),
            "remaining_seconds": round(max(0, cycle_duration_seconds - elapsed)),
            "prompts_remaining": max(0, self.prompts_per_cycle - self.prompts_this_cycle)
        }

    async def run_cycle(self):
        """Run a single burn cycle"""
        self.running = True

        await self._log("🔥 Burn scheduler started")

        # Start first cycle
        await self.start_new_cycle()

        while self.running:
            try:
                # Get current balance
                balance = await self.monitor.check_balance_async()
                metrics = self.monitor.calculate_burn_metrics(balance)

                # Get cycle progress
                progress = self.get_cycle_progress()

                # Check if cycle is complete
                elapsed = (datetime.now() - self.current_cycle_start).total_seconds()
                cycle_duration_seconds = self.cycle_hours * 3600

                if elapsed >= cycle_duration_seconds:
                    # Cycle complete
                    await self._log(f"✅ Cycle {self.current_cycle_number} complete | "
                                  f"Prompts: {self.prompts_this_cycle}/{self.prompts_per_cycle} | "
                                  f"Tokens: {self.tokens_this_cycle}")

                    # Start new cycle
                    await self.start_new_cycle()
                    continue

                # Calculate if we need to burn more prompts this cycle
                prompts_remaining = self.prompts_per_cycle - self.prompts_this_cycle
                time_remaining = cycle_duration_seconds - elapsed

                if prompts_remaining > 0 and time_remaining > 0:
                    # Calculate optimal burn rate for remaining time
                    prompts_per_hour = prompts_remaining / (time_remaining / 3600)
                    prompts_per_minute = prompts_per_hour / 60

                    # Determine how many prompts to send now
                    # Send in batches every minute
                    batch_size = max(1, int(prompts_per_minute * 0.5))  # Send half of what we need per minute

                    if batch_size > 0:
                        # Burn tokens
                        await self._log(f"🔥 Burning {batch_size} prompts | "
                                      f"Progress: {progress['prompts_this_cycle']}/{self.prompts_per_cycle} | "
                                      f"Time: {progress['progress_percent']}%")

                        result = await self.burner._execute_burn_async(batch_size)

                        if result.get("status") == "completed":
                            self.prompts_this_cycle += result.get("successful", 0)
                            self.tokens_this_cycle += result.get("total_tokens_burned", 0)

                            await self._log(f"✓ Burned {result.get('total_tokens_burned', 0)} tokens | "
                                          f"Success: {result.get('successful', 0)}/{batch_size}")
                        else:
                            await self._log(f"⚠ Burn failed: {result.get('error', 'Unknown')}")

                        # Save state
                        self.save_state()

                # Wait before next check
                await asyncio.sleep(60)  # Check every minute

            except Exception as e:
                await self._log(f"❌ Scheduler error: {str(e)}")
                await asyncio.sleep(60)

    def stop(self):
        """Stop the scheduler"""
        self.running = False
        self.save_state()

    def get_status(self) -> Dict:
        """Get scheduler status"""
        progress = self.get_cycle_progress()
        burner_stats = self.burner.get_statistics()
        heartbeat_status = self.heartbeat.get_status()

        return {
            "scheduler": {
                "running": self.running,
                "current_cycle": progress,
                "configuration": {
                    "prompts_per_cycle": self.prompts_per_cycle,
                    "cycle_duration_hours": self.cycle_hours,
                    "target_burn_rate": self.target_burn_rate
                }
            },
            "burner": burner_stats,
            "heartbeat": heartbeat_status
        }
