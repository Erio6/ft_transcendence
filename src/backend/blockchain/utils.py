from django.db import transaction, close_old_connections
from asgiref.sync import sync_to_async
from web3 import Web3
from game.models import Game
from eth_account import Account
from django.conf import settings
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '../../smart_contract/.env'))

def record_game_on_blockchain(game_id):
    try:
        close_old_connections() # Ensure fresh DB connection in thread

        game = Game.objects.get(id=game_id)
        if game.is_recorded_on_blockchain:
            print(f"Game ID {game.id} is already recorded on the blockchain.")
            return None

        w3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URI))
        if not w3.is_connected():
            raise Exception("Failed to connect to blockchain.")

        contract_address = settings.CONTRACT_ADDRESS
        contract_abi = settings.CONTRACT_ABI
        if not w3.is_address(contract_address):
            raise ValueError("Invalid contract address")

        contract = w3.eth.contract(address=contract_address, abi=contract_abi)

        # to change between the 2 PK if using ANVIL or SEPOLIA
        private_key = os.getenv('PRIVATE_KEY')
        if not private_key:
            raise ValueError("Private key not found in environment")

        account = Account.from_key(private_key)

        print(f"Using account address: {account.address}")
        print(f"Contract address: {contract_address}")

        nonce=w3.eth.get_transaction_count(account.address,'pending')
        print(f"[DEBUG] Nonce for transaction: {nonce}")
        txn = contract.functions.recordGameResult(
            game.id,
            game.player_one.user.username,
            game.player_two.user.username,
            game.player_one_score,
            game.player_two_score
        ).build_transaction({
            'chainId': 11155111,  # Sepolia 11155111, Anvil 31337
            'gas': 200000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })
        print(f"Build transaction passed")

        signed_txn = w3.eth.account.sign_transaction(txn, account.key)
        print(f"[DEBUG] Signed transaction hash: {signed_txn.hash.hex()}")
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
        print(f"[DEBUG] Transaction receipt: {receipt}")

        if receipt.status != 1:
            raise Exception("Transaction failed")

        game.tx_hash = tx_hash.hex()
        game.is_recorded_on_blockchain = True
        game.save()

        return tx_hash.hex()

    except Exception as e:
        print(f"Error recording game on blockchain: {e}")
        return None

# it will fail, if you are not running a local blockchain (you need to run anvil)
# i will intentionally leave it like this as we are in development
# settings in djangoProject should be update to test it in SEPOLIA
async def blockchain_score_storage(game_id):
    try:
        tx_hash = await sync_to_async(record_game_on_blockchain)(game_id)
        print(f"Game recorded on blockchain: {tx_hash}")
        return tx_hash
    except Exception as e:
        print(f"Error recording game: {e}")
        return None