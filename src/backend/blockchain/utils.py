from web3 import Web3
from django.conf import settings

w3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URI))

if not w3.is_connected():
    raise Exception("Failed to connect to blockchain.")

contract_address = settings.CONTRACT_ADDRESS
contract_abi = settings.CONTRACT_ABI
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

def get_score(player_name):
    return contract.functions.getScore(player_name).call()

def set_score(player_name, score, private_key):
    account = w3.eth.account.from_key(private_key)
    nonce = w3.eth.get_transaction_count(account.address)
    tx = contract.functions.setScore(player_name, score).buildTransaction({
        'from': account.address,
        'nonce': nonce,
        'gas': 200000,
        'gasPrice': w3.to_wei('50', 'gwei'),
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return w3.to_hex(tx_hash)
