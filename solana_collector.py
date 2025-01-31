import asyncio
import random
import solana
from solana.rpc.async_api import AsyncClient
from solders.transaction import Transaction
from solders.system_program import transfer, TransferParams
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.instruction import Instruction
from solders.transaction import Transaction
from solders.message import Message


async def transfer_all_sol(private_keys, destination_wallet):
    """
    Transfer all SOL from multiple wallets to a single destination wallet.
    
    :param private_keys: List of private keys for source wallets
    :param destination_wallet: Public key of the destination wallet
    """
    # Use Solana devnet or mainnet URL
    solana_client = AsyncClient("https://api.mainnet-beta.solana.com")
    
    for private_key in private_keys:
        try:
            # Convert private key to keypair
            sender_keypair = Keypair.from_base58_string(private_key)
            sender_pubkey = sender_keypair.pubkey()
            
            # Get account balance
            balance_response = await solana_client.get_balance(sender_pubkey)
            balance = balance_response.value
            
            # Account for transaction fees (leave a small buffer)
            transfer_amount = balance - 5000  # 5000 lamports as fee
            
            if transfer_amount > 0:
                # Create transfer transaction
                transfer_instruction = transfer(
                    TransferParams(
                        from_pubkey=sender_pubkey,
                        to_pubkey=Pubkey.from_string(destination_wallet),
                        lamports=transfer_amount
                    )
                )
                
                # Create and add the instruction to a transaction
                transaction = Transaction([sender_keypair], Message([transfer_instruction]), (await solana_client.get_latest_blockhash()).value.blockhash)

                # Sign and send transaction
                tx_hash = await solana_client.send_transaction(transaction)
                print(f"Transferred {transfer_amount} lamports from {sender_pubkey} to {destination_wallet}, tx_hash: {tx_hash.value}")
            else:
                print(f"Insufficient balance in wallet {sender_pubkey}")
        
        except Exception as e:
            print(f"Error transferring from wallet {sender_pubkey}: {e}")
        await asyncio.sleep(random.uniform(0, 10)) # Sleep random amount of second from 0 to 10.

# Example usage
async def main():
    private_keys = [
'PRIVATE_KEY1',
'PRIVATE_KEY2',
'...',
    ]
    destination_wallet = ''
    
    await transfer_all_sol(private_keys, destination_wallet)

# Run the script
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

