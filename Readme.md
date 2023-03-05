# Završni ispit - ISBIT
***
##### Predmet:
             Informacijska sigurnost i blockchain tehnologije
##### Autori:
            Daniela Kraljić i Rea Žigant      
##### Ak.god:
            2022./2023.
***
#### 📃 Zadatak

Stvorite pametni ugovor koristeći Solidity koji implementira jednostavan sustav tokena. Pametni ugovor treba imati sljedeće značajke:
Ukupna količina tokena koja se može odrediti kada se ugovor implementira
Mogućnost prijenosa tokena s jedne adrese na drugu
Mogućnost provjere stanja tokena za određenu adresu
Ostale značajke koje su potrebne za stvoriti token (ime, kratica, …) proizvoljno definirate.
Funkcije koja vlasniku ugovora omogućuju:
Povećanje ukupne ponude tokena (mint).
Smanjenje ukupne ponude (burn).

#### Solidity pametni ugovor
Ovaj kod predstavlja implementaciju Ethereum ERC-20 tokena (standarda za izdavanje tokena na Ethereum blockchainu).

Definirana su polja za ime, simbol, decimalna mjesta i ukupnu količinu tokena koje se čuvaju u varijabli totalSupply. Također se definira i adresa koja će biti vlasnik tokena (my_address).

Kreirane su dvije mape za spremanje stanja računa i dozvola, koje se koriste za praćenje stanja tokena koji se nalaze na određenim Ethereum adresama.

Funkcija transfer omogućuje prebacivanje tokena sa jedne adrese na drugu, provjerava se je li adresi na koju se želi prebaciti token dodijeljena vrijednost različita od nule i je li dostupna dovoljna količina tokena za prijenos. Nakon prijenosa tokena, emitira se događaj Transfer.

Funkcija balanceOf vraća stanje tokena na određenoj adresi.

Funkcija approve dodjeljuje određenu količinu tokena nekoj drugoj adresi, također emitira događaj Approval.

Funkcija transferFrom se koristi za prebacivanje tokena s adrese na koju je već dodijeljeno određeno ovlaštenje. Provjerava se dostupna količina tokena i ispravno se oduzima iz svakog računa, a zatim emitira događaj Transfer.

Funkcija mint služi za izdavanje novih tokena i može se pozvati samo iz određene adrese (my_address). Nakon dodavanja tokena, emitira se događaj Mint i Transfer.

Funkcija burn omogućuje spaljivanje tokena na određenoj adresi, provjerava se dostupna količina tokena i ispravno se oduzima iz računa. Nakon toga, emitiraju se događaji Burn i Transfer.

Svi događaji su definirani kao emitiranje poruke u blockchain mrežu kako bi bili vidljivi i ostalim korisnicima.

```
// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;


contract ReaAndDanciContract {  
    string public name;
    string public symbol;
    uint8 public decimals;
    uint256 public totalSupply;
    address public my_address;
    
    mapping(address => uint256) private balances;
    mapping(address => mapping(address => uint256)) private allowances;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Mint(address indexed to, uint256 value);
    event Burn(address indexed from, uint256 value);

    constructor() public {
        my_address = 0x18540A7a2446cE028156D59BF66826Cd4f4efA19;
        symbol = "RDC";
        name = "ReaAndDanci Coin";
        decimals = 2;
        totalSupply = 200000;
        balances[my_address] = totalSupply;
        emit Transfer(address(0), my_address, totalSupply);
    }

    function transfer(address _to, uint256 _value) public returns (bool) {
        require(_to != address(0), "ERC20: transfer to the zero address");
        require(_value <= balances[msg.sender], "ERC20: transfer amount exceeds balance");
        
        balances[msg.sender] -= _value;
        balances[_to] += _value;
        
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    function balanceOf(address _owner) public view returns (uint256) {
        return balances[_owner];
    }
    
    
    function mint(address _to, uint256 _value) public returns (bool) {
        require(msg.sender == address(my_address), "ERC20: mint function can only be called by a specific address");
        
        totalSupply += _value;
        balances[_to] += _value;
        
        emit Mint(_to, _value);
        emit Transfer(address(0), _to, _value);
        return true;
    }
    
    function burn(uint256 _value) public returns (bool) {
        require(_value <= balances[msg.sender], "ERC20: burn amount exceeds balance");
        
        totalSupply -= _value;
        balances[msg.sender] -= _value;
        
        emit Burn(msg.sender, _value);
        emit Transfer(msg.sender, address(0), _value);
        return true;
    }
}
```
Ovaj kod kreira i deploya novi pametni ugovor na blockchain mreži pomoću Pythona, koristeći web3.py biblioteku za interakciju s blockchainom i solcx biblioteku za kompiliranje Solidity koda u bytecode.

