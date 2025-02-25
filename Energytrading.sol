/**
 *Submitted for verification at testnet.bscscan.com on 2025-01-03
*/

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EnergyTrading {
    struct User {
        uint256 balance;
        uint256 limit;
        uint256 currentUsage;
        bool active;
        bool isReceiving;
    }

    struct Trade {
        address buyer;
        address seller;
        uint256 energyAmount;
        uint256 price;
        bool completed;
        string deviceId;
    }

    mapping(address => User) public users;
    mapping(string => bool) public activeDevices;
    Trade[] public trades;

    address public owner;

    event TradeCreated(uint256 tradeId, address indexed seller, uint256 energyAmount, uint256 price);
    event TradeCompleted(uint256 tradeId, address indexed buyer);
    event LimitExceeded(address indexed user);
    event EnergyTransferStarted(string deviceId, address indexed user);
    event EnergyTransferStopped(string deviceId, address indexed user);
    event UsageUpdate(address indexed user, uint256 currentUsage);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can perform this action");
        _;
    }

    modifier onlyActiveUser() {
        require(users[msg.sender].active, "User is not active");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function registerUser(uint256 initialBalance, uint256 usageLimit) external {
        require(!users[msg.sender].active, "User already registered");

        users[msg.sender] = User({
            balance: initialBalance,
            limit: usageLimit,
            currentUsage: 0,
            active: true,
            isReceiving: false
        });
    }

    function createTrade(uint256 energyAmount, uint256 price, string calldata deviceId) external onlyActiveUser {
        require(users[msg.sender].balance >= energyAmount, "Insufficient energy balance");
        require(!activeDevices[deviceId], "Device is already in use");

        trades.push(Trade({
            buyer: address(0),
            seller: msg.sender,
            energyAmount: energyAmount,
            price: price,
            completed: false,
            deviceId: deviceId
        }));

        emit TradeCreated(trades.length - 1, msg.sender, energyAmount, price);
    }

    function initiateEnergyTransfer(string memory deviceId, address user) internal {
        require(!activeDevices[deviceId], "Device is already transferring energy");
        
        activeDevices[deviceId] = true;
        users[user].isReceiving = true;
        
        emit EnergyTransferStarted(deviceId, user);
    }

    function stopEnergyTransfer(string memory deviceId, address user) internal {
        require(activeDevices[deviceId], "Device is not transferring energy");
        
        activeDevices[deviceId] = false;
        users[user].isReceiving = false;
        
        emit EnergyTransferStopped(deviceId, user);
    }

    function buyEnergy(uint256 tradeId) external payable onlyActiveUser {
        Trade storage trade = trades[tradeId];

        require(!trade.completed, "Trade already completed");
        require(msg.sender != trade.seller, "Seller cannot buy their own energy");
        require(msg.value == trade.price, "Incorrect payment amount");

        users[trade.seller].balance -= trade.energyAmount;
        users[msg.sender].balance += trade.energyAmount;

        trade.buyer = msg.sender;
        trade.completed = true;

        payable(trade.seller).transfer(msg.value);

        initiateEnergyTransfer(trade.deviceId, msg.sender);

        emit TradeCompleted(tradeId, msg.sender);
    }

    function updateUsageAndMonitor(address user, uint256 newUsage) external onlyOwner {
        require(users[user].active, "User is not active");
        
        users[user].currentUsage = newUsage;
        emit UsageUpdate(user, newUsage);

        if (newUsage >= users[user].limit) {
            users[user].active = false;
            
            for (uint i = 0; i < trades.length; i++) {
                Trade storage trade = trades[i];
                if (trade.buyer == user && trade.completed && activeDevices[trade.deviceId]) {
                    stopEnergyTransfer(trade.deviceId, user);
                    break;
                }
            }
            
            emit LimitExceeded(user);
        }
    }

    function reactivateUser(address user, uint256 newLimit) external onlyOwner {
        require(!users[user].active, "User is already active");

        users[user].limit = newLimit;
        users[user].currentUsage = 0;
        users[user].active = true;
    }

    function getTrade(uint256 tradeId) external view returns (
        address buyer,
        address seller,
        uint256 energyAmount,
        uint256 price,
        bool completed,
        string memory deviceId
    ) {
        Trade memory trade = trades[tradeId];
        return (
            trade.buyer,
            trade.seller,
            trade.energyAmount,
            trade.price,
            trade.completed,
            trade.deviceId
        );
    }

    function getCurrentUsage(address user) external view returns (uint256) {
        return users[user].currentUsage;
    }
}