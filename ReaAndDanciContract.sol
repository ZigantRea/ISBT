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
