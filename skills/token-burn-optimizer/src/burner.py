#!/usr/bin/env python3
"""
Token Burner Module
Executes strategic API calls to burn tokens at optimal rate
"""

import json
import asyncio
import urllib.request
import urllib.error
from datetime import datetime
from typing import Dict, Optional, List


class TokenBurner:
    """Burn tokens by executing strategic API calls"""

    def __init__(self, config: Dict):
        """Initialize token burner with configuration"""
        self.config = config
        self.api_key = config["api_key"]
        self.endpoint = config["balance_endpoint"]
        self.model = config["model"]
        self.prompt_template = config.get("burn_prompt_template",
                                           "System check. Status: OK. Timestamp: {timestamp}")

        # Burn statistics
        self.burn_count = 0
        self.total_burned_tokens = 0
        self.failed_burns = 0
        self.last_burn_time = None

        # Rate limiting
        self.max_retries = config.get("max_retries", 3)
        self.retry_delay = config.get("retry_delay_seconds", 5)
        self.min_interval = config.get("min_prompt_interval_seconds", 1)

        self._last_burn_timestamp = 0

    async def _execute_single_burn(self, prompt: str = None) -> Dict:
        """Execute a single API call to burn tokens"""
        if prompt is None:
            prompt = self.prompt_template.format(timestamp=datetime.now().isoformat())

        # Enforce minimum interval
        loop = asyncio.get_event_loop()
        current_time = loop.time()
        time_since_last = current_time - self._last_burn_timestamp
        if time_since_last < self.min_interval:
            await asyncio.sleep(self.min_interval - time_since_last)

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 50,  # Small token count for efficient burning
            "stream": False
        }

        retry_count = 0
        last_error = None

        while retry_count < self.max_retries:
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
                    self._last_burn_timestamp = loop.time()

                    if response.status == 200:
                        response_data = json.loads(response.read().decode('utf-8'))
                        usage = response_data.get("usage", {})
                        tokens_used = usage.get("total_tokens", 0)

                        self.burn_count += 1
                        self.total_burned_tokens += tokens_used
                        self.last_burn_time = datetime.now().isoformat()

                        return {
                            "status": "success",
                            "tokens_burned": tokens_used,
                            "prompt_tokens": usage.get("prompt_tokens", 0),
                            "completion_tokens": usage.get("completion_tokens", 0),
                            "timestamp": self.last_burn_time
                        }

                    elif response.status == 429:
                        # Rate limited - wait and retry
                        await asyncio.sleep(self.retry_delay)
                        retry_count += 1
                        last_error = "Rate limited, retrying"
                        continue

                    elif response.status == 401:
                        return {
                            "status": "error",
                            "error": "Unauthorized - Check API key",
                            "tokens_burned": 0
                        }

                    else:
                        return {
                            "status": "error",
                            "error": f"API error: {response.status}",
                            "tokens_burned": 0
                        }

            except urllib.error.HTTPError as e:
                if e.code == 429:
                    await asyncio.sleep(self.retry_delay)
                    retry_count += 1
                    last_error = f"Rate limited: {e.code}"
                    continue
                self.failed_burns += 1
                return {
                    "status": "error",
                    "error": f"HTTP error: {e.code}",
                    "tokens_burned": 0
                }

            except urllib.error.URLError as e:
                retry_count += 1
                last_error = str(e.reason)
                await asyncio.sleep(self.retry_delay)
                continue

            except Exception as e:
                self.failed_burns += 1
                return {
                    "status": "error",
                    "error": str(e),
                    "tokens_burned": 0
                }

        # Max retries exceeded
        self.failed_burns += 1
        return {
            "status": "error",
            "error": f"Max retries exceeded: {last_error}",
            "tokens_burned": 0
        }

    def execute_burn(self, num_prompts: int = 1) -> Dict:
        """Execute token burn (synchronous wrapper)"""
        try:
            return asyncio.run(self._execute_burn_async(num_prompts))
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "tokens_burned": 0
            }

    async def _execute_burn_async(self, num_prompts: int = 1) -> Dict:
        """Execute multiple burn requests"""
        if num_prompts < 1:
            return {
                "status": "error",
                "error": "num_prompts must be >= 1",
                "tokens_burned": 0
            }

        results = []
        total_tokens = 0
        successful = 0
        failed = 0

        # Execute burns sequentially to respect rate limits
        for i in range(num_prompts):
            result = await self._execute_single_burn()
            results.append(result)

            if result.get("status") == "success":
                total_tokens += result.get("tokens_burned", 0)
                successful += 1
            else:
                failed += 1

            # Small delay between burns to avoid rate limiting
            if i < num_prompts - 1:  # Don't sleep after last burn
                await asyncio.sleep(self.min_interval)

        return {
            "status": "completed",
            "total_prompts": num_prompts,
            "successful": successful,
            "failed": failed,
            "total_tokens_burned": total_tokens,
            "average_tokens_per_prompt": round(total_tokens / successful, 2) if successful > 0 else 0,
            "timestamp": datetime.now().isoformat(),
            "details": results[:10]  # Include first 10 results
        }

    async def burn_to_target(self, target_tokens: int, balance_checker=None) -> Dict:
        """Burn tokens until reaching target amount"""
        burned = 0
        prompts_sent = 0

        while burned < target_tokens:
            # Check remaining balance if checker provided
            if balance_checker:
                balance = await balance_checker.check_balance_async()
                remaining = balance.get("available_tokens", 0)

                if remaining <= target_tokens * 0.1:  # 10% buffer
                    return {
                        "status": "completed",
                        "target_met": True,
                        "tokens_burned": burned,
                        "prompts_sent": prompts_sent,
                        "reason": "Low balance threshold reached"
                    }

            result = await self._execute_single_burn()

            if result.get("status") == "success":
                burned += result.get("tokens_burned", 0)
                prompts_sent += 1
            else:
                # Stop on persistent errors
                if self.failed_burns > 5:
                    return {
                        "status": "error",
                        "tokens_burned": burned,
                        "prompts_sent": prompts_sent,
                        "error": "Too many failed burns"
                    }

                await asyncio.sleep(self.retry_delay)

        return {
            "status": "completed",
            "target_met": burned >= target_tokens,
            "tokens_burned": burned,
            "prompts_sent": prompts_sent
        }

    def get_statistics(self) -> Dict:
        """Get burn statistics"""
        return {
            "total_burns": self.burn_count,
            "total_tokens_burned": self.total_burned_tokens,
            "failed_burns": self.failed_burns,
            "success_rate": round((1 - self.failed_burns / max(1, self.burn_count + self.failed_burns)) * 100, 2),
            "average_tokens_per_burn": round(self.total_burned_tokens / max(1, self.burn_count), 2),
            "last_burn_time": self.last_burn_time
        }

    def reset_statistics(self):
        """Reset burn statistics"""
        self.burn_count = 0
        self.total_burned_tokens = 0
        self.failed_burns = 0
        self.last_burn_time = None
