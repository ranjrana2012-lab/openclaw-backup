#!/usr/bin/env python3
"""
Token Burn Engine
Burn tokens by executing API calls
"""

import json
import urllib.request
import sys
from datetime import datetime

sys.path.insert(0, '/workspace/skills/_templates')


def burn_tokens(amount=1, config_path=None):
    """Burn tokens by making API calls"""
    if config_path is None:
        config_path = "/workspace/skills/monitoring/token-burn-optimizer/config.json"

    with open(config_path) as f:
        config = json.load(f)["token_burn_optimizer"]

    api_key = config["api_key"]
    endpoint = config["balance_endpoint"]
    model = config["model"]

    results = []
    total_tokens = 0

    for i in range(amount):
        prompt = f"Burn check {i+1}/{amount} at {datetime.now().isoformat()}"
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 50
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
                    tokens_used = usage.get("total_tokens", 0)
                    total_tokens += tokens_used

                    results.append({
                        "request": i + 1,
                        "tokens_burned": tokens_used,
                        "status": "success"
                    })
                else:
                    results.append({
                        "request": i + 1,
                        "tokens_burned": 0,
                        "status": f"error: {response.status}"
                    })

        except Exception as e:
            results.append({
                "request": i + 1,
                "tokens_burned": 0,
                "status": f"error: {str(e)}"
            })

    return {
        "status": "completed",
        "total_requests": amount,
        "total_tokens_burned": total_tokens,
        "average_tokens": round(total_tokens / amount, 2) if amount > 0 else 0,
        "results": results
    }


def run(action="burn", amount=1, **kwargs):
    """Main entry point"""
    if action == "burn":
        result = burn_tokens(int(amount))
        print(json.dumps(result, indent=2))
        return result
    else:
        return {"error": f"Unknown action: {action}"}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("action", default="burn")
    parser.add_argument("--amount", type=int, default=1)
    args = parser.parse_args()
    run(args.action, amount=args.amount)
