# Omni-Retail: All Commands

Here is the complete list of commands to set up and run the system from scratch.

## 1. Prerequisites
Ensure you have Python (3.10+) and Node.js (18+) installed.

## 2. Python Backend Setup
Run these commands in the `omni_retail` directory:

```powershell
# Create a virtual environment (Optional but Recommended)
python -m venv venv
.\venv\Scripts\activate

# Install Python Dependencies
pip install -r requirements.txt

# Set your Google Gemini API Key
set GOOGLE_API_KEY=your_actual_api_key_here
```

## 3. Database Generation
Generate the large synthetic dataset:

```powershell
python setup_dbs.py
```

## 4. Frontend Setup
Install the web dependencies:

```powershell
cd omni-retail-web
npm install
cd ..
```

## 5. Running the System
You have two options:

### Option A: The "One-Click" Script (Recommended)
This launches both the Backend API and the Frontend Web App.

```powershell
.\run_all.bat
```

### Option B: Manual Start
Open two terminal windows.

**Terminal 1 (Backend):**
```powershell
python -m uvicorn src.server:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 (Frontend):**
```powershell
cd omni-retail-web
npm run dev
```

## 6. Running the Console Demo (Optional)
If you just want to see the agents talk in the terminal without the web UI:

```powershell
python demo.py
```
