from web3 import Web3
from eth_account import Account
from django.conf import settings
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '../../smart_contract/.env'))

def record_game_on_blockchain(game):

    #w3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URI))
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

    if not w3.is_connected():
        raise Exception("Failed to connect to blockchain.")

    contract_address = settings.CONTRACT_ADDRESS
    contract_abi = settings.CONTRACT_ABI
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    #account = Account.from_key(os.getenv('PRIVATE_KEY'))
    account = Account.from_key(os.getenv('PRIVATE_KEY_ANVIL'))

    transaction = contract.functions.recordGameResult(
        game.id,
        game.player_one.user.username,
        game.player_two.user.username,
        game.player_one_score,
        game.player_two_score
    ).build_transaction({
        'chainId': 1337,  # Sepolia 11155111,
        'gas': 200000,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(account.address),
    })

    # Signer et envoyer
    signed_txn = w3.eth.account.sign_transaction(transaction, account.key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    return tx_hash.hex()

def blockchain_score_storage(game):
    try:
        tx_hash = record_game_on_blockchain(game)
        print(f"Game recorded on blockchain: {tx_hash}")
    except Exception as e:
        print(f"Error recording game: {e}")