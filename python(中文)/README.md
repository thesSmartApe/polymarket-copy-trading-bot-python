# Polymarket 跟单交易机器人 - Python 版本

> 用于 Polymarket 的自动化跟单交易机器人，可智能调整仓位大小并实时执行，镜像顶级交易者的交易。

[![License: ISC](https://img.shields.io/badge/License-ISC-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-%3E%3D3.10-brightgreen.svg)](https://www.python.org/)

## 概述

这是 Polymarket 跟单交易机器人的 Python 版本。它会自动复制成功 Polymarket 交易者的交易到您的钱包。它 24/7 监控交易者活动，根据您的资金计算比例仓位大小，并实时执行匹配订单。

### 工作原理

1. **选择交易者** - 从 [Polymarket 排行榜](https://polymarket.com/leaderboard) 或 [Predictfolio](https://predictfolio.com) 选择顶级表现者
2. **监控活动** - 机器人使用 Polymarket 数据 API 持续监控选定交易者新开的仓位
3. **计算大小** - 根据您的余额与交易者余额自动缩放交易
4. **执行订单** - 使用您的钱包在 Polymarket 上放置匹配订单
5. **跟踪表现** - 在 MongoDB 中维护完整的交易历史

## 快速开始

### 先决条件

- Python 3.10+
- MongoDB 数据库（[MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register) 免费版可用）
- 带有 USDC 和 POL/MATIC 用于 gas 的 Polygon 钱包
- RPC 端点（[Infura](https://infura.io) 或 [Alchemy](https://www.alchemy.com) 免费版）

### 安装

```bash
# 克隆仓库
git clone https://github.com/thesSmartApe/polymarket-copy-trading-bot-python.git
cd polymarket-copy-trading-bot-python/python

# 安装依赖
pip install -r requirements.txt

# 运行交互式设置向导
python -m src.scripts.setup.setup

# 验证系统状态
python -m src.scripts.setup.system_status

# 启动交易机器人
python -m src.main
```

📖 **详细设置说明，请参阅 [入门指南](docs/GETTING_STARTED.md)**

## 可用命令

### 设置和配置
```bash
python -m src.scripts.setup.setup              # 交互式设置向导
python -m src.scripts.setup.system_status       # 验证系统状态和配置
python -m src.scripts.setup.help              # 显示所有可用命令
```

### 主机器人
```bash
python -m src.main                       # 启动跟单交易机器人
```

### 钱包管理
```bash
python -m src.scripts.wallet.check_proxy_wallet        # 检查代理和主钱包活动
python -m src.scripts.wallet.check_both_wallets        # 比较两个钱包地址
python -m src.scripts.wallet.check_my_stats            # 查看钱包统计信息
python -m src.scripts.wallet.check_recent_activity     # 检查最近的交易活动
python -m src.scripts.wallet.check_positions_detailed  # 查看详细的仓位信息
python -m src.scripts.wallet.check_pnl_discrepancy     # 检查盈亏差异分析
python -m src.scripts.wallet.verify_allowance         # 验证 USDC 代币授权
python -m src.scripts.wallet.check_allowance          # 检查并设置 USDC 授权
python -m src.scripts.wallet.set_token_allowance      # 设置 ERC1155 代币授权
python -m src.scripts.wallet.find_my_eoa              # 查找和分析 EOA 钱包
python -m src.scripts.wallet.find_gnosis_safe_proxy   # 查找 Gnosis Safe 代理钱包
```

### 仓位管理（⚠️ 需要完整的 CLOB 客户端实现）
```bash
# 注意：这些脚本存在但需要完整的 CLOB 客户端实现
python -m src.scripts.position.manual_sell            # 手动卖出特定仓位
python -m src.scripts.position.sell_large_positions   # 卖出大仓位
python -m src.scripts.position.close_stale_positions # 关闭过期/旧仓位
python -m src.scripts.position.close_resolved_positions # 关闭已结算仓位
python -m src.scripts.position.redeem_resolved_positions # 赎回已结算仓位
```

### 交易者研究和分析
```bash
python -m src.scripts.research.find_best_traders      # 查找表现最佳的交易者
python -m src.scripts.research.find_low_risk_traders  # 查找具有良好指标的低风险交易者
python -m src.scripts.research.scan_best_traders      # 扫描和分析顶级交易者
python -m src.scripts.research.scan_traders_from_markets # 从活跃市场扫描交易者
```

### 模拟和回测
```bash
python -m src.scripts.simulation.simulate_profitability # 模拟交易者的盈利能力
python -m src.scripts.simulation.simulate_profitability_old # 旧模拟逻辑
python -m src.scripts.simulation.run_simulations        # 运行综合批量模拟
python -m src.scripts.simulation.compare_results        # 比较模拟结果
python -m src.scripts.simulation.aggregate_results      # 汇总跨策略的交易结果
python -m src.scripts.simulation.audit_copy_trading     # 审计跟单交易算法
python -m src.scripts.simulation.fetch_historical_trades # 获取并缓存历史交易数据
```

## 配置

### 基本变量

创建 `.env` 文件，包含以下变量：

| 变量 | 描述 | 示例 |
|----------|-------------|---------|
| `USER_ADDRESSES` | 要复制的交易者（逗号分隔） | `'0xABC..., 0xDEF...'` |
| `PROXY_WALLET` | 您的 Polygon 钱包地址 | `'0x123...'` |
| `PRIVATE_KEY` | 钱包私钥（无 0x 前缀） | `'abc123...'` |
| `MONGO_URI` | MongoDB 连接字符串 | `'mongodb+srv://...'` |
| `RPC_URL` | Polygon RPC 端点 | `'https://polygon...'` |
| `USDC_CONTRACT_ADDRESS` | Polygon 上的 USDC 合约 | `'0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'` |
| `CLOB_HTTP_URL` | Polymarket CLOB API URL | `'https://clob.polymarket.com'` |
| `TRADE_MULTIPLIER` | 仓位大小倍数（默认：1.0） | `2.0` |
| `FETCH_INTERVAL` | 检查间隔（秒，默认：1） | `1` |
| `TRADE_AGGREGATION_ENABLED` | 启用交易聚合（默认：false） | `true` |
| `TRADE_AGGREGATION_WINDOW_SECONDS` | 聚合窗口（默认：30） | `30` |

### 查找交易者

1. 访问 [Polymarket 排行榜](https://polymarket.com/leaderboard)
2. 寻找具有正盈亏、胜率 >55% 和活跃交易历史的交易者
3. 在 [Predictfolio](https://predictfolio.com) 上验证详细统计
4. 将钱包地址添加到 `.env` 中的 `USER_ADDRESSES`

## ✅ 概念验证

该机器人已在 Polygon 上通过真实交易成功测试和验证。以下是显示机器人从目标钱包复制交易到代理钱包的文档示例。

### 视频演示

📹 **[观看机器人运行](../python-copy-trading-bot.mp4)** - Python 机器人实时监控和复制交易的视频演示。

### 真实交易示例

#### 配置
- **目标钱包（被复制的交易者）：** `0xEb55A1A899594B5b9C406FfA493775Feab54d5e9`
- **代理钱包（机器人钱包）：** `0x2108FF2b299800B7a904BD36A7cEd1c4Db5F47dC`

#### 买入交易示例

**目标买入交易：**
- **交易哈希：** [`0x39b3bebdc377f12f116e6a43ed6157e6da2bc17cbb0f8cea63ce6992dd5a0d5e`](https://polygonscan.com/tx/0x39b3bebdc377f12f116e6a43ed6157e6da2bc17cbb0f8cea63ce6992dd5a0d5e)
- **来自：** 目标钱包 (`0xEb55A1A8...eab54d5e9`)
- **操作：** 在 Polymarket 上执行买入订单

**复制买入交易（机器人）：**
- **交易哈希：** [`0xa2e7abc0e35e2a7ed275c958209d34686fa87d7b186c8264334f8cbab1eca35d`](https://polygonscan.com/tx/0xa2e7abc0e35e2a7ed275c958209d34686fa87d7b186c8264334f8cbab1eca35d)
- **来自：** 代理钱包 (`0x2108FF2b...Db5F47dC`)
- **操作：** 机器人自动复制买入订单，按比例调整大小

#### 卖出交易示例

**目标卖出交易：**
- **交易哈希：** [`0xbbf1fa775c7c3ebcf65edf41117964c447b0bcb23864915a90e560f9f2459eb0`](https://polygonscan.com/tx/0xbbf1fa775c7c3ebcf65edf41117964c447b0bcb23864915a90e560f9f2459eb0)
- **来自：** 目标钱包 (`0xEb55A1A8...eab54d5e9`)
- **操作：** 在 Polymarket 上执行卖出订单
- **详情：** 转移 1,690,000 ERC-1155 代币，收到 0.676 USDC

**复制卖出交易（机器人）：**
- **交易哈希：** [`0x5fd83404750e5212d6491705a85a5659cc0111dea710c790879f6aed7bf5e2e7`](https://polygonscan.com/tx/0x5fd83404750e5212d6491705a85a5659cc0111dea710c790879f6aed7bf5e2e7)
- **来自：** 代理钱包 (`0x2108FF2b...Db5F47dC`)
- **操作：** 机器人自动复制卖出订单，按比例调整大小

### 验证

这些交易证明了：
- ✅ 实时交易检测和复制
- ✅ 基于资金比例的比例仓位大小
- ✅ 自动执行买入和卖出订单
- ✅ 成功集成 Polymarket 的 CLOB 交易所
- ✅ 在目标交易的 1 个区块内执行交易

所有交易都可以使用上面提供的交易哈希在 [PolygonScan](https://polygonscan.com) 上验证。

## 功能

- **多交易者支持** - 同时跟踪和复制多个交易者的交易
- **智能仓位大小** - 根据您的资金自动调整交易大小
- **分层倍数** - 根据交易大小应用不同的倍数
- **仓位跟踪** - 即使在余额变化后也能准确跟踪买入和卖出
- **交易聚合** - 将多个小交易合并为更大的可执行订单
- **实时执行** - 每秒监控交易并立即执行
- **MongoDB 集成** - 持久存储所有交易和仓位
- **价格保护** - 内置滑点检查以避免不利成交
- **彩色日志** - 美观的彩色控制台输出，便于监控

## 项目结构

```
polymarket-copy-trading-bot/
│
├── 📄 配置文件
│   ├── .env                    # 环境变量（通过设置创建）
│   ├── .env.example            # 示例环境文件
│   ├── requirements.txt        # Python 依赖
│   ├── pyproject.toml          # Python 项目元数据
│   ├── package.json            # 遗留引用（Python 项目）
│   └── docker-compose.yml      # Docker 配置
│
├── 📚 文档
│   ├── README.md               # 主要文档
│   ├── README_PYTHON.md        # 此文件 - Python 特定文档
│   ├── PYTHON_SCRIPTS_STATUS.md # 脚本转换状态
│   ├── PROJECT_STRUCTURE.md    # 详细项目结构
│   └── docs/                   # 其他文档
│       ├── GETTING_STARTED.md
│       ├── QUICK_START.md
│       ├── SIMULATION_GUIDE.md
│       └── ...
│
├── 🐍 源代码
│   └── src/
│       │
│       ├── 🚀 入口点
│       │   └── main.py                    # 主机器人入口点
│       │
│       ├── ⚙️ 配置
│       │   └── config/
│       │       ├── __init__.py
│       │       ├── env.py                 # 环境变量加载和验证
│       │       ├── db.py                  # MongoDB 连接管理
│       │       └── copy_strategy.py        # 跟单交易策略逻辑
│       │
│       ├── 📊 数据模型
│       │   └── models/
│       │       ├── __init__.py
│       │       └── user_history.py         # 用户活动和仓位的 MongoDB 模型
│       │
│       ├── 🔌 类型定义
│       │   └── interfaces/
│       │       ├── __init__.py
│       │       └── user.py                 # 类型定义（UserActivity, UserPosition）
│       │
│       ├── 🔄 核心服务
│       │   └── services/
│       │       ├── __init__.py
│       │       ├── trade_monitor.py        # 监控交易者活动（RTDS/API 轮询）
│       │       └── trade_executor.py       # 基于监控活动执行交易
│       │
│       ├── 🛠️ 工具
│       │   └── utils/
│       │       ├── __init__.py
│       │       ├── __main__.py
│       │       ├── logger.py               # 彩色日志和控制台输出
│       │       ├── fetch_data.py           # 带重试逻辑的 HTTP 请求
│       │       ├── get_my_balance.py       # 从区块链获取 USDC 余额
│       │       ├── create_clob_client.py   # 创建 Polymarket CLOB 客户端
│       │       ├── post_order.py           # 计算并向 Polymarket 提交订单
│       │       └── system_status.py        # 系统状态和诊断
│       │
│       └── 📜 管理脚本
│           └── scripts/
│               ├── __init__.py
│               ├── __main__.py
│               │
│               └── 注意：所有脚本都位于 `src/scripts/` 中。
│                   下面的组织是按类别的逻辑分组。
│               │
│               ├── 🔧 设置和配置 (setup/)
│               │   ├── setup.py                  # 交互式设置向导
│               │   ├── system_status.py          # 验证系统状态和连接
│               │   └── help.py                   # 显示所有可用命令
│               │
│               ├── 💰 钱包管理 (wallet/)
│               │   ├── check_proxy_wallet.py     # 检查代理和主钱包
│               │   ├── check_both_wallets.py     # 比较两个钱包
│               │   ├── check_my_stats.py         # 查看钱包统计信息
│               │   ├── check_recent_activity.py  # 检查最近的交易活动
│               │   ├── check_positions_detailed.py # 查看详细仓位
│               │   ├── check_pnl_discrepancy.py  # 盈亏差异分析
│               │   ├── verify_allowance.py       # 验证 USDC 授权
│               │   ├── check_allowance.py         # 检查并设置 USDC 授权
│               │   ├── set_token_allowance.py    # 设置 ERC1155 代币授权
│               │   ├── find_my_eoa.py            # 查找和分析 EOA 钱包
│               │   └── find_gnosis_safe_proxy.py # 查找 Gnosis Safe 代理
│               │
│               ├── 📊 仓位管理 (position/)
│               │   ├── manual_sell.py           # 手动卖出仓位
│               │   ├── sell_large_positions.py   # 卖出大仓位
│               │   ├── close_stale_positions.py  # 关闭过期仓位
│               │   ├── close_resolved_positions.py # 关闭已结算仓位
│               │   └── redeem_resolved_positions.py # 赎回已结算仓位
│               │   ⚠️  注意：需要完整的 CLOB 客户端实现
│               │
│               ├── 🔍 交易者研究 (research/)
│               │   ├── find_best_traders.py      # 查找表现最佳的交易者
│               │   ├── find_low_risk_traders.py  # 查找低风险交易者
│               │   ├── scan_best_traders.py      # 扫描和分析顶级交易者
│               │   └── scan_traders_from_markets.py # 从市场扫描交易者
│               │
│               └── 📈 模拟和分析 (simulation/)
│                   ├── simulate_profitability.py # 模拟盈利能力
│                   ├── simulate_profitability_old.py # 旧模拟逻辑
│                   ├── run_simulations.py        # 运行批量模拟
│                   ├── compare_results.py        # 比较模拟结果
│                   ├── aggregate_results.py      # 汇总交易结果
│                   ├── audit_copy_trading.py      # 审计跟单交易算法
│                   └── fetch_historical_trades.py # 获取历史交易数据
│
├── 📁 运行时目录
│   ├── logs/                    # 应用程序日志（自动创建）
│   │   └── bot-YYYY-MM-DD.log  # 每日日志文件
│   │
│   ├── trader_data_cache/       # 缓存的交易者数据（自动创建）
│   │   └── {address}_{days}d_{date}.json
│   │
│   ├── simulation_results/      # 模拟结果（自动创建）
│   │   └── {strategy}_{trader}_{date}.json
│   │
│   ├── audit_results/           # 审计报告（自动创建）
│   │   └── audit_{timestamp}.json
│   │
│   └── strategy_factory_results/ # 策略分析结果（自动创建）
│       └── aggregated_results.json
│
└── 🐳 部署
    ├── Dockerfile               # Docker 镜像定义
    └── docker-compose.yml       # Docker Compose 配置
```

### 目录角色

#### **配置 (`src/config/`)**
- **env.py**: 从 `.env` 文件加载和验证环境变量
- **db.py**: 管理 MongoDB 连接、数据库提取和连接生命周期
- **copy_strategy.py**: 实现跟单交易逻辑（仓位大小、倍数、限制）

#### **数据模型 (`src/models/`)**
- **user_history.py**: 用于存储用户交易活动和仓位的 MongoDB 集合和模型

#### **类型定义 (`src/interfaces/`)**
- **user.py**: UserActivity 和 UserPosition 接口的类型定义

#### **核心服务 (`src/services/`)**
- **trade_monitor.py**: 通过 RTDS WebSocket 或 API 轮询监控交易者活动
- **trade_executor.py**: 基于监控活动执行交易，支持聚合

#### **工具 (`src/utils/`)**
- **logger.py**: 各种日志级别的彩色控制台日志
- **fetch_data.py**: 带重试逻辑和错误处理的异步 HTTP 请求
- **get_my_balance.py**: 从 Polygon 区块链获取 USDC 余额
- **create_clob_client.py**: 创建和配置 Polymarket CLOB 客户端（需要完整实现）
- **post_order.py**: 计算订单大小并向 Polymarket 提交订单
- **system_status.py**: 系统状态和诊断工具

#### **管理脚本 (`src/scripts/`)**

**设置和配置：**
- **setup.py**: 初始配置的交互式设置向导
- **system_status.py**: 验证系统状态、连接和配置
- **help.py**: 显示所有可用命令和使用信息

**钱包管理：**
- **check_proxy_wallet.py**: 检查代理钱包余额和仓位
- **check_both_wallets.py**: 比较两个钱包地址
- **check_my_stats.py**: 查看交易统计信息
- **check_recent_activity.py**: 查看最近的交易活动
- **check_positions_detailed.py**: 查看详细的仓位信息
- **check_pnl_discrepancy.py**: 检查盈亏差异分析
- **verify_allowance.py**: 验证 USDC 代币授权
- **check_allowance.py**: 检查并设置 USDC 授权
- **set_token_allowance.py**: 设置 ERC1155 代币授权
- **find_my_eoa.py**: 查找和分析 EOA 钱包
- **find_gnosis_safe_proxy.py**: 查找 Gnosis Safe 代理钱包

**仓位管理：**
- **manual_sell.py**: 手动卖出特定仓位
- **sell_large_positions.py**: 卖出大仓位
- **close_stale_positions.py**: 关闭过期/旧仓位
- **close_resolved_positions.py**: 关闭已结算仓位
- **redeem_resolved_positions.py**: 赎回已结算仓位
- ⚠️ **注意**：这些需要完整的 CLOB 客户端实现

**交易者研究：**
- **find_best_traders.py**: 按 ROI 和指标查找表现最佳的交易者
- **find_low_risk_traders.py**: 查找具有良好风险指标的低风险交易者
- **scan_best_traders.py**: 从市场扫描和分析顶级交易者
- **scan_traders_from_markets.py**: 从活跃市场扫描交易者

**模拟和分析：**
- **simulate_profitability.py**: 模拟交易者的盈利能力
- **simulate_profitability_old.py**: 旧模拟逻辑（遗留算法）
- **run_simulations.py**: 使用预设运行综合批量模拟
- **compare_results.py**: 并排比较模拟结果
- **aggregate_results.py**: 汇总跨策略的交易结果
- **audit_copy_trading.py**: 审计跟单交易算法性能
- **fetch_historical_trades.py**: 获取并缓存历史交易数据

#### **入口点 (`src/main.py`)**
- 初始化服务并处理优雅关闭的主应用程序入口点

## 与 TypeScript 版本的主要区别

- **Async/Await**: Python 使用 `asyncio` 进行异步操作
- **类型系统**: Python 使用类型提示而不是 TypeScript 类型
- **MongoDB**: 使用 `pymongo` 而不是 `mongoose`
- **Web3**: 使用 `web3.py` 而不是 `ethers.js`
- **HTTP 客户端**: 使用 `httpx` 而不是 `axios`
- **日志**: 使用 `colorama` 进行彩色输出
- **包管理**: 使用 `pip` 和 `requirements.txt` 而不是 `npm` 和 `package.json`

## 重要说明

### CLOB 客户端实现

Polymarket CLOB（中央限价订单簿）客户端是一个关键组件，需要完整实现。当前的 Python 版本包含一个占位符结构。对于生产使用，您有两个选择：

1. **通过子进程使用 JavaScript SDK**（目前推荐）
   - 安装 Node.js 和 `@polymarket/clob-client` 包
   - 创建一个从 Python 调用 JS SDK 的桥接脚本

2. **实现完整的 Python CLOB 客户端**
   - 这需要实现 Polymarket 的订单签名协议
   - 有关 API 详细信息，请参阅 Polymarket 文档
   - 结构位于 `src/utils/create_clob_client.py`

## 安全和风险管理

⚠️ **重要免责声明：**

- **使用风险自负** - 此机器人使用真实资金执行真实交易
- **从小开始** - 在扩大规模之前使用最少的资金进行测试
- **分散投资** - 不要只复制一个交易者；跟踪多种策略
- **定期监控** - 每天检查机器人日志以确保正确执行
- **不保证** - 过去的表现不能保证未来的结果

### 最佳实践

1. 使用与主要资金分开的专用钱包
2. 只分配您能承受损失的资金
3. 在复制之前彻底研究交易者
4. 设置监控和警报
5. 知道如何快速停止机器人（Ctrl+C）
6. 启动前运行系统状态检查：`python -m src.scripts.setup.system_status`

## 故障排除

### 常见问题

**缺少环境变量** → 运行 `python -m src.scripts.setup.setup` 创建 `.env` 文件

**MongoDB 连接失败** → 验证 `MONGO_URI`，在 MongoDB Atlas 中白名单 IP

**机器人未检测到交易** → 验证交易者地址并检查最近的活动

**余额不足** → 向钱包添加 USDC 并确保有 POL/MATIC 用于 gas 费用

**CLOB 客户端错误** → CLOB 客户端需要完整实现（请参阅上面的重要说明）

**导入错误** → 确保您从项目根目录运行

**运行系统状态检查：** `python -m src.scripts.setup.system_status`

## 开发

### 运行测试

```bash
# 运行测试（实现后）
pytest
```

### 代码风格

此项目遵循 PEP 8 风格指南。考虑使用：
- `black` 进行代码格式化
- `flake8` 或 `pylint` 进行代码检查
- `mypy` 进行类型检查

### 依赖

关键 Python 包：
- `web3` - 以太坊/Polygon 区块链交互
- `pymongo` - MongoDB 数据库操作
- `httpx` - 异步 HTTP 客户端
- `colorama` - 跨平台彩色终端输出
- `python-dotenv` - 环境变量管理
- `asyncio` - 异步编程（内置）
- `websockets` - RTDS 的 WebSocket 客户端

完整列表请参阅 `requirements.txt`。

## 贡献

欢迎贡献！请：

1. Fork 仓库
2. 创建功能分支（`git checkout -b feature/amazing-feature`）
3. 提交更改（`git commit -m 'Add amazing feature'`）
4. 推送到分支（`git push origin feature/amazing-feature`）
5. 打开 Pull Request

## 许可证

ISC 许可证 - 详细信息请参阅 [LICENSE](LICENSE) 文件。

## 致谢

- 基于 [Polymarket CLOB 客户端](https://github.com/Polymarket/clob-client)（JavaScript SDK）构建
- 使用 [Predictfolio](https://predictfolio.com) 进行交易者分析
- 由 Polygon 网络提供支持

---

**免责声明：** 本软件仅供教育用途。交易涉及损失风险。开发人员不对使用此机器人时产生的任何财务损失负责。

**注意：** 此 Python 版本是从原始 TypeScript 版本完全转换而来。所有 TypeScript 文件已删除。对于生产使用，请确保 CLOB 客户端完全实现或使用 JavaScript SDK 桥接。

**📊 转换状态：** 有关已转换脚本及其状态的完整列表，请参阅 [PYTHON_SCRIPTS_STATUS.md](./PYTHON_SCRIPTS_STATUS.md)。

**📁 项目结构：** 有关按角色组织的详细文件和文件夹，请参阅 [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)。

## 文档

`docs/` 目录中提供了全面的文档：

- **[入门指南](docs/GETTING_STARTED.md)** - 完整的逐步设置和首次运行
- **[策略指南](docs/STRATEGY.md)** ⭐ - 了解跟单交易策略和配置
- **[命令参考](docs/COMMAND_REFERENCE.md)** - 所有命令的详细参考
- **[使用示例](docs/EXAMPLES.md)** - 常见任务的实用示例

### 快速链接

- 🚀 [入门](docs/GETTING_STARTED.md) - 首次设置请从这里开始
- 📊 [策略指南](docs/STRATEGY.md) - 了解机器人工作原理并配置策略
- 📖 [命令参考](docs/COMMAND_REFERENCE.md) - 所有可用命令说明
- 💡 [示例](docs/EXAMPLES.md) - 实际使用示例
- 📁 [项目结构](PROJECT_STRUCTURE.md) - 文件组织
- 📊 [脚本状态](PYTHON_SCRIPTS_STATUS.md) - 转换状态
