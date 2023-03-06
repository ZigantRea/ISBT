# Završni ispit - ISBIT
***
#### Predmet:
Informacijska sigurnost i blockchain tehnologije
#### Autori:
Daniela Kraljić i Rea Žigant      
#### Ak.god:
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

## Solidity pametni ugovor
#### ReaAndDanciContract.py:
Ovaj kod predstavlja implementaciju Ethereum ERC-20 tokena (standarda za izdavanje tokena na Ethereum blockchainu).

Definirana su polja za ime, simbol, decimalna mjesta i ukupnu količinu tokena koje se čuvaju u varijabli totalSupply. Također se definira i adresa koja će biti vlasnik tokena (my_address).

Funkcija transfer omogućuje prebacivanje tokena sa jedne adrese na drugu, provjerava se je li adresi na koju se želi prebaciti token dodijeljena vrijednost različita od nule i je li dostupna dovoljna količina tokena za prijenos. Nakon prijenosa tokena, emitira se događaj Transfer.
```Python
function transfer(address _to, uint256 _value) public returns (bool) {
        require(_to != address(0), "ERC20: transfer to the zero address");
        require(_value <= balances[msg.sender], "ERC20: transfer amount exceeds balance");
        
        balances[msg.sender] -= _value;
        balances[_to] += _value;
        
        emit Transfer(msg.sender, _to, _value);
        return true;
    }
```
Funkcija balanceOf vraća stanje tokena na određenoj adresi.
```Python
function balanceOf(address _owner) public view returns (uint256) {
        return balances[_owner];
    }
```

Funkcija mint služi za izdavanje novih tokena i može se pozvati samo iz određene adrese (my_address). Nakon dodavanja tokena, emitira se događaj Mint i Transfer.
```Python
 function mint(address _to, uint256 _value) public returns (bool) {
        require(msg.sender == address(my_address), "ERC20: mint function can only be called by a specific address");
        
        totalSupply += _value;
        balances[_to] += _value;
        
        emit Mint(_to, _value);
        emit Transfer(address(0), _to, _value);
        return true;
    }
```

Funkcija burn omogućuje spaljivanje tokena na određenoj adresi, provjerava se dostupna količina tokena i ispravno se oduzima iz računa. Nakon toga, emitiraju se događaji Burn i Transfer.
```Python
   function burn(uint256 _value) public returns (bool) {
        require(_value <= balances[msg.sender], "ERC20: burn amount exceeds balance");
        
        totalSupply -= _value;
        balances[msg.sender] -= _value;
        
        emit Burn(msg.sender, _value);
        emit Transfer(msg.sender, address(0), _value);
        return true;
    }
```
Svi događaji su definirani kao emitiranje poruke u blockchain mrežu kako bi bili vidljivi i ostalim korisnicima.

#### token_deploy.py:

Ovaj kod kreira i deploya novi pametni ugovor na blockchain mreži pomoću Pythona, koristeći web3.py biblioteku za interakciju s blockchainom i solcx biblioteku za kompiliranje Solidity koda.

Prvo se učitava Solidity kod iz datoteke "ReaAndDanciContract.sol", nakon čega se koristi solcx biblioteka za kompiliranje koda u bytecode i ABI (Application Binary Interface) oblik. Bytecode se koristi za deploy na blockchain, a ABI za interakciju s ugovorom.

Nakon što se dobije bytecode i ABI, kreira se objekt "ReaAndDanciContract" pomoću web3.py biblioteke, a zatim se koristi za stvaranje transakcije koja će deployati novi ugovor na blockchain mreži. Transakcija se potpisuje koristeći privatni ključ "PRIVATE_KEY", nakon čega se šalje na mrežu pomoću "send_raw_transaction" funkcije. Čekanje na potvrdu transakcije se obavlja korištenjem "wait_for_transaction_receipt" funkcije.
Nakon što se ugovor uspješno deploya na mrežu, adresa ugovora se sprema u datoteku "contract_address.txt" i vraća se novi objekt koji predstavlja ugovor u Pythonu. 
```Python
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
```
#### token_fuction.py:
U ovoj datoteci stvaramo funkcije pomoću kreiranog pametnog ugovora izrađuju funkcije blockhaina koje smo definirali u ReaAndDanciContract.sol.

Inicijaliziranje klase TokeFuction koja se spaja na web3, ukoliko ne postoji copiled_code.json ili contract_address.txt pozivamo funkciju create_new_contract_and_save_it_to_local_file iz datoteke deploy_token.py koja kreira novi pametni ugovor. Inače ukoliko postoji sve prije navedeno koristi ugovor spremljen u te datoteke.
```Python
class TokenFunction:
    def _init_(self) -> None:
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
```

#### user_interface.py:
Ova datoteka predstavlja implementaciju jednostavne grafičke korisničke sučelja koje koristi web3 biblioteku za interakciju s blockchain mrežom. 
Klasa UserInterface nasljeđuje od klase App iz textual paketa, što znači da se koristi za izradu aplikacija s grafičkim korisničkim sučeljem.
Ova klasa poziva funkcije iz token_fuction.py datoteke.
Izgled korisničkog sučelja je definiran u style.css datoteci.

#### Testiranje na Ganache testnoj mreži
        
![image](https://user-images.githubusercontent.com/100025512/223092807-8af12e47-476d-470a-802e-ab7c91621ba6.png)

Slika korisničkog sučelja za interakciju s ReaAndDanci tokenima na tesnim Walletima Ganache mreži.

![image](https://user-images.githubusercontent.com/100025512/223093430-c1535c71-8add-46c3-9f12-c7db128a6425.png)

Tesni walleti i njihove privatne adrese.

![image](https://user-images.githubusercontent.com/100025512/223093581-b2d603ad-efc7-4bd2-9dae-a694c43983be.png)

Novi blok koji predstavlja transakciju na Ganache testnoj mreži.


### Literatura:
skripta s vježbi
ChatGPT
            
   
