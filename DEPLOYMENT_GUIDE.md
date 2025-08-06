# 🚀 TreasureCorp Commander Deployment Guide

Complete step-by-step deployment for aggressive 2-month growth to 10K followers.

## 🎯 Prerequisites

### 1. System Requirements
- **Python 3.8+** (for AI/backend)
- **Node.js 18+** (for mobile app)
- **Git** (for version control)
- **Domain name** (optional, for production)

### 2. API Keys Required
- **Anthropic Claude API** (for content generation)
- **OpenAI API** (backup LLM)
- **Twitter API v2** (for posting/monitoring)
- **Telegram Bot Token** (for community)
- **LinkedIn credentials** (for professional posts)

---

## 📋 Step 1: Local Development Setup

### Clone and Setup
```bash
# 1. Navigate to your project directory
cd /mnt/c/Users/test/Treasurecorp

# 2. Install Python dependencies
python -m pip install --upgrade pip
python -m pip install fastapi uvicorn anthropic openai tweepy python-telegram-bot
python -m pip install aiohttp beautifulsoup4 feedparser Pillow schedule requests

# 3. Run the unified deployment script
python unified_deployment.py
```

### Configure Environment
```bash
# 4. Edit the .env file with your API keys
cp .env.template .env
nano .env  # or use any text editor
```

**Add your API keys to `.env`:**
```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-your-openai-key-here
TWITTER_BEARER_TOKEN=your-twitter-bearer-token
TWITTER_CONSUMER_KEY=your-twitter-consumer-key
TWITTER_CONSUMER_SECRET=your-twitter-consumer-secret
TWITTER_ACCESS_TOKEN=your-twitter-access-token
TWITTER_ACCESS_TOKEN_SECRET=your-twitter-access-token-secret
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-telegram-channel-id
LINKEDIN_USERNAME=your-linkedin-email
LINKEDIN_PASSWORD=your-linkedin-password
```

### Test Local Deployment
```bash
# 5. Start all services locally
python unified_deployment.py --start

# This starts:
# - Backend API at http://localhost:8000
# - DAO monitoring service
# - WebSocket connections for real-time updates
```

---

## 📱 Step 2: Mobile App Setup

### Install Mobile App
```bash
# 1. Setup mobile app
cd TreasureCorpCommander
npm install

# 2. Install Expo CLI globally
npm install -g @expo/cli

# 3. Start the mobile app
npm start
# or
expo start
```

### Test Mobile App
- **iOS**: Scan QR code with iPhone camera
- **Android**: Scan QR code with Expo Go app
- **Web**: Press 'w' in terminal to open web version

---

## 🌐 Step 3: Production Deployment Options

### Option A: VPS/Cloud Server (Recommended)

#### 1. DigitalOcean/AWS/Linode Setup
```bash
# Create a VPS with Ubuntu 22.04
# SSH into your server
ssh root@your-server-ip

# Install dependencies
apt update && apt upgrade -y
apt install python3 python3-pip nodejs npm nginx certbot python3-certbot-nginx -y

# Clone your project
git clone https://github.com/your-username/treasurecorp-commander.git
cd treasurecorp-commander

# Install Python packages
pip3 install -r requirements.txt

# Setup environment
cp .env.template .env
nano .env  # Add your API keys
```

#### 2. Configure Nginx
```bash
# Create Nginx config
sudo nano /etc/nginx/sites-available/treasurecorp-commander

# Add this configuration:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}

# Enable the site
sudo ln -s /etc/nginx/sites-available/treasurecorp-commander /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com
```

#### 3. Setup Systemd Services
```bash
# Copy service files
sudo cp treasurecorp-backend.service /etc/systemd/system/
sudo cp treasurecorp-monitor.service /etc/systemd/system/

# Enable and start services
sudo systemctl daemon-reload
sudo systemctl enable treasurecorp-backend treasurecorp-monitor
sudo systemctl start treasurecorp-backend treasurecorp-monitor

# Check status
sudo systemctl status treasurecorp-backend
sudo systemctl status treasurecorp-monitor
```

### Option B: Docker Deployment

#### 1. Create Dockerfile
```dockerfile
# Create Dockerfile in project root
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "unified_deployment.py", "--start"]
```

#### 2. Docker Compose
```yaml
# Create docker-compose.yml
version: '3.8'
services:
  treasurecorp-backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - TWITTER_BEARER_TOKEN=${TWITTER_BEARER_TOKEN}
    volumes:
      - ./dao_monitoring.db:/app/dao_monitoring.db
      - ./logs:/app/logs
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - treasurecorp-backend
    restart: unless-stopped
```

#### 3. Deploy with Docker
```bash
# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Option C: Railway/Heroku/Vercel (Easy Deploy)

#### Railway Deployment
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up

# Set environment variables
railway variables:set ANTHROPIC_API_KEY=your-key-here
railway variables:set TWITTER_BEARER_TOKEN=your-token-here
```

