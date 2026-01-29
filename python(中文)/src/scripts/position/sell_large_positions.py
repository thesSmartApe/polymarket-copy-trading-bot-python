#!/usr/bin/env python3
"""
Sell large positions
"""
import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from colorama import init, Fore, Style
from src.config.env import ENV

init(autoreset=True)


async def sell_large_positions():
    """
    Sell large positions
    
    This script identifies and sells positions above a certain value threshold.
    """
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Selling Large Positions")
    print()
    
    # Get threshold from user or use default
    threshold_input = input(f"Minimum position value to sell (default: $1000): ").strip()
    threshold = float(threshold_input) if threshold_input else 1000.0
    
    print()
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Fetching positions...")
    
    try:
        wallet = ENV.PROXY_WALLET
        url = f'https://data-api.polymarket.com/positions?user={wallet}'
        
        from src.utils.fetch_data import fetch_data_async
        positions = await fetch_data_async(url)
        
        if not isinstance(positions, list):
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Failed to fetch positions")
            return
        
        # Filter large positions
        large_positions = [
            p for p in positions
            if p.get('currentValue', 0) >= threshold
        ]
        
        if not large_positions:
            print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} No positions found above ${threshold}")
            return
        
        print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Found {len(large_positions)} large positions:")
        for pos in large_positions:
            print(f"  - {pos.get('title', 'Unknown')}: ${pos.get('currentValue', 0):.2f}")
        
        print()
        print(f"{Fore.YELLOW}[NOTE]{Style.RESET_ALL} CLOB client implementation is required to execute sells")
        print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} See src/utils/create_clob_client.py for implementation")
        
        # TODO: When CLOB client is ready:
        # 1. For each large position, create sell order
        # 2. Post orders via CLOB client
        # 3. Report results
        
    except Exception as e:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Failed to process positions: {e}")


if __name__ == '__main__':
    asyncio.run(sell_large_positions())

