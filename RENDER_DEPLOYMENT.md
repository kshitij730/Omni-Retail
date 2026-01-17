# 🚀 Render.com Deployment Guide

## 📋 Overview
Render.com is perfect for this project because it supports:
- ✅ Persistent disk storage (for SQLite databases)
- ✅ Python and Node.js applications
- ✅ Environment variables
- ✅ Free tier available

## 🏗️ Architecture on Render

You'll create **TWO services**:
1. **Backend Service** (Python/FastAPI) - Runs on port 8000
2. **Frontend Service** (Next.js) - Runs on port 3000

---

## 🔧 Step 1: Prepare Your Repository

### 1.1 Push to GitHub
```bash
git init
git add .
git commit -m "Ready for Render deployment"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

---

## 🎯 Step 2: Deploy Backend Service

### 2.1 Create Backend Service
1. Go to [render.com](https://render.com) and sign in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `omni-retail-backend`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python setup_dbs.py
     ```
   - **Start Command**: 
     ```bash
     python src/server.py
     ```

### 2.2 Add Environment Variables
In the service settings, add:
- **Key**: `GROQ_API_KEY`
- **Value**: Your actual Groq API key

### 2.3 Add Persistent Disk (Important!)
1. Go to **"Disks"** tab
2. Click **"Add Disk"**
3. Configure:
   - **Name**: `omni-data`
   - **Mount Path**: `/opt/render/project/src/data`
   - **Size**: 1 GB (free tier)

### 2.4 Deploy
Click **"Create Web Service"**

Your backend will be available at: `https://omni-retail-backend.onrender.com`

---

## 🎨 Step 3: Deploy Frontend Service

### 3.1 Create Frontend Service
1. Click **"New +"** → **"Web Service"**
2. Connect the same GitHub repository
3. Configure:
   - **Name**: `omni-retail-frontend`
   - **Region**: Same as backend
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: `Node`
   - **Build Command**: 
     ```bash
     npm install && npm run build
     ```
   - **Start Command**: 
     ```bash
     npm start
     ```

### 3.2 Add Environment Variable
Add the backend URL:
- **Key**: `NEXT_PUBLIC_API_URL`
- **Value**: `https://omni-retail-backend.onrender.com`

### 3.3 Deploy
Click **"Create Web Service"**

Your frontend will be available at: `https://omni-retail-frontend.onrender.com`

---

## 🔗 Step 4: Connect Frontend to Backend

Update your Next.js config to use the backend URL:

In `next.config.mjs`, update the rewrites section:
```javascript
async rewrites() {
    return [
        {
            source: "/api/:path*",
            destination: process.env.NEXT_PUBLIC_API_URL + "/api/:path*",
        },
    ];
}
```

---

## ✅ Verification

1. Visit your backend: `https://omni-retail-backend.onrender.com/`
   - Should show: `{"status": "Omni-Agent API is live"}`

2. Visit your frontend: `https://omni-retail-frontend.onrender.com`
   - Should show the Omni-Retail UI

3. Test a query through the UI

---

## 💡 Tips

- **Free Tier**: Services spin down after 15 minutes of inactivity (first request may be slow)
- **Logs**: Check service logs in Render dashboard for debugging
- **Database**: The persistent disk ensures your SQLite databases survive restarts
- **Updates**: Push to GitHub and Render auto-deploys

---

## 🐛 Troubleshooting

### Backend won't start
- Check logs in Render dashboard
- Verify `GROQ_API_KEY` is set
- Ensure persistent disk is mounted

### Frontend can't connect to backend
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check CORS settings in `src/server.py`
- Ensure both services are running

### Database not found
- Verify persistent disk is mounted at `/opt/render/project/src/data`
- Check that `setup_dbs.py` ran successfully in build logs

---

**Your Omni-Retail system is now production-ready on Render! 🎉**