---

## 📱 Step 4: Mobile App Production Build

### iOS App Store
```bash
# 1. Install EAS CLI
npm install -g eas-cli

# 2. Configure EAS
eas login
eas build:configure

# 3. Build for iOS
eas build --platform ios --profile production

# 4. Submit to App Store
eas submit --platform ios
```

### Android Play Store
```bash
# 1. Build Android APK
eas build --platform android --profile production

# 2. Submit to Play Store
eas submit --platform android
```

### Web Deployment
```bash
# 1. Build web version
expo build:web

# 2. Deploy to Netlify/Vercel
# Upload dist folder to your hosting provider
```

---

## 🔧 Step 5: Production Configuration

### 1. Environment Variables (Production)
```env
# Production .env
NODE_ENV=production
API_BASE_URL=https://your-domain.com
DATABASE_URL=postgresql://user:password@host:port/database
REDIS_URL=redis://localhost:6379

# Rate limiting (aggressive growth)
RATE_LIMIT_TWITTER=15
RATE_LIMIT_LINKEDIN=5
RATE_LIMIT_TELEGRAM=12

# Monitoring
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=info
```

### 2. Database Migration (Optional: PostgreSQL)
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb treasurecorp_commander

# Update connection string in .env
DATABASE_URL=postgresql://username:password@localhost:5432/treasurecorp_commander
```

### 3. Redis for Caching (Optional)
```bash
# Install Redis
sudo apt install redis-server

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

---

## 📊 Step 6: Monitoring & Analytics

### 1. Setup Logging
```bash
# Create log rotation
sudo nano /etc/logrotate.d/treasurecorp

# Add:
/home/treasurecorp/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    create 644 treasurecorp treasurecorp
}
```

### 2. Setup Monitoring Dashboard
```bash
# Access monitoring at:
http://your-domain.com/dashboard

# API documentation:
http://your-domain.com/docs

# Real-time WebSocket:
ws://your-domain.com/ws
```

### 3. Health Checks
```bash
# Check all services
curl http://your-domain.com/api/health
curl http://your-domain.com/api/dashboard/metrics
```

---

## 🚨 Step 7: Go Live Checklist

### Pre-Launch
- [ ] All API keys configured
- [ ] Database initialized
- [ ] Services running and healthy
- [ ] Mobile app tested on devices
- [ ] SSL certificate installed
- [ ] Monitoring dashboard accessible
- [ ] Growth targets configured
- [ ] Social media accounts connected

### Launch Day
```bash
# Start aggressive growth campaign
python -c "
from aggressive_growth_config import AggressiveGrowthConfig
config = AggressiveGrowthConfig()
print('🚀 LAUNCHING 2-MONTH GROWTH CAMPAIGN!')
print(f'Target: {sum(config.follower_targets.values())} followers')
print('Ready to dominate social media! 💪')
"

# Monitor in real-time
tail -f logs/dao_monitoring.log
```

### Post-Launch
- [ ] Monitor growth metrics daily
- [ ] Respond to viral alerts immediately
- [ ] Adjust posting schedule based on engagement
- [ ] Track competitor movements
- [ ] Scale server resources if needed

---

## 🎯 Success Metrics

**Daily Targets:**
- Twitter: +75 followers/day
- LinkedIn: +58 followers/day
- Telegram: +33 followers/day

**Weekly Milestones:**
- Week 2: 1,300 total followers
- Week 4: 3,750 total followers
- Week 6: 6,850 total followers
- Week 8: 10,000 total followers ✅

---

## 🆘 Troubleshooting

### Common Issues
```bash
# Service not starting
sudo systemctl status treasurecorp-backend
sudo journalctl -u treasurecorp-backend -f

# Database connection issues
python -c "import sqlite3; print('SQLite OK')"

# API key issues
python -c "
import os
from dao_monitoring_llm import DAOMonitoringLLM
monitor = DAOMonitoringLLM()
print('API keys loaded successfully!')
"

# Mobile app build issues
expo doctor
npm cache clean --force
```

### Support
- Check logs in `logs/` directory
- Review API documentation at `/docs`
- Monitor real-time metrics at `/dashboard`

---

## 🎉 You're Ready!

Your TreasureCorp Commander is now deployed and ready to grow from 0 to 10K followers in 2 months!

**Access Points:**
- 🌐 Web Dashboard: `https://your-domain.com`
- 📱 Mobile App: Available on devices via Expo
- 🔧 API Docs: `https://your-domain.com/docs`
- 📊 Real-time Metrics: WebSocket connection

**Next Steps:**
1. Launch aggressive posting campaign
2. Monitor viral alerts daily
3. Engage with community in real-time
4. Track progress toward 10K goal

Let the growth begin! 🚀📈