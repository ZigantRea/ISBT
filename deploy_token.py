import json

from solcx import compile_standard
from web3 import Web3
from constant import MY_ADDRESS, PRIVATE_KEY, TO_ADDRESS, CHAIN_ID


def create_new_contract_and_save_it_to_local_file(w3=None):
    if not w3:
        w3 = Web3(Web3.HTTPProvider("http://0.0.0.0:8545"))
        
    with open("./ReaAndDanciContract.sol", "r") as file:
        simple_storage_file = file.read()

    # Compile the Solidity contract using the solcx package
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"ReaAndDanciContract.sol": {"content": simple_storage_file}},
            "settings": {"outputSelection": {"*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}}},
        },
        solc_version="0.6.0",
    )

    # Save the compiled contract's bytecode and ABI to a local file
    with open("compiled_code.json", "w") as file:
        json.dump(compiled_sol, file)

    # Extract the bytecode and ABI from the compiled contract
    bytecode = compiled_sol["contracts"]["ReaAndDanciContract.sol"]["ReaAndDanciContract"]["evm"]["bytecode"]["object"]
    abi = compiled_sol["contracts"]["ReaAndDanciContract.sol"]["ReaAndDanciContract"]["abi"]

    # Create the contract in python
    ReaAndDanciContract = w3.eth.contract(abi=abi, bytecode=bytecode)

    # Build a transaction
    transaction = ReaAndDanciContract.constructor().build_transaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": CHAIN_ID,
            "from": MY_ADDRESS,
            "nonce": w3.eth.getTransactionCount(MY_ADDRESS),
        }
    )

    # Sign a transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)

    # Send the signed transaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # Create the contract in python
    with open("contract_address.txt", "w") as f:
        f.write(tx_receipt.contractAddress)
    return w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)


if __name__ == "__main__":
    create_new_contract_and_save_it_to_local_file()
