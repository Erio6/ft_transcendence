from asgiref.sync import sync_to_async
from web3 import Web3
from eth_account import Account
from django.conf import settings
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '../../smart_contract/.env'))

def record_game_on_blockchain(game):

    w3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URI))

    if not w3.is_connected():
        raise Exception("Failed to connect to blockchain.")

    contract_address = settings.CONTRACT_ADDRESS
    contract_abi = settings.CONTRACT_ABI

    if not w3.is_address(contract_address):
        raise ValueError("Invalid contract address")

    contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# to change between the 2 PK if using ANVIL or SEPOLIA
    private_key = os.getenv('PRIVATE_KEY_ANVIL')
    if not private_key:
        raise ValueError("Private key not found in environment")

    account = Account.from_key(private_key)


    # Print some debug info
    print(f"Using account address: {account.address}")
    print(f"Contract address: {contract_address}")

    transaction = contract.functions.recordGameResult(
        game.id,
        game.player_one.user.username,
        game.player_two.user.username,
        game.player_one_score,
        game.player_two_score
    ).build_transaction({
        'chainId': 31337,  # Sepolia 11155111, Anvil 31337
        'gas': 200000,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(account.address),
    })

    # Signer et envoyer
    signed_txn = w3.eth.account.sign_transaction(transaction, account.key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

    if receipt.status != 1:
        raise Exception("Transaction failed")

    return tx_hash.hex()

# it will fail, if you are not running a local blockchain (you need to run anvil)
# i will intentionally leave it like this as we are in development
# settings in djangoProject should be update to test it in SEPOLIA
async def blockchain_score_storage(game):
    try:
        tx_hash = await sync_to_async(record_game_on_blockchain)(game)
        print(f"Game recorded on blockchain: {tx_hash}")
    except Exception as e:
        print(f"Error recording game: {e}")