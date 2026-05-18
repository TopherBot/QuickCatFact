# QuickCatFact

**What it does**
- Retrieves a random cat fact from `https://catfact.ninja/fact`.
- Prints the fact to STDOUT.
- (Optional) Sends the fact to a Telegram chat using a bot token and chat ID you provide.

**Why this project?**
- Minimal footprint – only two files.
- Great for showcasing rapid scaffolding, CI pipelines, and Telegram alerts.
- Easy to extend (e.g., add more APIs, schedule with cron, etc.).

**Usage**
```bash
# Simple run – just prints a fact
python3 catfact.py

# Run with Telegram notification
python3 catfact.py --token <BOT_TOKEN> --chat <CHAT_ID>
```

**Requirements**
- Python 3.8+
- `requests` library (`pip install requests`)

**CI Hint**
Add a GitHub Action that runs `python -m pytest` (you can drop a simple test later) and a Telegram alert on success/failure.
