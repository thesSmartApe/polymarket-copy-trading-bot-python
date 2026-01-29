# Polymarket Copy Trading Bot — Python Edition

> **Copy the best, automate success.** Mirror trades from top Polymarket traders with intelligent position sizing and real-time execution.

[![License: ISC](https://img.shields.io/badge/License-ISC-blue.svg)](python/LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

---

## Why This Bot?

A **copy trading bot** for [Polymarket](https://polymarket.com) that lets you automatically follow successful traders like **gabagool22** and others. One user turned **$200 into $800** using this bot by copying proven performers. No manual trading—set your strategy, pick your traders, and let the bot run.

### Real Results

| What you get | Description |
|--------------|-------------|
| **Proven track record** | Users have grown capital (e.g. $200 → $800) by copying top traders |
| **Follow leaders** | Copy traders such as [gabagool22](https://polymarket.com/@gabagool22?tab=activity) and others from the [Polymarket leaderboard](https://polymarket.com/leaderboard) |
| **24/7 automation** | Bot monitors and executes trades in real time so you don’t miss moves |
| **Smart sizing** | Position sizes scale with your capital vs. the trader’s balance |

---

## Quick Start

```bash
# Clone this repository
git clone https://github.com/thesSmartApe/polymarket-copy-trading-bot-python.git
cd polymarket-copy-trading-bot-python/python

# Install dependencies
pip install -r requirements.txt

# Run interactive setup
python -m src.scripts.setup.setup

# Start the bot
python -m src.main
```

**Video:** A step-by-step video on how to run the Polymarket Python copy trading bot is available—check the repository or [releases](https://github.com/thesSmartApe/polymarket-copy-trading-bot-python/releases) for the walkthrough.

📖 **Full setup:** See **[python/README.md](python/README.md)** and **[python/docs/GETTING_STARTED.md](python/docs/GETTING_STARTED.md)** for detailed installation and configuration.

---

## Other Editions

This repo is the **Python** version of the Polymarket Copy Trading Bot. The same project is also available in:

| Edition | Repo | Description |
|---------|------|-------------|
| **TypeScript** | [thesSmartApe/polymarket-copy-trading-bot](https://github.com/thesSmartApe/polymarket-copy-trading-bot) | Full-featured web dashboard, Node.js/TypeScript |
| **Python** | [thesSmartApe/polymarket-copy-trading-bot-python](https://github.com/thesSmartApe/polymarket-copy-trading-bot-python) | This repo — Python, simple CLI, same core logic |
| **Rust** | *(Rust edition link when available)* | High-performance Rust implementation |

Use the edition that fits your stack (Python vs TypeScript vs Rust); all aim to copy successful Polymarket traders with smart position sizing.

---

## Features

- **Multi-trader support** — Copy several traders at once  
- **Smart position sizing** — Automatic scaling based on your balance  
- **Real-time execution** — Trades mirrored within seconds  
- **MongoDB** — Full trade and position history  
- **Safety controls** — Min/max order size, preview mode, tiered multipliers  

---

## Requirements

- **Python 3.10+**
- **MongoDB** (e.g. [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) free tier)
- **Polygon wallet** with USDC and POL (MATIC) for gas
- **RPC endpoint** (e.g. [Alchemy](https://www.alchemy.com) or [Infura](https://infura.io) on Polygon)

---

## Configuration

After cloning, go to the `python` folder and copy `.env.example` to `.env`. Set at least:

- `USER_ADDRESSES` — Wallet addresses of traders to copy (e.g. top leaderboard traders)
- `PROXY_WALLET` — Your Polygon wallet address
- `PRIVATE_KEY` — Your wallet private key (never share or commit)
- `MONGO_URI` — MongoDB connection string
- `RPC_URL` — Polygon RPC URL

Run the setup wizard for a guided config:

```bash
cd python && python -m src.scripts.setup.setup
```

---

## Safety & Disclaimer

- **Use at your own risk.** This bot places real trades with real funds.
- Start with small amounts and use **preview/dry-run** mode when testing.
- Research traders before copying. Past performance does not guarantee future results.
- Not financial advice. For educational use; you are responsible for compliance with local laws and Polymarket’s terms.

---

## Links

- **This repo (Python):** [github.com/thesSmartApe/polymarket-copy-trading-bot-python](https://github.com/thesSmartApe/polymarket-copy-trading-bot-python)
- **TypeScript edition:** [github.com/thesSmartApe/polymarket-copy-trading-bot](https://github.com/thesSmartApe/polymarket-copy-trading-bot)
- **Polymarket:** [polymarket.com](https://polymarket.com) · [Leaderboard](https://polymarket.com/leaderboard)
- **Predictfolio:** [predictfolio.com](https://predictfolio.com) — Trader analytics
- **Contact:** [Telegram @jerrix1](https://t.me/jerrix1)

---

## License

ISC. See [python/LICENSE](python/LICENSE).

**Disclaimer:** Trading involves risk of loss. The developers are not responsible for any financial losses from using this software.
