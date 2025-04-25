/**
 *Submitted for verification at testnet.bscscan.com on 2025-04-16
*/

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EnergyTrading {
    struct BuyerHistory {
        uint256 energybought;
        uint256 amountpaid;
        address seller;
    }

    struct Buyer {
        uint256 receivedenergy;
        uint256 remainingenergy;
        uint256 boughtenergy;
        uint256 totalBill;
        uint256 totalEnergyBought;
        bool active;
        bool isReceiving;
        bool trans;
    }

    struct Customer {
        uint256 customertransferedenergy;
        uint256 customerremainingenergy;
        uint256 customerboughtenergy;
        uint256 perunitprice;
        address buyer;
    }

    struct Seller {
        Customer[] livecustomers;
        Customer[] customerhistory;
        bool isavailable;
        uint256 totalenergyavailable;
        uint256 priceperunit;
        uint256 totalSoldUnit;
        uint256 totalEarnings;
        uint256 totalActiveConnections;
    }

    struct Trade {
        address buyer;
        address seller;
        uint256 energyAmount;
        uint256 priceperunit;
        uint256 totalprice;
        bool completed;
    }

    address SunlightOwner;
    constructor (){
        SunlightOwner = msg.sender;
    }
    mapping(address => BuyerHistory[]) internal buyinghistory;
    mapping(address => Customer[]) internal sellinghistory;
    mapping(address => Buyer) internal buyerpage;
    mapping(address => Seller) internal sellerpage;

    address[] public AvailableSellers;
    Trade[] public trades;

    event TradeCreated(uint256 indexed tradeId, address indexed seller, uint256 energyAmount, uint256 totalprice);
    event TradeCompleted(uint256 indexed tradeId, address indexed buyer);
    event EnergyTransferStarted(address indexed buyer, address indexed seller);
    event EnergyTransferStopped(address indexed buyer, address indexed seller);

    function registerBuyer() external {
        require(!buyerpage[msg.sender].active, "Already registered as buyer");
        buyerpage[msg.sender] = Buyer({
            receivedenergy: 0,
            remainingenergy: 0,
            boughtenergy: 0,
            totalBill : 0,
            totalEnergyBought : 0,
            active: true,
            isReceiving: false,
            trans : false
        });
    }

    function registerSeller(uint256 totalenergyAvaialble, uint256 pricePerUnit) external {
        require(!sellerpage[msg.sender].isavailable, "Already registered as seller");
        sellerpage[msg.sender].isavailable = true;
        sellerpage[msg.sender].totalenergyavailable = totalenergyAvaialble;
        sellerpage[msg.sender].priceperunit = pricePerUnit;
        sellerpage[msg.sender].totalSoldUnit = 0;
        sellerpage[msg.sender].totalEarnings = 0;
        sellerpage[msg.sender].totalActiveConnections = 0;
        AvailableSellers.push(msg.sender);
    }

    function buyEnergy(address sellerAddress, uint256 energyAmount) external payable {
        require(buyerpage[msg.sender].active, "Register as buyer first");
        require(sellerpage[sellerAddress].isavailable, "Seller not available");

        uint256 totalCost = energyAmount * sellerpage[sellerAddress].priceperunit;
        require(msg.value >= totalCost, "You don't have enough Amount, try reducing energyAmount");

        trades.push(Trade({
            buyer: msg.sender,
            seller: sellerAddress,
            energyAmount: energyAmount,
            priceperunit: sellerpage[sellerAddress].priceperunit,
            totalprice: totalCost,
            completed: true
        }));

        payable(sellerAddress).transfer(totalCost);

        Buyer storage buyer = buyerpage[msg.sender];
        Seller storage seller = sellerpage[sellerAddress];

        seller.totalSoldUnit+=energyAmount;
        seller.totalEarnings+=totalCost;

        buyer.totalBill += totalCost;
        buyer.totalEnergyBought += energyAmount;
        buyer.receivedenergy = 0;
        buyer.boughtenergy = energyAmount;
        buyer.remainingenergy = energyAmount;
        buyer.isReceiving = true;

        seller.livecustomers.push(Customer({
            customertransferedenergy: 0,
            customerremainingenergy: energyAmount,
            customerboughtenergy: energyAmount,
            perunitprice: seller.priceperunit,
            buyer: msg.sender
        }));


        buyer.trans = initiateEnergy();
        seller.totalActiveConnections+=1;
        buyinghistory[msg.sender].push(BuyerHistory({
            energybought: energyAmount,
            amountpaid: totalCost,
            seller: sellerAddress
        }));

        emit TradeCreated(trades.length - 1, sellerAddress, energyAmount, totalCost);
        emit TradeCompleted(trades.length - 1, msg.sender);
        emit EnergyTransferStarted(msg.sender, sellerAddress);
    }

    function initiateEnergy() internal pure returns(bool){
        return true;
    }

    function monitorEnergyTransfer(address buyerAddr, address sellerAddr, uint256 amount) external returns (bool) {
    require(sellerpage[sellerAddr].isavailable, "Seller not available");
    require(buyerpage[buyerAddr].active, "Buyer not active");

    buyerpage[buyerAddr].isReceiving = true;
    buyerpage[buyerAddr].receivedenergy += amount;
    buyerpage[buyerAddr].remainingenergy += amount;

    Seller storage seller = sellerpage[sellerAddr];
    for (uint256 i = 0; i < seller.livecustomers.length; i++) {
        if (seller.livecustomers[i].buyer == buyerAddr) {
            seller.livecustomers[i].customertransferedenergy += amount;
            seller.livecustomers[i].customerremainingenergy -= amount;

            if (seller.livecustomers[i].customerremainingenergy == 0) {
                buyerpage[buyerAddr].trans = stopEnergyTransfer(buyerAddr, sellerAddr);
                seller.customerhistory.push(seller.livecustomers[i]);

                seller.livecustomers[i] = seller.livecustomers[seller.livecustomers.length - 1];
                seller.livecustomers.pop();
                seller.totalActiveConnections-=1;
            }

            break;
        }
    }

    emit EnergyTransferStarted(buyerAddr, sellerAddr);
    return true;
}

    function stopEnergyTransfer(address buyerAddr, address sellerAddr) internal returns (bool) {
    require(buyerpage[buyerAddr].isReceiving, "Transfer not active");

    buyerpage[buyerAddr].isReceiving = false;

    emit EnergyTransferStopped(buyerAddr, sellerAddr);
    return false;
}


    function myBuyingHistory() external view returns (BuyerHistory[] memory) {
        require(buyerpage[msg.sender].active, "It's not registered buyer");
        return buyinghistory[msg.sender];
    }

    function mySellingHistory() external view returns (Customer[] memory) {
        Seller storage seller = sellerpage[msg.sender];
        require(seller.isavailable, "It's not registered seller");
        return sellinghistory[msg.sender];
    }

    function yourCurrentCustomers() external view returns (Customer[] memory) {
        require(sellerpage[msg.sender].isavailable, "Seller not registered");
        return sellerpage[msg.sender].livecustomers;
    }

    function UpdatePriceperUnit(uint newPrice) external { 
        sellerpage[msg.sender].priceperunit = newPrice;
    }
    
    function UpdateTotalEnergyAvailablility(uint256 total) external {
        sellerpage[msg.sender].totalenergyavailable = total;
    }
}
