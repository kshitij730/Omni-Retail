# 🌌 Omni-Retail: Enterprise Multi-Agent Intelligence

[![Live Demo](https://omni-retail-1.onrender.com/)](YOUR_RENDER_APP_URL_HERE)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-15+-black.svg)](https://nextjs.org/)

Omni-Retail is a production-grade, multi-agent AI ecosystem designed to unify disparate enterprise data sources—**Retail, Logistics, FinTech, and Customer Support**—into a single, conversational interface. Powered by **Groq Llama 3.3 70B**, it provides split-second reasoning across production-scale synthetic data with a **voice-first** user experience.

---

## 🏗️ System Architecture

The project utilizes a **Modular Agentic Reasoning** architecture, ensuring absolute data isolation and high-precision retrieval.

### 🧩 The Multi-Agent Logic Core
The system is orchestrated by a central "Brain" (`orchestrator_groq.py`) that manages specialized sub-agents:

1.  **The Planner**: Analyzes user intent and determines the optimal sequence of database lookups across all platforms.
2.  **Specialized Sub-Agents**:
    *   **ShopCore Agent** (`src/subagents/shopcore.py`): Manages user profiles, product catalogs, and order history.
    *   **ShipStream Agent** (`src/subagents/shipstream.py`): Handles global tracking, warehouse logistics, and shipping status.
    *   **PayGuard Agent** (`src/subagents/payguard.py`): Oversees virtual wallets, transactions, and payment security.
    *   **CareDesk Agent** (`src/subagents/caredesk.py`): Manages support tickets, agent messages, and satisfaction surveys.
3.  **Identity Resolver**: Proactively identifies anonymous users (e.g., "Where is my order?") by cross-referencing recent transactions.
4.  **Synthesis Engine**: Merges raw data into professional, HTML-formatted dashboard responses with automated Text-to-Speech.

### 🗄️ Four-Platform Database Ecosystem
We maintain 4 separate SQLite databases to simulate a real-world enterprise environment where data is siloed:

| Database | Focus | Key Tables | Agent |
|:---------|:------|:-----------|:------|
| **ShopCore** | Retail Operations | Users, Products, Orders | ShopCore Agent |
| **ShipStream** | Logistics & Tracking | Shipments, Warehouses, TrackingEvents | ShipStream Agent |
| **PayGuard** | Financial Transactions | Wallets, Transactions, PaymentMethods | PayGuard Agent |
| **CareDesk** | Customer Support | Tickets, TicketMessages, Surveys | CareDesk Agent |

---

## ✨ Features

- **🚀 Ultra-Low Latency**: Sub-second inference powered by Groq's Llama-3.3-70B model.
- **🎙️ Voice-First Interface**: 
  - Speak your queries naturally using the Web Speech API
  - Automatic speech-to-text conversion
  - AI reads responses back to you with Text-to-Speech
  - Hands-free operation with auto-submit
- **📊 Adaptive Dashboards**: Responses formatted in rich HTML with automatic bolding of IDs, statuses, and currency.
- **🛡️ Secure SQL Generation**: Queries generated within strict database sandboxes, preventing cross-database hallucinations.
- **🎭 Anonymous Query Handling**: Identifies users even when they don't provide their name (e.g., "I ordered a Gaming Monitor").
- **📈 Production-Scale Data**: Includes automated generator creating 500+ users, 2000+ orders, and 500+ support tickets.
- **🔄 Model Failover**: Automatic fallback to Llama-3.1-8B in case of Groq rate limits.
- **🎨 Premium UI**: Dark mode, glassmorphism effects, smooth animations with Framer Motion.

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: [Next.js 15+](https://nextjs.org/) with React 19
- **Styling**: [Tailwind CSS 4](https://tailwindcss.com/)
- **Animations**: [Framer Motion](https://www.framer.com/motion/)
- **Icons**: [Lucide React](https://lucide.dev/)
- **Voice**: Web Speech API (Native Browser Support)
- **License**: MIT

### Backend
- **Language**: [Python 3.10+](https://www.python.org/)
- **API Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Server**: [Uvicorn](https://www.uvicorn.org/)
- **LLM SDK**: [Groq Python](https://github.com/groq/groq-python)
- **Database**: SQLite3 (with 4 separate databases)
- **Data Generation**: [Faker](https://faker.readthedocs.io/)
- **License**: MIT

### Key Dependencies
```
Backend:
- fastapi
- pydantic
- uvicorn
- groq
- python-dotenv
- faker

Frontend:
- next@16.1.3
- react@19.2.3
- framer-motion@12.26.2
- tailwindcss@4
- lucide-react@0.562.0
```

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.10+** installed
- **Node.js 18+** installed
- A **[Groq API Key](https://console.groq.com/)** (free tier available)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/your-username/omni-retail.git
cd omni-retail

# Install Python backend dependencies
pip install -r requirements.txt

# Install Frontend dependencies
npm install
```

### 3. Environment Setup

Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Database Initialization

Generate the production-scale synthetic data (500 users, 2000 orders):
```bash
python setup_dbs.py
```

This creates 4 SQLite databases in the `data/` folder:
- `DB_ShopCore.db`
- `DB_ShipStream.db`
- `DB_PayGuard.db`
- `DB_CareDesk.db`

---

## 🏃 Running the Application

### Option A: One-Click Launch (Windows)
```powershell
.\run_all.bat
```
This automatically:
1. Cleans up any existing sessions on port 8000
2. Starts the FastAPI backend
3. Starts the Next.js frontend

### Option B: Manual Start

**Terminal 1 - Backend:**
```bash
python src/server.py
```

**Terminal 2 - Frontend:**
```bash
npm run dev
```

### Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 💬 Sample Queries

Test the full power of the multi-agent system with these queries:

### Anonymous Identity Recovery
> *"I ordered a **Gaming Monitor** recently. Can you check my **shipping status**, my current **wallet balance**, and see if the **support ticket** I opened has been resolved?"*

**Triggers**: ShopCore → ShipStream → PayGuard → CareDesk

### Full 360° Status Check
> *"I am **Alice Johnson**. Give me a complete update on my latest order: the **product name**, which **warehouse** it's at, if my **payment** was successful, and the latest **support message**."*

**Triggers**: All 4 agents in sequence

### Financial & Feedback Audit
> *"Check everything for **Chad Baldwin**. What did he last buy, is it delivered, what is his **account balance**, and did he leave a **satisfaction survey**?"*

**Triggers**: ShopCore → ShipStream → PayGuard → CareDesk (with survey lookup)

### Logistics Deep-Dive
> *"Check **order #1200**. Tell me the **tracking number**, which **warehouse manager** is responsible, my current **balance**, and the **status** of my last support inquiry."*

**Triggers**: ShopCore → ShipStream → PayGuard → CareDesk

---

## 🌐 Deployment

### Local Development
This project works perfectly for local development using the `run_all.bat` script or manual commands.

### Production Deployment (Render.com) ⭐ Recommended
This project is optimized for deployment on **[Render.com](https://render.com)**, which supports:
- ✅ **SQLite databases** with persistent disk storage
- ✅ **Python and Node.js** applications
- ✅ **Free tier** available
- ✅ **Auto-deploy** on git push
- ✅ **Environment variables** management

**See [RENDER_DEPLOYMENT.md](./RENDER_DEPLOYMENT.md) for complete step-by-step deployment instructions.**

### Alternative Platforms
- **Railway.app**: Supports SQLite with persistent volumes
- **DigitalOcean App Platform**: Supports persistent storage
- **Fly.io**: Supports persistent volumes

**Note**: Vercel and other serverless platforms are **not compatible** due to read-only filesystems (SQLite requires write access).

---

## 📁 Project Structure

```
omni-retail/
├── src/                          # Python Backend
│   ├── orchestrator_groq.py     # Main AI orchestrator
│   ├── server.py                # FastAPI server
│   ├── utils.py                 # Database utilities
│   └── subagents/               # Specialized agents
│       ├── shopcore.py          # Retail agent
│       ├── shipstream.py        # Logistics agent
│       ├── payguard.py          # FinTech agent
│       └── caredesk.py          # Support agent
├── app/                         # Next.js App Router
│   ├── page.tsx                 # Main page
│   ├── layout.tsx               # Root layout
│   └── globals.css              # Global styles
├── components/                  # React Components
│   └── OmniAgentUI.tsx         # Main chat interface
├── data/                        # SQLite Databases
│   ├── DB_ShopCore.db
│   ├── DB_ShipStream.db
│   ├── DB_PayGuard.db
│   └── DB_CareDesk.db
├── public/                      # Static assets
├── setup_dbs.py                 # Database generator
├── demo.py                      # CLI demo script
├── requirements.txt             # Python dependencies
├── package.json                 # Node.js dependencies
├── README.md                    # This file
├── RENDER_DEPLOYMENT.md         # Deployment guide
└── LICENSE                      # MIT License
```

---

## 📜 License & Acknowledgments

### License
Distributed under the **MIT License**. See [LICENSE](./LICENSE) for more information.

### Acknowledgments
- **[Groq](https://groq.com)** - For providing the world's fastest LLM inference engine
- **[Meta AI](https://ai.meta.com/)** - For the Llama 3.3 70B and Llama 3.1 8B models
- **[Vercel](https://vercel.com)** - For Next.js and frontend infrastructure inspiration
- **[FastAPI](https://fastapi.tiangolo.com/)** - For the high-performance Python backend framework
- **[Faker](https://faker.readthedocs.io/)** - For realistic synthetic data generation

### Repository Information
- **Author**: Kshitij Sharma
- **Year**: 2026
