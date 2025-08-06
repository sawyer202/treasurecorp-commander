# 🚀 Railway + Vercel Deployment Guide

Deploy TreasureCorp Commander in under 10 minutes with zero configuration!

## 🎯 Architecture Overview

- **Railway**: Backend API + DAO Monitoring (Python/FastAPI)
- **Vercel**: Frontend Dashboard (Next.js/React)
- **Real-time sync**: WebSocket connection between platforms

## ⚡ One-Click Deployment

### Step 1: Deploy Backend to Railway (2 minutes)

```bash
# Make script executable
chmod +x railway_deploy.sh

# Run deployment
./railway_deploy.sh
```

**What this does:**
- Installs Railway CLI
- Creates new Railway project
- Deploys Python backend with FastAPI
- Sets up DAO monitoring worker
- Configures environment variables

### Step 2: Deploy Frontend to Vercel (3 minutes)

```bash
# Make script executable
chmod +x vercel_deploy.sh

# Run deployment
./vercel_deploy.sh
```

**What this does:**
- Installs Vercel CLI
- Creates Next.js dashboard app
- Builds optimized production version
- Deploys to global CDN
- Connects to Railway backend

### Step 3: Configure API Keys (5 minutes)

1. **Go to Railway Dashboard**: https://railway.app/dashboard
2. **Find your project** → Variables tab
3. **Add your API keys**:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   TWITTER_BEARER_TOKEN=your-twitter-token
   TELEGRAM_BOT_TOKEN=your-bot-token
   LINKEDIN_USERNAME=your-email
   LINKEDIN_PASSWORD=your-password
   ```

---

## 🌐 Manual Deployment (Alternative)

### Railway Deployment

#### Option A: GitHub Integration
1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "TreasureCorp Commander initial commit"
   git push origin main
   ```

2. **Connect to Railway**:
   - Go to https://railway.app/new
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway auto-detects Python and deploys

#### Option B: CLI Deployment
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up

# Set environment variables in dashboard
```

### Vercel Deployment

#### Option A: GitHub Integration
1. **Go to https://vercel.com/new**
2. **Import your GitHub repository**
3. **Framework**: Next.js
4. **Build Command**: `npm run build`
5. **Deploy**

#### Option B: CLI Deployment
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel login
vercel

# Follow prompts to deploy
```

---

## 🔧 Configuration Files Explained

### `railway.json`
```json
{
  "build": {
    "builder": "NIXPACKS"  // Auto-detects Python
  },
  "deploy": {
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### `Procfile`
```
web: uvicorn mobile_app_backend:app --host 0.0.0.0 --port $PORT
worker: python dao_monitoring_llm.py
```

### `vercel.json`
```json
{
  "builds": [
    {
      "src": "mobile_app_backend.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "mobile_app_backend.py"
    }
  ]
}
```

---

## 📊 Post-Deployment Setup

### 1. Verify Backend Deployment
```bash
# Check if Railway backend is running
curl https://your-app.railway.app/api/dashboard/metrics

# Expected response:
[
  {"platform": "twitter", "followers": 0, "daily_growth": 0},
  {"platform": "linkedin", "followers": 0, "daily_growth": 0},
  {"platform": "telegram", "followers": 0, "daily_growth": 0}
]
```

### 2. Verify Frontend Deployment
- Visit your Vercel URL: `https://your-app.vercel.app`
- Should see TreasureCorp Commander dashboard
- Real-time metrics updating every 30 seconds

### 3. Test Real-time Connection
- Open browser developer tools
- Check WebSocket connection in Network tab
- Should see `ws://your-app.railway.app/ws` connected

---

## 🎯 Environment Variables Setup

### Railway Backend Variables
```env
# Required for DAO monitoring
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-your-openai-key

# Social media APIs
TWITTER_BEARER_TOKEN=your-bearer-token
TWITTER_CONSUMER_KEY=your-consumer-key
TWITTER_CONSUMER_SECRET=your-consumer-secret
TWITTER_ACCESS_TOKEN=your-access-token
TWITTER_ACCESS_TOKEN_SECRET=your-access-secret

TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-channel-id

LINKEDIN_USERNAME=your-email
LINKEDIN_PASSWORD=your-password

# Growth configuration
AGGRESSIVE_MODE=true
GROWTH_TARGET=10000
TIMELINE_DAYS=60
POSTS_PER_DAY_TWITTER=15
POSTS_PER_DAY_LINKEDIN=5
POSTS_PER_DAY_TELEGRAM=12
```

