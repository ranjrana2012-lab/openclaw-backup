#!/usr/bin/env python3
"""
Heartbeat Keeper
Keep gateway and API connections alive
"""

import json
import urllib.request
import sys
from datetime import datetime

sys.path.insert(0, '/workspace/skills/_templates')


def ping_gateway(url="http://localhost:18790/health"):
    """Ping OpenClaw gateway"""
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            return {
                "status": "healthy" if response.status == 200 else "error",
                "status_code": response.status,
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


def ping_api(config_path=None):
    """Ping z.ai API with heartbeat"""
    if config_path is None:
        config_path = "/workspace/skills/monitoring/token-burn-optimizer/config.json"

    with open(config_path) as f:
        config = json.load(f)["token_burn_optimizer"]

    api_key = config["api_key"]
    endpoint = config["balance_endpoint"]
    model = config["model"]

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "heartbeat"}],
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

        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                response_data = json.loads(response.read().decode('utf-8'))
                usage = response_data.get("usage", {})

                return {
                    "status": "healthy",
                    "tokens_used": usage.get("total_tokens", 0),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "status_code": response.status,
                    "timestamp": datetime.now().isoformat()
                }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


def run(action="check", **kwargs):
    """Main entry point"""
    if action == "check":
        gateway = ping_gateway()
        api = ping_api()

        result = {
            "gateway": gateway,
            "api": api,
            "overall_status": "healthy" if gateway.get("status") == "healthy" and api.get("status") == "healthy" else "unhealthy"
        }

        print(json.dumps(result, indent=2))
        return result
    elif action == "gateway":
        result = ping_gateway()
        print(json.dumps(result, indent=2))
        return result
    elif action == "api":
        result = ping_api()
        print(json.dumps(result, indent=2))
        return result
    else:
        return {"error": f"Unknown action: {action}"}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("action", default="check", nargs='?')
    args = parser.parse_args()
    run(args.action)
