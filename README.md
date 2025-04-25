Certainly! Here's a revised README description reflecting that the web development is ongoing while the smart contract (blockchain) work is complete:

---

# Sunlight - Energy Trading Platform

**Sunlight** is a decentralized energy trading platform designed to facilitate peer-to-peer energy trading using blockchain technology. The platform allows consumers (buyers) to purchase energy directly from producers (sellers), promoting green and eco-friendly energy consumption. The core blockchain functionality for secure transactions and energy tracking is already implemented, while web development is currently underway.

## Project Overview

Sunlight enables users to connect their wallets and register as either **Buyers** (consumers) or **Sellers** (energy producers). Sellers can list their available energy units, and buyers can purchase energy directly. The platform leverages blockchain to ensure that all transactions are transparent, secure, and decentralized.

### Current Development Status

- **Blockchain/Smart Contracts**: Fully implemented. The smart contracts that govern energy transactions and user registrations on the blockchain have been developed and deployed. This includes the functionalities for registering buyers and sellers, tracking energy transfers, and managing energy purchases.
  
- **Web Development**: Ongoing. The frontend user interface and interactions are in active development, and the web pages are being integrated to interact with the deployed smart contracts. The current focus is on creating user-friendly dashboards for both buyers and sellers, allowing them to track transactions and energy data.

### Key Features

1. **Login & Registration**: 
   - Users can log in or register as **Buyers** or **Sellers**.
   - Registration requires personal details like **Email, Mobile Number, Aadhar Number (for Sellers),** and **Address**.
   - Secure login with **password recovery** options.

2. **Buyer Dashboard**:
   - **Connect/Disconnect Wallet** functionality.
   - **View Wallet Address**, **Total Energy Bought**, and **Total Bill Amount**.
   - Display **Current Connections** to view producers' profiles and **Buying History**.

3. **Seller Dashboard**:
   - **Connect/Disconnect Wallet** functionality.
   - **View Wallet Address**, **Total Earnings**, **Total Sold Units**, and **Current Customers**.
   - Display **Customer History** for tracking energy transactions.
   - **Producer Profile** with an option to update **price per unit** and **available energy**.

4. **Producer Profile**:
   - Display **Energy Availability**, **Price per Unit**, and **Total Units Sold**.
   - Producers can **Buy Energy** from other producers.
   - **Rating** functionality to rate and review other producers, and **Chat with Producer** option.

5. **Consumer Profile**:
   - Detailed **Address** and **Energy Purchase Details**.
   - **Chat with Customer** option to communicate with the buyer.

### Web Pages Schema

1. **Login/Register Page**:
   - **Login Sections**:
     - Login as **Buyer**
     - Login as **Seller**
     - Email/Password fields with **Forgot Password** option.
   - **Register Sections**:
     - **Register as Buyer**
     - **Register as Seller** (additional fields like **Aadhar Number**, **Mobile Number**, **Email**, **Address**)
     - Password creation and confirmation.

2. **Seller Dashboard**:
   - **Connect/Disconnect Wallet** button.
   - Display **Wallet Address** and **Total Current Customers**.
   - **Customer History** with detailed buyer transaction information.
   - **Producer Profile** link for managing energy and customer ratings.

3. **Buyer Dashboard**:
   - **Connect/Disconnect Wallet** button.
   - Display **Wallet Address** and **Total Energy Bought**.
   - **Current Connections** showing **Producer Profiles**.
   - **Buying History** to view past transactions with sellers.

4. **Producer Profile**:
   - Display **Producer Rating**, **Total Energy Available**, **Price per Unit**, and **Units Sold**.
   - **Buy Energy** option to interact with other producers (through smart contract).
   - **Chat with Producer** option for communication.

5. **Consumer Profile**:
   - Display **Complete Address** and **Energy Purchase History**.
   - **Chat with Customer** option to communicate with the buyer.

### Completed Smart Contract (Blockchain) Features

- **Smart Contracts** for registering buyers and sellers on the blockchain.
- **Energy Transactions**: Track energy purchases and sales between buyers and sellers.
- **Register Buyer**: `registerBuyer()` function called for new buyers to register on the blockchain.
- **Register Seller**: `registerSeller()` function called for new sellers to register on the blockchain.
- **Energy Transfer Tracking**: Each transaction between buyer and seller is securely recorded on the blockchain.
- **Producer and Consumer Rating**: Ratings are stored and updated on the blockchain for transparent feedback.

### Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Django Framework)
- **Blockchain**: Solidity (Smart Contracts), Web3.js (Web3.js for front-end integration)
- **Database**: MongoDB (for storing user data and transaction histories)
- **Wallet Integration**: Web3.js (for connecting and interacting with blockchain)

### How to Run the Project

1. Clone the repository to your local machine.
2. Set up your Python environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up MongoDB for storing user data and transaction information.
4. Run the Django development server:
   ```bash
   python manage.py runserver
   ```
5. Open the platform in your browser at `http://127.0.0.1:8000`.

### Smart Contract Deployment

1. The Solidity smart contracts have been compiled and deployed on an Ethereum-based test network.
2. **Interacting with Blockchain**: The web platform will interact with the deployed smart contracts via Web3.js.
3. Use **Infura** or **Alchemy** to connect the frontend with the blockchain network for live data updates and transactions.

### Future Development

- **UI Improvements**: Currently focusing on enhancing the user interface for better interaction and visual experience.
- **Additional Blockchain Features**: Plans to integrate more advanced blockchain features like energy trading analytics, tokenized rewards, and further smart contract improvements.

### Contributing

We welcome contributions from developers and energy enthusiasts. To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

### License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
