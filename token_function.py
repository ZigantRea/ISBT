from solcx import compile_standard, install_solc
from pathlib import Path


import json
from web3 import Web3
from deploy_token import create_new_contract_and_save_it_to_local_file
from constant import MY_ADDRESS, PRIVATE_KEY, TO_ADDRESS, CHAIN_ID

install_solc("0.6.0")


class TokenFunction:
    def __init__(self) -> None:
        self.simple_storage = None
        # Connect to ganache
        self.w3 = Web3(Web3.HTTPProvider("http://0.0.0.0:8545"))

        # if token is already created don't create new
        compiled_code = Path("./compiled_code.json")
        contract_address = Path("./contract_address.txt")

        if compiled_code.is_file() and contract_address.is_file():
            self.simple_storage = self.import_contract_from_local_file()

        else:
            self.simple_storage = create_new_contract_and_save_it_to_local_file(w3=self.w3)

    def import_contract_from_local_file(self):
        with open("compiled_code.json", "r") as f:
            compiled_code = json.load(f)

        with open("contract_address.txt", "r") as f:
            CONTRACT_ADDRESS = f.read()

        abi = compiled_code["contracts"]["ReaAndDanciContract.sol"]["ReaAndDanciContract"]["abi"]
        # # create a Contract object
        return self.w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

    def transact(self, amount=1000, address=TO_ADDRESS):
        """
        Send transaction to receiver
        """
        amount = int(amount)
        store_transaction = self.simple_storage.functions.transfer(address, amount).buildTransaction(
            {
                "gasPrice": self.w3.eth.gas_price,
                "chainId": CHAIN_ID,
                "from": MY_ADDRESS,
                "nonce": self.w3.eth.getTransactionCount(MY_ADDRESS),
            }
        )

        signed_store_txn = self.w3.eth.account.sign_transaction(store_transaction, private_key=PRIVATE_KEY)

        send_store_tx = self.w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(send_store_tx)

        my_balance = self.simple_storage.functions.balanceOf(MY_ADDRESS).call()
        to_balance = self.simple_storage.functions.balanceOf(address).call()

        return my_balance, to_balance

    def mint(self, amount=1000):
        """
        Calling mint function
        """
        amount = int(amount)
        gas_price = self.w3.eth.gas_price
        gas_limit = self.simple_storage.functions.mint(MY_ADDRESS, amount).estimateGas({"from": MY_ADDRESS})

        transaction = self.simple_storage.functions.mint(MY_ADDRESS, amount).buildTransaction(
            {
                "from": MY_ADDRESS,
                "gasPrice": gas_price,
                "gas": gas_limit,
                "nonce": self.w3.eth.getTransactionCount(MY_ADDRESS),
            }
        )

        signed_transaction = self.w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
        tx_hash = self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        # print(f'Transaction hash: {self.w3.toHex(tx_hash)}')
        my_balance = self.simple_storage.functions.balanceOf(MY_ADDRESS).call()
        return my_balance

    def burn(self, amount=1000):
        """
        Calling burn function
        """
        amount = int(amount)
        gas_price = self.w3.eth.gas_price
        gas_limit = self.simple_storage.functions.burn(amount).estimateGas({"from": MY_ADDRESS})

        transaction = self.simple_storage.functions.burn(amount).buildTransaction(
            {
                "from": MY_ADDRESS,
                "gasPrice": gas_price,
                "gas": gas_limit,
                "nonce": self.w3.eth.getTransactionCount(MY_ADDRESS),
            }
        )

        signed_transaction = self.w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
        tx_hash = self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        my_balance = self.simple_storage.functions.balanceOf(MY_ADDRESS).call()
        return my_balance

    def get_balance(self, address=MY_ADDRESS):
        return self.simple_storage.functions.balanceOf(address).call()

    def approve(self, address=TO_ADDRESS, amount=10000000):
        amount = int(amount)
        return self.simple_storage.functions.approve(address, amount).call()
    
def help():
    print("Welcome to Rea & Dance coin -.-")
    print("Select your action:")
    print("\t1 for transaction between two account")
    print("\t2 for minting new coin. YEAHHHH!!!")
    print("\t3 for burning coin. Pls no")
    print("\t4 for your balance")
    print("\tH for help")
    print("\t0 for exit\n")


def main():
    t = TokenFunction()
    action = 9

    help()
    while action != "0":
        error = False
        action = input()
        match action:
            case "1":
                try:
                    print("Insert amount:")
                    amount = input()
                    my_balance, to_balance = t.transact(amount=amount)
                    print(f"My balance: {my_balance}\nReceivers balance: {to_balance}")
                except Exception as e:
                    print("Error occur in your action. Please try again.")
                    print(f"ERROR: {e}\n")
                    error = True
            case "2":
                try:
                    print("Insert amount:")
                    amount = input()
                    my_balance = t.mint(amount=amount)
                    print(f"My balance: {my_balance}")
                except Exception as e:
                    print("Error occur in your action. Please try again.")
                    print(f"ERROR: {e}\n")

                    error = True

            case "3":
                try:
                    print("Insert amount:")
                    amount = input()
                    my_balance = t.burn(amount=amount)
                    print(f"My balance: {my_balance}")
                except Exception as e:
                    print("Error occur in your action. Please try again.")
                    print(f"ERROR: {e}\n")
                    error = True
            case "4":
                print(t.get_balance())
            case "5":
                print("Insert amount:")
                amount = input()
                print(t.approve(address=MY_ADDRESS, amount=amount))
            case "H":
                help()
                error = True
            case "0":
                print("Thank you! Come back sometimes :D")
                break
            case _:
                print("Not valid choice\n")
                error = True

        if not error:
            print("You action is successfully executed. Select new action\n")


if __name__ == "__main__":
    main()
