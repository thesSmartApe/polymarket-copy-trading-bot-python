"""
Create Polymarket CLOB client
Note: This is a simplified wrapper. For full functionality, you may need to use
the JavaScript SDK via subprocess or implement the full Python API client.
"""
from typing import Optional, Dict, Any
from web3 import Web3
from eth_account import Account
from ..config.env import ENV
from ..utils.logger import info, error


async def is_gnosis_safe(address: str) -> bool:
    """Determines if a wallet is a Gnosis Safe by checking if it has contract code"""
    try:
        w3 = Web3(Web3.HTTPProvider(ENV.RPC_URL))
        # Convert address to checksum format for web3.py
        checksum_address = Web3.to_checksum_address(address)
        code = w3.eth.get_code(checksum_address)
        # If code is not "0x", then it's a contract (likely Gnosis Safe)
        return code != b'0x'
    except Exception as e:
        error(f'Error checking wallet type: {e}')
        return False


class ClobClient:
    """Simplified Polymarket CLOB client wrapper"""
    
    def __init__(
        self,
        host: str,
        chain_id: int,
        wallet: Any,
        api_creds: Optional[Dict[str, Any]] = None,
        signature_type: str = 'EOA',
        proxy_wallet: Optional[str] = None
    ):
        self.host = host.rstrip('/')
        self.chain_id = chain_id
        self.wallet = wallet
        self.api_creds = api_creds or {}
        self.signature_type = signature_type
        self.proxy_wallet = proxy_wallet
        self.api_key = api_creds.get('key') if api_creds else None
        self.api_secret = api_creds.get('secret') if api_creds else None
        self.api_passphrase = api_creds.get('passphrase') if api_creds else None
    
    async def create_api_key(self) -> Dict[str, Any]:
        """Create API key - placeholder, needs implementation"""
        # This would need to call the Polymarket API to create keys
        # For now, return empty dict
        return {}
    
    async def derive_api_key(self) -> Dict[str, Any]:
        """Derive API key - placeholder, needs implementation"""
        # This would need to call the Polymarket API to derive keys
        # For now, return empty dict
        return {}
    
    async def get_order_book(self, token_id: str) -> Dict[str, Any]:
        """Get order book for a token"""
        import httpx
        url = f'{self.host}/book?token_id={token_id}'
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    
    async def create_market_order(self, order_args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a market order - placeholder, needs full implementation"""
        # This needs to create and sign an order according to Polymarket's format
        # For now, return a placeholder
        return {
            'side': order_args.get('side'),
            'tokenID': order_args.get('tokenID'),
            'amount': order_args.get('amount'),
            'price': order_args.get('price'),
        }
    
    async def post_order(self, signed_order: Dict[str, Any], order_type: str) -> Dict[str, Any]:
        """Post order to Polymarket - placeholder, needs full implementation"""
        # This needs to post the signed order to Polymarket's API
        # For now, return a placeholder response
        return {'success': False, 'error': 'Not implemented - requires full CLOB client implementation'}


async def create_clob_client() -> ClobClient:
    """Create and initialize CLOB client"""
    chain_id = 137  # Polygon
    host = ENV.CLOB_HTTP_URL
    
    # Create wallet from private key
    account = Account.from_key(ENV.PRIVATE_KEY)
    
    # Detect if the proxy wallet is a Gnosis Safe or EOA
    is_proxy_safe = await is_gnosis_safe(ENV.PROXY_WALLET)
    signature_type = 'POLY_GNOSIS_SAFE' if is_proxy_safe else 'EOA'
    
    info(
        f'Wallet type detected: {"Gnosis Safe" if is_proxy_safe else "EOA (Externally Owned Account)"}'
    )
    
    # Create initial client
    clob_client = ClobClient(
        host=host,
        chain_id=chain_id,
        wallet=account,
        signature_type=signature_type,
        proxy_wallet=ENV.PROXY_WALLET if is_proxy_safe else None
    )
    
    # Try to create or derive API key
    try:
        creds = await clob_client.create_api_key()
        if not creds.get('key'):
            creds = await clob_client.derive_api_key()
    except Exception as e:
        error(f'Failed to create/derive API key: {e}')
        creds = {}
    
    # Create client with credentials
    clob_client = ClobClient(
        host=host,
        chain_id=chain_id,
        wallet=account,
        api_creds=creds,
        signature_type=signature_type,
        proxy_wallet=ENV.PROXY_WALLET if is_proxy_safe else None
    )
    
    return clob_client

