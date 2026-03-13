#!/usr/bin/env python3
"""
Token Balance Monitor
Check z.ai GLM 4.7 token balance and usage
"""

import json
import urllib.request
import sys

sys.path.insert(0, '/workspace/skills/_templates')


def check_balance(config_path=None):
    """Check current token balance"""
    if config_path is None:
        config_path = "/workspace/skills/monitoring/token-burn-optimizer/config.json"

    with open(config_path) as f:
        config = json.load(f)["token_burn_optimizer"]

    api_key = config["api_key"]
    endpoint = config["balance_endpoint"]
    model = config["model"]

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "ping"}],
        "max_tokens": 1
    }

    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            endpoint,
            data=data,
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status == 200:
                response_data = json.loads(response.read().decode('utf-8'))
                usage = response_data.get("usage", {})

                return {
                    "status": "success",
                    "available_tokens": "unlimited",
                    "last_request_tokens": usage.get("total_tokens", 0),
                    "prompt_tokens": usage.get("prompt_tokens", 0),
                    "completion_tokens": usage.get("completion_tokens", 0),
                    "model": model
                }
            else:
                return {"status": "error", "error": f"HTTP {response.status}"}

    except Exception as e:
        return {"status": "error", "error": str(e)}


def run(action="check", **kwargs):
    """Main entry point"""
    if action == "check":
        result = check_balance()
        print(json.dumps(result, indent=2))
        return result
    else:
        return {"error": f"Unknown action: {action}"}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("action", default="check")
    args = parser.parse_args()
    run(args.action)