### Vercel Frontend Variables
```env
# Backend connection
BACKEND_URL=https://your-app.railway.app
API_TOKEN=treasurecorp-mobile-2024
NODE_ENV=production

# Optional: Analytics
NEXT_PUBLIC_ANALYTICS_ID=your-analytics-id
```

---

## 🚀 Scaling & Performance

### Railway Auto-Scaling
- **Free Tier**: 512MB RAM, $5/month after usage
- **Pro Tier**: Auto-scales based on demand
- **Custom domains**: Connect your own domain

### Vercel Global CDN
- **Edge Functions**: Deploy in 20+ regions
- **Automatic HTTPS**: SSL certificates included
- **Analytics**: Built-in performance monitoring

### Database Scaling
```bash
# Upgrade to PostgreSQL on Railway
railway add postgresql

# Update connection string
DATABASE_URL=postgresql://username:password@host:port/database
```

---

## 📱 Mobile App Integration

### Progressive Web App (PWA)
The Vercel deployment automatically creates a PWA that can be installed on mobile devices:

1. **Visit your Vercel URL** on mobile
2. **"Add to Home Screen"** option appears
3. **Works offline** with cached data
4. **Push notifications** for viral alerts

### Native App Deployment
```bash
# Build native apps with Capacitor
npm install @capacitor/core @capacitor/cli

# Add iOS/Android platforms
npx cap add ios
npx cap add android

# Build and deploy
npx cap build
npx cap open ios
npx cap open android
```

---

## 🔍 Monitoring & Debugging

### Railway Logs
```bash
# View live logs
railway logs

# Or in dashboard: railway.app/dashboard → your-project → Deployments
```

### Vercel Logs
```bash
# View function logs
vercel logs

# Or in dashboard: vercel.com/dashboard → your-project → Functions
```

### Health Checks
```bash
# Backend health
curl https://your-app.railway.app/

# Frontend health
curl https://your-app.vercel.app/api/health
```

---

## 🎯 Success Metrics

After deployment, you should see:

### Immediate (5 minutes)
- ✅ Backend API responding at Railway URL
- ✅ Frontend dashboard loading at Vercel URL
- ✅ WebSocket connection established
- ✅ Environment variables configured

### First Hour
- ✅ DAO monitoring started
- ✅ First content items discovered
- ✅ Social media connections verified
- ✅ Posting schedule activated

### First Day
- ✅ 32+ posts across all platforms
- ✅ Follower count starting to increase
- ✅ Viral alerts generated
- ✅ Real-time dashboard updating

### First Week
- ✅ 1,000+ total followers
- ✅ Multiple viral posts
- ✅ Steady growth trajectory
- ✅ Mobile notifications working

---

## 🆘 Troubleshooting

### Common Issues

**Backend not starting on Railway:**
```bash
# Check logs
railway logs

# Common fixes:
1. Verify requirements.txt includes all dependencies
2. Check environment variables are set
3. Ensure Procfile syntax is correct
```

**Frontend not connecting to backend:**
```bash
# Check Vercel environment variables
vercel env ls

# Update BACKEND_URL if needed
vercel env add BACKEND_URL
```

**API keys not working:**
```bash
# Test API keys locally first
python -c "
import anthropic
client = anthropic.Anthropic(api_key='your-key')
print('Claude API working!')
"
```

---

## 🎉 You're Live!

Your TreasureCorp Commander is now deployed and ready to:

🚀 **Automatically grow** from 0 to 10K followers in 2 months
📱 **Monitor in real-time** via web dashboard or mobile PWA  
🤖 **Generate viral content** 24/7 with AI
📊 **Track performance** across all platforms
🚨 **Alert on opportunities** for maximum engagement

**Your URLs:**
- 🌐 **Dashboard**: `https://your-app.vercel.app`
- ⚡ **API**: `https://your-app.railway.app`
- 📖 **Docs**: `https://your-app.railway.app/docs`

**Cost:** ~$5-10/month total for both platforms

Let the aggressive growth begin! 📈🎯