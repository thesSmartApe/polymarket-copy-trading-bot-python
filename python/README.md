# Polymarket Copy Trading Bot — Python Edition

> **Copy the best, automate success.** Mirror trades from top Polymarket traders with intelligent position sizing and real-time execution.

[![License: ISC](https://img.shields.io/badge/License-ISC-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

---

## Why This Bot?

A **copy trading bot** for [Polymarket](https://polymarket.com) that automatically replicates trades from successful traders to your wallet. One user turned **$200 into $800** using this bot by copying proven performers. The bot monitors trader activity 24/7, scales position sizes to your capital, and executes matching orders in real time.

### Who Can You Copy?

Follow top performers from the [Polymarket leaderboard](https://polymarket.com/leaderboard) or [Predictfolio](https://predictfolio.com)—for example, successful traders like [**gabagool22**](https://polymarket.com/@gabagool22?tab=activity). You choose the wallets; the bot does the rest.

### How It Works

1. **Choose traders** — Pick leaders from the [Polymarket leaderboard](https://polymarket.com/leaderboard) or [Predictfolio](https://predictfolio.com) (e.g. [gabagool22](https://polymarket.com/@gabagool22?tab=activity)).
2. **Bot monitors** — Continuously watches for new positions opened by your selected traders.
3. **Smart sizing** — Scales each trade based on your balance vs. the trader’s balance.
4. **Auto execution** — Places matching orders on Polymarket with your wallet.
5. **Full history** — Stores all trades and positions in MongoDB.

---

## Quick Start

### Prerequisites

- **Python 3.10+**
- **MongoDB** ([MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register) free tier works)
- **Polygon wallet** with USDC and POL/MATIC for gas
- **RPC endpoint** ([Infura](https://infura.io) or [Alchemy](https://www.alchemy.com) free tier)

### Installation

```bash
# Clone the repository
git clone https://github.com/thesSmartApe/polymarket-copy-trading-bot-python.git
cd polymarket-copy-trading-bot-python/python

# Install dependencies
pip install -r requirements.txt

# Run interactive setup wizard
python -m src.scripts.setup.setup

# Verify system status
python -m src.scripts.setup.system_status

# Start the copy trading bot
python -m src.main
```

📖 **Step-by-step guide:** [Getting Started](docs/GETTING_STARTED.md)

---

## Video Walkthrough

A **step-by-step video** on how to run the Polymarket Python copy trading bot is available. Check the repository or [releases](https://github.com/thesSmartApe/polymarket-copy-trading-bot-python/releases) for the walkthrough.

*To add your video link here: replace this paragraph with something like: **📹 [Watch: How to run the bot](YOUR_VIDEO_URL)**.*

---

## Other Editions

This is the **Python** edition. The same project is also available in:

| Edition | Repository | Description |
|--------|------------|-------------|
| **TypeScript** | [thesSmartApe/polymarket-copy-trading-bot](https://github.com/thesSmartApe/polymarket-copy-trading-bot) | Full-featured web dashboard, Node.js/TypeScript |
| **Python** | [thesSmartApe/polymarket-copy-trading-bot-python](https://github.com/thesSmartApe/polymarket-copy-trading-bot-python) | This repo — Python, CLI, same core logic |
| **Rust** | *(Rust edition when available)* | High-performance Rust implementation |

Use the edition that fits your stack; all aim to copy successful Polymarket traders with smart position sizing.

---

## Available Commands

### Setup & configuration
```bash
python -m src.scripts.setup.setup              # Interactive setup wizard
python -m src.scripts.setup.system_status      # Verify system status
python -m src.scripts.setup.help               # List all commands
```

### Main bot
```bash
python -m src.main                             # Start the copy trading bot
```

### Wallet
```bash
python -m src.scripts.wallet.check_proxy_wallet
python -m src.scripts.wallet.check_my_stats
python -m src.scripts.wallet.check_recent_activity
# ... see docs/COMMAND_REFERENCE.md for full list
```

### Research & simulation
```bash
python -m src.scripts.research.find_best_traders
python -m src.scripts.research.find_low_risk_traders
python -m src.scripts.simulation.simulate_profitability
# ... see docs/COMMAND_REFERENCE.md for full list
```

📖 **Full command list:** [Command Reference](docs/COMMAND_REFERENCE.md)

---

## Configuration

Create a `.env` file (or use the setup wizard). Essential variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `USER_ADDRESSES` | Traders to copy (comma-separated) | `'0xABC..., 0xDEF...'` |
| `PROXY_WALLET` | Your Polygon wallet | `'0x123...'` |
| `PRIVATE_KEY` | Wallet private key (no 0x) | `'abc123...'` |
| `MONGO_URI` | MongoDB connection string | `'mongodb+srv://...'` |
| `RPC_URL` | Polygon RPC | `'https://polygon...'` |
| `COPY_STRATEGY` | PERCENTAGE / FIXED / ADAPTIVE | `PERCENTAGE` |
| `COPY_SIZE` | Copy size (% or USD) | `10.0` |
| `TRADE_MULTIPLIER` | Position multiplier | `1.0` |
| `PREVIEW_MODE` | Simulate without trading | `false` |

See `.env.example` for all options. 📖 **Strategy details:** [Strategy Guide](docs/STRATEGY.md)

### Finding traders

1. Open [Polymarket Leaderboard](https://polymarket.com/leaderboard) or [Predictfolio](https://predictfolio.com).
2. Look for traders with strong P&L, win rate, and activity (e.g. [gabagool22](https://polymarket.com/@gabagool22?tab=activity)).
3. Copy their wallet addresses into `USER_ADDRESSES` in `.env`.

---

## Proof & Real Results

### User result

- **One user turned $200 into $800** using this bot by copying successful Polymarket traders. Results depend on trader selection, market conditions, and risk settings.

### Verified on-chain

The bot has been tested with real transactions on Polygon. See [Proof of Concept](docs/PROOF.md) for documented buy/sell examples and transaction hashes on PolygonScan.

---

## Features

| Feature | Description |
|---------|-------------|
| **Multi-trader support** | Copy several traders at once |
| **Smart position sizing** | Automatic scaling based on your capital |
| **Tiered multipliers** | Different multipliers by trade size |
| **Position tracking** | Tracks buys and sells across balance changes |
| **Trade aggregation** | Combine small trades into larger orders |
| **Real-time execution** | Sub-second monitoring and execution |
| **MongoDB** | Persistent trade and position history |
| **Preview mode** | Test without placing real orders |

---

## Project Structure (summary)

```
python/
├── .env, .env.example     # Configuration
├── requirements.txt       # Dependencies
├── src/
│   ├── main.py            # Entry point
│   ├── config/            # env, db, copy_strategy
│   ├── models/            # user_history (MongoDB)
│   ├── interfaces/        # Type definitions
│   ├── services/          # trade_monitor, trade_executor
│   ├── utils/             # logger, fetch_data, clob, post_order, etc.
│   └── scripts/           # setup, wallet, position, research, simulation
└── docs/                  # GETTING_STARTED, STRATEGY, COMMAND_REFERENCE, EXAMPLES, PROOF
```

---

## Safety & Disclaimers

- **Use at your own risk.** This bot executes real trades with real money.
- Start small and use **PREVIEW_MODE=true** to test without trading.
- Research traders before copying. Past performance does not guarantee future results.
- Use a dedicated wallet with limited funds and monitor the bot regularly.

**Best practices:** Dedicated wallet, only risk what you can afford to lose, diversify traders, run `python -m src.scripts.setup.system_status` before starting.

---

## Troubleshooting

| Issue | What to do |
|-------|------------|
| Missing env vars | Run `python -m src.scripts.setup.setup` |
| MongoDB connection failed | Check `MONGO_URI` and Atlas IP whitelist |
| Bot not detecting trades | Verify `USER_ADDRESSES` and recent trader activity |
| Insufficient balance | Add USDC and POL/MATIC for gas |
| Import errors | Run from project root: `python` from `python/` directory |

Run system check: `python -m src.scripts.setup.system_status`

---

## Documentation

| Doc | Description |
|-----|-------------|
| [Getting Started](docs/GETTING_STARTED.md) | Full setup and first run |
| [Strategy Guide](docs/STRATEGY.md) | Copy strategy and sizing |
| [Command Reference](docs/COMMAND_REFERENCE.md) | All commands |
| [Examples](docs/EXAMPLES.md) | Example workflows |
| [Proof](docs/PROOF.md) | On-chain proof and tx examples |

**Contact:** [Telegram @jerrix1](https://t.me/jerrix1)

---

## Contributing

1. Fork the repo
2. Create a branch (`git checkout -b feature/amazing-feature`)
3. Commit (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

ISC — see [LICENSE](LICENSE).

**Disclaimer:** For educational use. Trading involves risk of loss. Developers are not responsible for financial losses from using this bot.