Prvo se učitava Solidity kod iz datoteke "ReaAndDanciContract.sol", nakon čega se koristi solcx biblioteka za kompiliranje koda u bytecode i ABI (Application Binary Interface) oblik. Bytecode se koristi za deploy na blockchain, a ABI za interakciju s ugovorom.

Nakon što se dobije bytecode i ABI, kreira se objekt "ReaAndDanciContract" pomoću web3.py biblioteke, a zatim se koristi za stvaranje transakcije koja će deployati novi ugovor na blockchain mreži. Transakcija se potpisuje koristeći privatni ključ "PRIVATE_KEY", nakon čega se šalje na mrežu pomoću "send_raw_transaction" funkcije. Čekanje na potvrdu transakcije se obavlja korištenjem "wait_for_transaction_receipt" funkcije.

Nakon što se ugovor uspješno deploya na mrežu, adresa ugovora se sprema u datoteku "contract_address.txt" i vraća se novi objekt koji predstavlja ugovor u Pythonu. Funkcija može primiti i Web3 objekt kao argument, što omogućuje korištenje postojeće konekcije s blockchain mrežom. Ako se ne preda Web3 objekt, funkcija će koristiti "HTTPProvider" da bi se uspostavila nova veza na blockchain mrežu.
```
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
```
Ovaj kod predstavlja implementaciju jednostavne grafičke korisničke sučelja koje koristi web3 biblioteku za interakciju s blockchain mrežom.

Klasa UserInterface nasljeđuje od klase App iz textual paketa, što znači da se koristi za izradu aplikacija s grafičkim korisničkim sučeljem.

CSS_PATH je varijabla koja sadrži putanju do CSS datoteke koja definira stilove korisničkog sučelja.

balance i output su varijable koje koriste biblioteku reactive iz textual paketa kako bi se pratila njihova vrijednost. amount_0, address, amount_1, amount_2 su varijable koje definiraju ulazne polja za unos podataka. function je instanca klase TokenFunction koja je definirana u vanjskoj datoteci token_function.py.

Metode watch_balance i watch_output se koriste za praćenje promjena vrijednosti balance i output.

successful_action i unsuccessful_action su pomoćne metode koje se koriste za ažuriranje output varijable nakon što se izvrši određena akcija (uspješna ili neuspješna).

compose metoda se koristi za stvaranje korisničkog sučelja. Koristi se yield kako bi se definirali elementi koji čine sučelje.

on_button_pressed metoda se poziva kada se klikne gumb. Provjerava se kojem gumbu pripada klik i izvršava se odgovarajuća akcija (transakcija, mint, burn, get_balance).

Uz pomoć query_one metode dohvaćaju se vrijednosti iz ulaznih polja, a zatim se pozivaju metode instanci TokenFunction klase kako bi se izvršile željene akcije.

Ako se dogodi greška, iznimke se hvataju i prikazuju u korisničkom sučelju pomoću unsuccessful_action metode. U slučaju uspješne akcije, ažurira se balance varijabla i poziva se successful_action metoda.

