# 🌌 Omni-Retail: Enterprise Multi-Agent Intelligence

[![Live Demo](https://img.shields.io/badge/Live-Application_Link-blueviolet?style=for-the-badge&logo=vercel)](YOUR_LIVE_APPLICATION_LINK_HERE)

Omni-Retail is a production-grade, multi-agent AI ecosystem designed to unify disparate enterprise data sources—Retail, Logistics, FinTech, and Customer Support—into a single, conversational interface. Powered by **Groq Llama 3.3 70B**, it provides split-second reasoning across petabyte-scale synthetic data.

---

## 🏗️ System Architecture

The project utilizes a **Modular Agentic Reasoning** architecture, ensuring absolute data isolation and high-precision retrieval.

### 1. The Logic Core (Orchestrator)
- **The Planner**: Analyzes user intent and determines the sequence of database lookups across the 4 platforms.
- **The SQL Expert**: Generates context-aware, sandboxed SQLite queries for each specific domain.
- **Identity Resolver**: Proactively identifies anonymous users by cross-referencing order history with user profiles.
- **Synthesis Engine**: Merges raw data into a professional, HTML-formatted dashboard response.

### 2. Four Platform Ecosystem
| Platform | Focus | Key Tables |
| :--- | :--- | :--- |
| **ShopCore** (Retail) | User accounts & Catalog | `Users`, `Products`, `Orders` |
| **ShipStream** (Logistics) | Global tracking & Warehousing | `Shipments`, `Warehouses`, `TrackingEvents` |
| **PayGuard** (FinTech) | Transactions & Wallet | `Wallets`, `Transactions`, `PaymentMethods` |
| **CareDesk** (Support) | Tickets & Satisfaction | `Tickets`, `TicketMessages`, `Surveys` |

---

## ✨ Key Features

- **🚀 Instant Reasoning**: Powered by Groq for sub-second LLM inference.
- **🎙️ Voice-Auto-Submit**: Integrated Web Speech API allows users to speak queries and watch the system automatically process and read back answers.
- **📊 Premium HTML Formatting**: High-contrast bolding (**<b>**) and structured lists (**<ul><li>**) for a professional dashboard experience.
- **🎭 Identity Recovery**: Personalized greetings (e.g., "Hello Alice") even for anonymous queries like *"Where is my order?"*
- **📈 Production-Scale**: Built-in generator creating **500 users**, **2000 orders**, and **500 support cases**.
- **🛡️ Model Fallback**: Automatic failover to Llama 3.1 8B in case of Rate Limits (429 errors).

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- Node.js 18+
- [Groq API Key](https://console.groq.com/)

### 2. Installation
```powershell
# Clone the repository
git clone [your-repo-link]
cd omni_retail

# Install Python dependencies
pip install -r requirements.txt

# Install Frontend dependencies
cd omni-retail-web
npm install
```

### 3. Setup Environment
Create a `.env` file in the root:
```env
GROQ_API_KEY=your_key_here
```

### 4. Run the Ecosystem
```powershell
# Generate production data and start both servers
.\run_all.bat
```

---

## 💬 Sample Queries

Test the system's cross-platform reasoning with these scenarios:

- **Anonymous Identity**: *"I ordered a Gaming Monitor. Can you check my shipping location and my wallet balance?"*
- **Support Deep-Dive**: *"Check order #1500. Who is the customer, where is the package, and what was the last message on their support ticket?"*
- **FinTech Intelligence**: *"I am Chad Baldwin. Show me my last three transactions and my current balance."*
- **Logistics Trace**: *"Where did shipment TRK-ALICE-101 originate from, and who is the manager of that warehouse?"*

---

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## 🤝 Project Links
- **GitHub**: [Link to Repository](https://github.com/your-username/omni-retail)
- **Live Version**: [Link to Live App](YOUR_LIVE_APPLICATION_LINK_HERE)

**Engineered by Antigravity AI for the next generation of Agentic Commerce.**
