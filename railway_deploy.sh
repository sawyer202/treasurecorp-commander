#!/bin/bash
# TreasureCorp Commander - Railway Deployment Script

echo "🚀 Deploying TreasureCorp Commander to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login to Railway
echo "🔐 Please login to Railway..."
railway login

# Create new project
echo "📝 Creating Railway project..."
railway init

# Set environment variables
echo "⚙️ Setting environment variables..."
echo "Please set these environment variables in Railway dashboard:"
echo ""
echo "Required Variables:"
echo "ANTHROPIC_API_KEY=your_anthropic_key_here"
echo "OPENAI_API_KEY=your_openai_key_here"
echo "TWITTER_BEARER_TOKEN=your_twitter_bearer_token"
echo "TWITTER_CONSUMER_KEY=your_twitter_consumer_key"
echo "TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret"
echo "TWITTER_ACCESS_TOKEN=your_twitter_access_token"
echo "TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret"
echo "TELEGRAM_BOT_TOKEN=your_telegram_bot_token"
echo "TELEGRAM_CHAT_ID=your_telegram_channel_id"
echo "LINKEDIN_USERNAME=your_linkedin_email"
echo "LINKEDIN_PASSWORD=your_linkedin_password"
echo "API_TOKEN=treasurecorp-mobile-2024"
echo ""

# Automated environment variable setup (if you want to script it)
read -p "Do you want to set environment variables now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Setting environment variables..."
    
    railway variables:set NODE_ENV=production
    railway variables:set API_TOKEN=treasurecorp-mobile-2024
    railway variables:set AGGRESSIVE_MODE=true
    railway variables:set GROWTH_TARGET=10000
    railway variables:set TIMELINE_DAYS=60
    railway variables:set POSTS_PER_DAY_TWITTER=15
    railway variables:set POSTS_PER_DAY_LINKEDIN=5
    railway variables:set POSTS_PER_DAY_TELEGRAM=12
    
    echo "⚠️  You still need to set your API keys manually in Railway dashboard!"
fi

# Deploy to Railway
echo "🚀 Deploying to Railway..."
railway up

echo "✅ Deployment initiated!"
echo ""
echo "📱 Next steps:"
echo "1. Go to your Railway dashboard"
echo "2. Set your API keys in environment variables"
echo "3. Your app will be available at: https://your-app.railway.app"
echo "4. Deploy mobile app to Vercel (run ./vercel_deploy.sh)"
echo ""
echo "🎯 Your TreasureCorp Commander will be live in a few minutes!"