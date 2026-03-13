#!/usr/bin/env python3
"""
Token Monitor Module
Checks z.ai GLM 4.7 token balance and usage statistics
"""

import json
import asyncio
import urllib.request
import urllib.error
from datetime import datetime
from typing import Dict, Optional


class TokenMonitor:
    """Monitor token balance and usage for z.ai GLM 4.7 API"""

    def __init__(self, config: Dict):
        """Initialize token monitor with configuration"""
        self.config = config
        self.api_key = config["api_key"]
        self.endpoint = config["balance_endpoint"]
        self.model = config["model"]

        # Balance cache
        self._balance_cache = None
        self._balance_cache_time = None
        self._cache_ttl_seconds = 60  # Cache balance for 1 minute

    def get_balance(self) -> Dict:
        """Get current token balance (synchronous wrapper)"""
        try:
            return asyncio.run(self._get_balance_async())
        except Exception as e:
            return {
                "error": str(e),
                "available_tokens": 0,
                "status": "error"
            }

    async def _get_balance_async(self) -> Dict:
        """Get current token balance from z.ai API"""
        # Check cache first
        if self._balance_cache and self._balance_cache_time:
            age = (datetime.now() - self._balance_cache_time).total_seconds()
            if age < self._cache_ttl_seconds:
                return self._balance_cache

        # Make a minimal API call to check balance
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": "ping"}
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

            with urllib.request.urlopen(req, timeout=30) as response:
                if response.status == 200:
                    response_data = json.loads(response.read().decode('utf-8'))

                    # Check rate limit headers if available
                    remaining = response.headers.get("X-RateLimit-Remaining")
                    limit = response.headers.get("X-RateLimit-Limit")
                    reset = response.headers.get("X-RateLimit-Reset")

                    # Extract usage from response
                    usage = response_data.get("usage", {})
                    tokens_used = usage.get("total_tokens", 0)

                    balance_info = {
                        "status": "success",
                        "available_tokens": int(remaining) if remaining else 1000000,  # Default high value
                        "limit": int(limit) if limit else -1,
                        "reset_time": reset,
                        "last_checked": datetime.now().isoformat(),
                        "model": self.model,
                        "last_request_tokens": tokens_used
                    }

                    # Cache the result
                    self._balance_cache = balance_info
                    self._balance_cache_time = datetime.now()

                    return balance_info
                elif response.status == 401:
                    return {
                        "status": "error",
                        "error": "Unauthorized - Check API key",
                        "available_tokens": 0
                    }
                elif response.status == 429:
                    return {
                        "status": "rate_limited",
                        "error": "Rate limit exceeded",
                        "available_tokens": 0
                    }
                else:
                    return {
                        "status": "error",
                        "error": f"API error: {response.status}",
                        "available_tokens": 0
                    }

        except urllib.error.HTTPError as e:
            return {
                "status": "error",
                "error": f"HTTP error: {e.code}",
                "available_tokens": 0
            }
        except urllib.error.URLError as e:
            return {
                "status": "network_error",
                "error": str(e.reason),
                "available_tokens": 0
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "available_tokens": 0
            }

    async def check_balance_async(self) -> Dict:
        """Async wrapper for balance checking"""
        return await self._get_balance_async()

    def calculate_burn_metrics(self, balance: Dict) -> Dict:
        """Calculate burn metrics based on current balance"""
        target_burn_rate = self.config.get("target_burn_rate", 0.90)
        prompts_per_cycle = self.config.get("prompts_per_cycle", 2400)
        cycle_hours = self.config.get("cycle_duration_hours", 5)

        available = balance.get("available_tokens", 0)
        limit = balance.get("limit", available)

        # Calculate tokens to burn this cycle
        tokens_to_burn = int(available * target_burn_rate)

        # Calculate prompts distribution
        prompts_per_hour = prompts_per_cycle / cycle_hours
        prompts_per_minute = prompts_per_hour / 60
        interval_seconds = 3600 / prompts_per_hour if prompts_per_hour > 0 else 60

        return {
            "tokens_available": available,
            "tokens_limit": limit,
            "target_burn_rate": target_burn_rate,
            "tokens_to_burn": tokens_to_burn,
            "prompts_per_cycle": prompts_per_cycle,
            "prompts_per_hour": round(prompts_per_hour, 2),
            "prompts_per_minute": round(prompts_per_minute, 2),
            "suggested_interval_seconds": round(interval_seconds, 2),
            "cycle_duration_hours": cycle_hours
        }

    def get_health_status(self) -> Dict:
        """Get overall health status of the monitoring system"""
        balance = self.get_balance()

        return {
            "monitor_status": "healthy" if balance.get("status") == "success" else "unhealthy",
            "last_check": balance.get("last_checked"),
            "api_reachable": balance.get("status") != "error",
            "balance_status": balance.get("status"),
            "cache_age_seconds": (datetime.now() - self._balance_cache_time).total_seconds() if self._balance_cache_time else 0
        }

    def estimate_remaining_capacity(self, balance: Dict) -> Dict:
        """Estimate remaining capacity until end date"""
        from datetime import datetime

        end_date_str = self.config.get("end_date", "2027-03-31")
        end_date = datetime.fromisoformat(end_date_str)
        now = datetime.now()

        days_remaining = (end_date - now).days
        hours_remaining = days_remaining * 24

        prompts_per_cycle = self.config.get("prompts_per_cycle", 2400)
        cycle_hours = self.config.get("cycle_duration_hours", 5)

        cycles_remaining = hours_remaining / cycle_hours
        total_prompts_capacity = cycles_remaining * prompts_per_cycle

        return {
            "end_date": end_date_str,
            "days_remaining": days_remaining,
            "hours_remaining": hours_remaining,
            "cycles_remaining": round(cycles_remaining, 1),
            "prompts_per_cycle": prompts_per_cycle,
            "total_estimated_prompts": round(total_prompts_capacity)
        }
