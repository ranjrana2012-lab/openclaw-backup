#!/usr/bin/env python3
"""
Heartbeat Manager Module
Keeps gateway and API connections alive with periodic pings
"""

import asyncio
import urllib.request
import urllib.error
import json
from datetime import datetime
from typing import Dict, Optional


class HeartbeatManager:
    """Manages heartbeat operations for gateway and API"""

    def __init__(self, config: Dict):
        """Initialize heartbeat manager with configuration"""
        self.config = config
        self.gateway_url = config.get("gateway_health_url", "http://localhost:18790/health")
        self.interval = config.get("heartbeat_interval_seconds", 60)
        self.api_key = config["api_key"]
        self.endpoint = config["balance_endpoint"]
        self.model = config["model"]

        # State
        self.running = False
        self.gateway_healthy = False
        self.api_healthy = False
        self.last_gateway_check = None
        self.last_api_check = None
        self.total_pings = 0
        self.failed_pings = 0

        # Log file
        self.log_file = config.get("log_file", "/workspace/logs/token-burn-optimizer.log")

    async def ping_gateway(self) -> Dict:
        """Ping OpenClaw gateway health endpoint"""
        try:
            req = urllib.request.Request(self.gateway_url)
            with urllib.request.urlopen(req, timeout=5) as response:
                self.gateway_healthy = response.status == 200
                self.last_gateway_check = datetime.now().isoformat()

                return {
                    "status": "success" if self.gateway_healthy else "error",
                    "gateway_url": self.gateway_url,
                    "status_code": response.status,
                    "timestamp": self.last_gateway_check
                }

        except Exception as e:
            self.gateway_healthy = False
            self.last_gateway_check = datetime.now().isoformat()

            return {
                "status": "error",
                "error": str(e),
                "gateway_url": self.gateway_url,
                "timestamp": self.last_gateway_check
            }

    async def ping_api(self) -> Dict:
        """Send minimal heartbeat prompt to z.ai API"""
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": "heartbeat"}
            ],
            "max_tokens": 1,
            "stream": False
        }

        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                self.endpoint,
                data=data,
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }
            )

            with urllib.request.urlopen(req, timeout=10) as response:
                self.api_healthy = response.status == 200
                self.last_api_check = datetime.now().isoformat()

                if response.status == 200:
                    response_data = json.loads(response.read().decode('utf-8'))
                    usage = response_data.get("usage", {})

                    return {
                        "status": "success",
                        "tokens_used": usage.get("total_tokens", 0),
                        "timestamp": self.last_api_check
                    }
                elif response.status == 429:
                    return {
                        "status": "rate_limited",
                        "timestamp": self.last_api_check
                    }
                else:
                    return {
                        "status": "error",
                        "status_code": response.status,
                        "timestamp": self.last_api_check
                    }

        except urllib.error.HTTPError as e:
            self.api_healthy = False
            self.last_api_check = datetime.now().isoformat()
            return {
                "status": "error",
                "error": f"HTTP error: {e.code}",
                "timestamp": self.last_api_check
            }
        except Exception as e:
            self.api_healthy = False
            self.last_api_check = datetime.now().isoformat()
            return {
                "status": "error",
                "error": str(e),
                "timestamp": self.last_api_check
            }

    async def _log(self, message: str):
        """Write log message to file"""
        try:
            timestamp = datetime.now().isoformat()
            log_entry = f"[{timestamp}] {message}\n"

            with open(self.log_file, "a") as f:
                f.write(log_entry)
        except Exception:
            pass  # Don't fail on logging errors

    async def run(self):
        """Run heartbeat loop"""
        self.running = True

        await self._log("🫀 Heartbeat manager started")

        while self.running:
            try:
                self.total_pings += 1

                # Ping gateway
                gateway_result = await self.ping_gateway()
                if gateway_result.get("status") != "success":
                    self.failed_pings += 1
                    await self._log(f"⚠ Gateway unhealthy: {gateway_result}")

                # Ping API
                api_result = await self.ping_api()
                if api_result.get("status") != "success":
                    self.failed_pings += 1
                    await self._log(f"⚠ API unhealthy: {api_result}")
                else:
                    # Log successful heartbeat with token usage
                    tokens = api_result.get("tokens_used", 0)
                    await self._log(f"💓 Heartbeat OK | Gateway: {self.gateway_healthy} | API: {self.api_healthy} | Tokens: {tokens}")

            except Exception as e:
                self.failed_pings += 1
                await self._log(f"❌ Heartbeat error: {str(e)}")

            # Wait for next interval
            await asyncio.sleep(self.interval)

    def stop(self):
        """Stop heartbeat loop"""
        self.running = False

    def get_status(self) -> Dict:
        """Get heartbeat status"""
        return {
            "running": self.running,
            "gateway_healthy": self.gateway_healthy,
            "api_healthy": self.api_healthy,
            "last_gateway_check": self.last_gateway_check,
            "last_api_check": self.last_api_check,
            "total_pings": self.total_pings,
            "failed_pings": self.failed_pings,
            "success_rate": round((1 - self.failed_pings / max(1, self.total_pings)) * 100, 2),
            "interval_seconds": self.interval
        }
