"""
Post order to Polymarket
"""
from typing import Optional, Dict, Any
from ..config.env import ENV
from ..models.user_history import get_user_activity_collection
from ..utils.logger import info, warning, order_result
from ..config.copy_strategy import calculate_order_size, get_trade_multiplier

RETRY_LIMIT = ENV.RETRY_LIMIT
COPY_STRATEGY_CONFIG = ENV.COPY_STRATEGY_CONFIG

# Polymarket minimum order sizes
MIN_ORDER_SIZE_USD = 1.0  # Minimum order size in USD for BUY orders
MIN_ORDER_SIZE_TOKENS = 1.0  # Minimum order size in tokens for SELL/MERGE orders


def extract_order_error(response: Any) -> Optional[str]:
    """Extract error message from order response"""
    if not response:
        return None
    
    if isinstance(response, str):
        return response
    
    if isinstance(response, dict):
        # Check direct error
        if 'error' in response:
            error_val = response['error']
            if isinstance(error_val, str):
                return error_val
            if isinstance(error_val, dict):
                if 'error' in error_val:
                    return error_val['error']
                if 'message' in error_val:
                    return error_val['message']
        
        # Check other error fields
        if 'errorMsg' in response:
            return response['errorMsg']
        if 'message' in response:
            return response['message']
    
    return None


def is_insufficient_balance_or_allowance_error(message: Optional[str]) -> bool:
    """Check if error is related to insufficient balance or allowance"""
    if not message:
        return False
    lower = message.lower()
    return 'not enough balance' in lower or 'allowance' in lower


