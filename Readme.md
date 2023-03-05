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


        
        

            
   
