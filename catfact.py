#!/usr/bin/env python3
"""QuickCatFact – fetch a random cat fact and optionally notify via Telegram.

Features:
- GET request to https://catfact.ninja/fact
- Print fact to console
- If `--token` and `--chat` arguments are supplied, send the fact using Telegram Bot API

Usage:
    python3 catfact.py [--token BOT_TOKEN] [--chat CHAT_ID]
"""

import argparse
import json
import sys
from urllib import request, error

API_URL = "https://catfact.ninja/fact"
TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"


def fetch_fact() -> str:
    """Retrieve a random cat fact from the public API."""
    try:
        with request.urlopen(API_URL) as resp:
            data = json.load(resp)
            return data.get("fact", "<no fact found>")
    except error.URLError as e:
        sys.stderr.write(f"Error fetching cat fact: {e}\n")
        sys.exit(1)


def send_telegram(token: str, chat_id: str, message: str) -> None:
    """Send a message to Telegram using Bot API.
    Raises on failure.
    """
    payload = json.dumps({"chat_id": chat_id, "text": message}).encode("utf-8")
    url = TELEGRAM_API.format(token=token)
    req = request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with request.urlopen(req) as resp:
            resp_data = json.load(resp)
            if not resp_data.get("ok"):
                raise RuntimeError(f"Telegram API error: {resp_data}")
    except error.HTTPError as e:
        raise RuntimeError(f"Telegram HTTP error {e.code}: {e.read().decode()}")
    except error.URLError as e:
        raise RuntimeError(f"Telegram connection error: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="QuickCatFact – fetch a cat fact and optionally send to Telegram.")
    parser.add_argument("--token", help="Telegram Bot token (if you want to send a message)")
    parser.add_argument("--chat", help="Telegram chat ID (required when --token is used)")
    args = parser.parse_args()

    fact = fetch_fact()
    print(fact)

    if args.token:
        if not args.chat:
            sys.stderr.write("--chat is required when --token is provided.\n")
            sys.exit(2)
        try:
            send_telegram(args.token, args.chat, fact)
            print("✅ Sent to Telegram")
        except Exception as exc:
            sys.stderr.write(f"Failed to send Telegram message: {exc}\n")
            sys.exit(3)

if __name__ == "__main__":
    main()
