import os
from web3 import Web3
from decouple import config
import json

BSC_RPC_URL = config('BSC_RPC_URL')
CONTRACT_ADDRESS = config('CONTRACT_ADDRESS')
CONTRACT_ABI = json.loads(config('CONTRACT_ABI'))

web3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))

contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)

def get_web3():
    return web3

def get_contract():
    return contract 