Na kraju se poziva metoda run() koja pokreće korisničko sučelje.
```
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import var
from textual.widgets import Button, Static, Input
from web3.exceptions import ValidationError
from token_function import TokenFunction


class UserInterface(App):
    """A working 'desktop' calculator."""

    CSS_PATH = "style.css"

    balance = var("BALANCE")
    output = var("Welcome to Rea and Danci coin!")

    amount_0 = Input
    address = Input

    amount_1 = Input
    amount_2 = Input

    function = TokenFunction

    def watch_balance(self, value: str) -> None:
        """Called when balance is updated."""
        self.query_one("#balance", Static).update(value)

    def watch_output(self, value: str) -> None:
        """Called when output is updated."""
        self.query_one("#output", Static).update(value)

    def successful_action(self):
        output_element = self.query_one("#output", Static)
        output_element.remove_class("error")
        output_element.add_class("success")
        self.output = "You action was successfully executed!"

    def unsuccessful_action(self, error):
        output_element = self.query_one("#output", Static)
        output_element.remove_class("success")
        output_element.add_class("error")
        self.output = error
    
    def compose(self) -> ComposeResult:
        """Add our buttons."""
        self.function = TokenFunction()

        yield Container(
            Static(id="balance"),
            Button("Transact", id="transact", variant="primary"),
            Input(placeholder="amount", id="amount_0"),
            Input(placeholder="wallet", id="address"),
            Button("Mint", id="mint", variant="primary"),
            Input(placeholder="amount", id="amount_1"),
            Button("Burn", id="burn", variant="primary"),
            Input(placeholder="amount", id="amount_2"),
            Button("Get balance", id="get_balance", variant="primary"),
            Input(placeholder="wallet", id="address_1"),
            Static(id="output"),
            id="user_interface",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        if event.button.id == "transact":
            try:
                amount = self.query_one("#amount_0", Input).value
                address = self.query_one("#address", Input).value

                my_balance, to_balance = self.function.transact(amount, address)
                self.balance = f"My balance: {my_balance} RDC\nReceivers balance: {to_balance} RDC"

                self.successful_action()
            except ValueError:
                self.unsuccessful_action("Amount and wallet are required!")
            except ValidationError:
                self.unsuccessful_action("Insert correct wallet")
            except Exception as error:
                self.unsuccessful_action(str(error))

        if event.button.id == "mint":
            try:
                amount = self.query_one("#amount_1", Input).value
                my_balance = self.function.mint(amount)
                self.balance = f"My balance: {my_balance} RDC"
                self.successful_action()

            except ValueError:
                self.unsuccessful_action("Amount is required and have to be integer!")
            except ValidationError:
                self.unsuccessful_action("Insert valid amount!")
            except Exception as error:
                self.unsuccessful_action(str(error))

        if event.button.id == "burn":
            try:
                amount = self.query_one("#amount_2", Input).value
                my_balance = self.function.burn(amount)
                self.balance = f"My balance: {my_balance} RDC"
                self.successful_action()

            except Exception as error:
                self.unsuccessful_action(str(error))

        if event.button.id == "get_balance":
            try:
                address = self.query_one("#address_1", Input).value
                balance = self.function.get_balance(address)
                self.balance = f"Balance of wallet {address}: {balance} RDC"
                self.successful_action()

            except ValidationError:
                self.unsuccessful_action("Insert a valid wallet address")
            except Exception as error:
                self.unsuccessful_action(str(error))

if __name__ == "__main__":
    UserInterface().run()
```


#### Testiranje na Ganache testnoj mreži

Ovaj kod omogućuje kompiliranje i stvaranje Ethereum pametnog ugovora (smart contract) koristeći Python. Evo detaljnijeg objašnjenja svake linije koda:
###### import json - 
Importiramo JSON modul za manipuliranje JSON formatom podataka.
###### from solcx import compile_standard - 
Importiramo funkciju za kompiliranje pametnog ugovora iz modula solcx.
###### from web3 import Web3 - 
Importiramo biblioteku Web3 koja nam omogućuje interakciju s Ethereum mrežom.
###### from constant import MY_ADDRESS, PRIVATE_KEY, TO_ADDRESS, CHAIN_ID - 
Importiramo konstante koje su potrebne za stvaranje i slanje transakcija. Ove konstante su definirane u constant.py datoteci koja se nalazi u istom direktoriju kao i ovaj kod.
Sljedeća funkcija definira proces stvaranja novog pametnog ugovora i spremanja njegove adrese u lokalnu datoteku:
```Python
def create_new_contract_and_save_it_to_local_file(w3=None):
    if not w3:
        w3 = Web3(Web3.HTTPProvider("http://0.0.0.0:8545"))
        
    with open("./ReaAndDanciContract.sol", "r") as file:
        simple_storage_file = file.read()
```


        
        

            
   