async def post_order(
    clob_client: Any,
    condition: str,
    my_position: Optional[Dict[str, Any]],
    user_position: Optional[Dict[str, Any]],
    trade: Dict[str, Any],
    my_balance: float,
    user_balance: float,
    user_address: str
):
    """Post order to Polymarket"""
    collection = get_user_activity_collection(user_address)
    
    if condition == 'merge':
        info('Executing MERGE strategy...')
        if not my_position:
            warning('No position to merge')
            collection.update_one({'_id': trade['_id']}, {'$set': {'bot': True}})
            return
        
        remaining = my_position.get('size', 0)
        
        # Check minimum order size
        if remaining < MIN_ORDER_SIZE_TOKENS:
            warning(f'Position size ({remaining:.2f} tokens) too small to merge - skipping')
            collection.update_one({'_id': trade['_id']}, {'$set': {'bot': True}})
            return
        
        retry = 0
        abort_due_to_funds = False
        
        while remaining > 0 and retry < RETRY_LIMIT:
            try:
                order_book = await clob_client.get_order_book(trade['asset'])
                if not order_book.get('bids') or len(order_book['bids']) == 0:
                    warning('No bids available in order book')
                    collection.update_one({'_id': trade['_id']}, {'$set': {'bot': True}})
                    break
                
                max_price_bid = max(order_book['bids'], key=lambda x: float(x['price']))
                
                info(f'Best bid: {max_price_bid["size"]} @ ${max_price_bid["price"]}')
                
                if remaining <= float(max_price_bid['size']):
                    order_args = {
                        'side': 'SELL',
                        'tokenID': my_position['asset'],
                        'amount': remaining,
                        'price': float(max_price_bid['price']),
                    }
                else:
                    order_args = {
                        'side': 'SELL',
                        'tokenID': my_position['asset'],
                        'amount': float(max_price_bid['size']),
                        'price': float(max_price_bid['price']),
                    }
                
                signed_order = await clob_client.create_market_order(order_args)
                resp = await clob_client.post_order(signed_order, 'FOK')
                
                if resp.get('success') is True:
                    retry = 0
                    order_result(True, f'Sold {order_args["amount"]} tokens at ${order_args["price"]}')
                    remaining -= order_args['amount']
                else:
                    error_message = extract_order_error(resp)
                    if is_insufficient_balance_or_allowance_error(error_message):
                        abort_due_to_funds = True
                        warning(f'Order rejected: {error_message or "Insufficient balance or allowance"}')
                        warning('Skipping remaining attempts. Top up funds or check allowance before retrying.')
                        break
                    retry += 1
                    warning(f'Order failed (attempt {retry}/{RETRY_LIMIT}){f" - {error_message}" if error_message else ""}')
            except Exception as e:
                retry += 1
                warning(f'Order error (attempt {retry}/{RETRY_LIMIT}): {e}')
        
        if abort_due_to_funds:
            collection.update_one(
                {'_id': trade['_id']},
                {'$set': {'bot': True, 'botExcutedTime': RETRY_LIMIT}}
            )
            return
        
        if retry >= RETRY_LIMIT:
            collection.update_one(
                {'_id': trade['_id']},
                {'$set': {'bot': True, 'botExcutedTime': retry}}
            )
        else:
            collection.update_one({'_id': trade['_id']}, {'$set': {'bot': True}})
    
    elif condition == 'buy':
        info('Executing BUY strategy...')
        
        info(f'Your balance: ${my_balance:.2f}')
        info(f'Trader bought: ${trade.get("usdcSize", 0):.2f}')
        
        # Get current position size for position limit checks
        current_position_value = (my_position.get('size', 0) * my_position.get('avgPrice', 0)) if my_position else 0
        
        # Use new copy strategy system
        order_calc = calculate_order_size(
            COPY_STRATEGY_CONFIG,
            trade.get('usdcSize', 0),
            my_balance,
            current_position_value
        )
        
        # Log the calculation reasoning
        info(f'{order_calc.reasoning}')
        
        # Check if order should be executed
        if order_calc.final_amount == 0:
            warning(f'Cannot execute: {order_calc.reasoning}')
            if order_calc.below_minimum:
                warning('Increase COPY_SIZE or wait for larger trades')
            collection.update_one({'_id': trade['_id']}, {'$set': {'bot': True}})
            return
        
        remaining = order_calc.final_amount
        available_balance = my_balance  # Track remaining balance after orders
        
        retry = 0
        abort_due_to_funds = False
        total_bought_tokens = 0  # Track total tokens bought for this trade
        
        while remaining > 0 and retry < RETRY_LIMIT:
            try:
                order_book = await clob_client.get_order_book(trade['asset'])
                if not order_book.get('asks') or len(order_book['asks']) == 0:
                    warning('No asks available in order book')
                    collection.update_one({'_id': trade['_id']}, {'$set': {'bot': True}})
                    break
                
                min_price_ask = min(order_book['asks'], key=lambda x: float(x['price']))
                
                info(f'Best ask: {min_price_ask["size"]} @ ${min_price_ask["price"]}')
                
                # Check if remaining amount is below minimum before creating order
                if remaining < MIN_ORDER_SIZE_USD:
                    info(f'Remaining amount (${remaining:.2f}) below minimum - completing trade')
                    collection.update_one(
                        {'_id': trade['_id']},
                        {'$set': {'bot': True, 'myBoughtSize': total_bought_tokens}}
                    )
                    break
                
                max_order_size = float(min_price_ask['size']) * float(min_price_ask['price'])
                order_size = min(remaining, max_order_size)
                
                # Ensure minimum order size is 1 USDC
                if order_size < MIN_ORDER_SIZE_USD:
                    info(f'Order size (${order_size:.2f}) below minimum (${MIN_ORDER_SIZE_USD}) - completing trade')
                    collection.update_one(
                        {'_id': trade['_id']},
                        {'$set': {'bot': True, 'myBoughtSize': total_bought_tokens}}
                    )
                    break
                
                # Check if balance is sufficient for the order
                if available_balance < order_size:
                    warning(f'Insufficient balance: Need ${order_size:.2f} but only have ${available_balance:.2f}')
                    abort_due_to_funds = True
                    break
                
                order_args = {
                    'side': 'BUY',
                    'tokenID': trade['asset'],
                    'amount': order_size,
                    'price': float(min_price_ask['price']),
                }
                
                info(f'Creating order: ${order_size:.2f} @ ${min_price_ask["price"]} (Balance: ${available_balance:.2f})')
                
                signed_order = await clob_client.create_market_order(order_args)
                resp = await clob_client.post_order(signed_order, 'FOK')
                
                if resp.get('success') is True:
                    retry = 0
                    tokens_bought = order_args['amount'] / order_args['price']
                    total_bought_tokens += tokens_bought
                    order_result(
                        True,
                        f'Bought ${order_args["amount"]:.2f} at ${order_args["price"]} ({tokens_bought:.2f} tokens)'
                    )
                    remaining -= order_args['amount']
                    # Update balance after successful order
                    available_balance -= order_args['amount']
                else:
                    error_message = extract_order_error(resp)
                    if is_insufficient_balance_or_allowance_error(error_message):
                        abort_due_to_funds = True
                        warning(f'Order rejected: {error_message or "Insufficient balance or allowance"}')
                        warning('Skipping remaining attempts. Top up funds or check allowance before retrying.')
                        break
                    retry += 1
                    warning(f'Order failed (attempt {retry}/{RETRY_LIMIT}){f" - {error_message}" if error_message else ""}')
            except Exception as e:
                retry += 1
                warning(f'Order error (attempt {retry}/{RETRY_LIMIT}): {e}')
        
        if abort_due_to_funds:
            collection.update_one(
                {'_id': trade['_id']},
                {'$set': {'bot': True, 'botExcutedTime': RETRY_LIMIT}}
            )
            return
        
        if retry >= RETRY_LIMIT:
            collection.update_one(
                {'_id': trade['_id']},
                {'$set': {'bot': True, 'botExcutedTime': retry}}
            )
        else:
            collection.update_one(
                {'_id': trade['_id']},
                {'$set': {'bot': True, 'myBoughtSize': total_bought_tokens}}
            )
    
    elif condition == 'sell':
        # SELL strategy - similar to merge but different logic
        info('Executing SELL strategy...')
        # Implementation similar to merge but for selling positions
        # This would be implemented based on the full TypeScript version
        collection.update_one({'_id': trade['_id']}, {'$set': {'bot': True}})

