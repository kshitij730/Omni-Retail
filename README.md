# 🌌 Omni-Retail: Enterprise Multi-Agent Intelligence

[![Live Demo](https://img.shields.io/badge/Live-Application_Link-blueviolet?style=for-the-badge&logo=vercel)](YOUR_LIVE_APPLICATION_LINK_HERE)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Omni-Retail is a production-grade, multi-agent AI ecosystem designed to unify disparate enterprise data sources—Retail, Logistics, FinTech, and Customer Support—into a single, conversational interface. Powered by **Groq Llama 3.3 70B**, it provides split-second reasoning across production-scale synthetic data.

---

## 🏗️ System Architecture

The project utilizes a **Modular Agentic Reasoning** architecture, ensuring absolute data isolation and high-precision retrieval.

### 🧩 The Multi-Agent Logic Core
The system is orchestrated by a central "Brain" (`orchestrator_groq.py`) that manages specialized sub-agents:

1.  **The Planner**: Analyzes user intent and determines the sequence of database lookups across the platform.
2.  **Specialized Sub-Agents**:
    *   **ShopCore Agent**: Manages user profiles, catalogs, and order history.
    *   **ShipStream Agent**: Handles global tracking, warehouse logistics, and shipping status.
    *   **PayGuard Agent**: Oversees wallets, transactions, and payment security.
    *   **CareDesk Agent**: Manages support tickets, agent messages, and satisfaction surveys.
3.  **Identity Resolver**: Proactively identifies anonymous users (Queries like "Where is my order?") by cross-referencing recent transactions with the Retail database.
4.  **Synthesis Engine**: Merges raw data into a professional dashboard response with automated Text-to-Speech (TTS).

### 🗄️ Database Ecosystem
We maintain 4 separate SQLite databases to simulate a real-world enterprise environment where data is siloed:
*   **RetailDB**: Users, Products, Orders.
*   **LogisticsDB**: Shipments, Warehouses, Tracking Events.
*   **FinanceDB**: Virtual Wallets, Transactions.
*   **SupportDB**: Helpdesk Tickets, Messages, NPS Surveys.

---

## ✨ Features

- **🚀 Ultra-Low Latency**: Sub-second inference powered by the Groq Llama-3-70B model.
- **🎙️ Voice-First Interface**: Speak your queries naturally. The system handles recognition, processing, and reads the answer back automatically.
- **📊 Adaptive Dashboards**: Responses are returned in rich HTML format, automatically bolding IDs, statuses, and currency.
- **🛡️ Secure Reasoning**: SQL is generated within strict database sandboxes, preventing cross-database hallucinations.
- **📈 Scalability**: Includes an automated generator (`setup_dbs.py`) creating 500+ users and 2000+ orders for testing.
- **🤖 Model Failover**: Automatic fallback to Llama-3-8B in case of Groq rate limits.

---

## 🛠️ Tech Stack & Repositories Used

### Frontend
- **Framework**: [Next.js 15+](https://nextjs.org/) (React 19)
- **Styling**: [Tailwind CSS 4](https://tailwindcss.com/)
- **Animations**: [Framer Motion](https://www.framer.com/motion/)
- **Icons**: [Lucide React](https://lucide.dev/)
- **Voice**: Web Speech API (Native Browser Support)

### Backend
- **Language**: [Python 3.10+](https://www.python.org/)
- **API**: [FastAPI](https://fastapi.tiangolo.com/)
- **Server**: [Uvicorn](https://www.uvicorn.org/)
- **LLM SDK**: [Groq Python](https://github.com/groq/groq-python)

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher
- A [Groq API Key](https://console.groq.com/)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/your-username/omni-retail.git
cd omni_retail

# Install Python backend dependencies
pip install -r requirements.txt

# Install Frontend dependencies
npm install
```

### 3. Setup Environment
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Database Initialization
Generate the production-scale synthetic data:
```bash
python setup_dbs.py
```

---

## 🏃 Running the Application

### The Easy Way (One-Click)
We provide a master launcher for Windows users:
```powershell
.\run_all.bat
```
This script handles:
1.  Stopping any old sessions on port 8000.
2.  Starting the **FastAPI Backend**.
3.  Starting the **Next.js Frontend**.

### Manual Start
**Run Backend:**
```bash
python src/server.py
```
**Run Frontend:**
```bash
npm run dev
```

---

## 💬 Sample Queries

| Query Type | Example |
| :--- | :--- |
| **Anonymous Search** | *"I ordered a Pro Laptop. Where is it and what is my wallet balance?"* |
| **Logistics Deep-Dive** | *"Check order #150. Which warehouse is it at and who is the manager?"* |
| **Support Trace** | *"Am I Alice Johnson? Show me my recent support ticket messages."* |
| **Financial History** | *"Show me all Debit transactions for Seth Matthews."* |

---

## 📜 License & Acknowledgments

Distributed under the **MIT License**. See `LICENSE` for more information.

Special thanks to the **Groq Team** for providing the world's fastest inference engine and the **Meta AI** team for the Llama 3.3 models.

---

**Engineered with ❤️ by Antigravity AI.**
