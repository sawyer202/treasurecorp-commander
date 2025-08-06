#!/usr/bin/env python3
"""
TreasureCorp Commander - Unified Deployment Script
Ties all components together for aggressive 2-month growth to 10K followers
"""

import os
import subprocess
import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime
import asyncio
import concurrent.futures
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TreasureCorpDeployment:
    """Unified deployment and orchestration system"""
    
    def __init__(self):
        self.base_dir = Path.cwd()
        self.components = {
            'dao_monitoring_llm': 'dao_monitoring_llm.py',
            'mobile_backend': 'mobile_app_backend.py', 
            'growth_config': 'aggressive_growth_config.py',
            'mobile_app': 'TreasureCorpCommander_App.tsx'
        }
        
    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        logger.info("🔍 Checking dependencies...")
        
        # Python dependencies
        python_deps = [
            'fastapi', 'uvicorn', 'anthropic', 'openai', 'tweepy',
            'python-telegram-bot', 'aiohttp', 'beautifulsoup4',
            'feedparser', 'Pillow', 'schedule', 'requests', 'sqlite3'
        ]
        
        missing_deps = []
        for dep in python_deps:
            try:
                __import__(dep.replace('-', '_'))
            except ImportError:
                missing_deps.append(dep)
        
        if missing_deps:
            logger.error(f"❌ Missing Python dependencies: {', '.join(missing_deps)}")
            logger.info("Installing missing dependencies...")
            for dep in missing_deps:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
        
        # Node.js dependencies (for mobile app)
        if not self._check_command('node'):
            logger.error("❌ Node.js not found. Please install Node.js for mobile app.")
            return False
        
        if not self._check_command('npm'):
            logger.error("❌ npm not found. Please install npm for mobile app.")
            return False
        
        logger.info("✅ All dependencies checked!")
        return True
    
    def _check_command(self, command):
        """Check if command exists in system PATH"""
        try:
            subprocess.check_output(['which', command], stderr=subprocess.DEVNULL)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def setup_environment(self):
        """Setup environment variables and configuration"""
        logger.info("⚙️ Setting up environment...")
        
        # Create .env file if it doesn't exist
        env_file = self.base_dir / '.env'
        if not env_file.exists():
            env_template = """
# TreasureCorp Commander Environment Configuration
# 2-Month Aggressive Growth Strategy

# AI APIs (Required)
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here

# Social Media APIs
TWITTER_BEARER_TOKEN=your_twitter_bearer_token
TWITTER_CONSUMER_KEY=your_twitter_consumer_key
TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_channel_id

LINKEDIN_USERNAME=your_linkedin_email
LINKEDIN_PASSWORD=your_linkedin_password

# Mobile App API
API_TOKEN=treasurecorp-mobile-2024
API_BASE_URL=http://localhost:8000

# Growth Configuration
AGGRESSIVE_MODE=true
GROWTH_TARGET=10000
TIMELINE_DAYS=60
POSTS_PER_DAY_TWITTER=15
POSTS_PER_DAY_LINKEDIN=5
POSTS_PER_DAY_TELEGRAM=12
"""
            
            with open(env_file, 'w') as f:
                f.write(env_template)
            
            logger.info(f"📝 Created environment template: {env_file}")
            logger.info("🚨 IMPORTANT: Please edit .env file with your actual API keys!")
        
        # Create directory structure
        directories = ['logs', 'temp', 'images', 'content_archive', 'mobile_build']
        for directory in directories:
            (self.base_dir / directory).mkdir(exist_ok=True)
        
        logger.info("✅ Environment setup complete!")
    
    def initialize_database(self):
        """Initialize SQLite database with all required tables"""
        logger.info("🗄️ Initializing database...")
        
        db_path = self.base_dir / 'dao_monitoring.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create tables for aggressive growth tracking
        tables = [
            '''CREATE TABLE IF NOT EXISTS monitored_content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                title TEXT NOT NULL,
                url TEXT UNIQUE,
                content_hash TEXT,
                discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed_at TIMESTAMP,
                summary TEXT,
                viral_score INTEGER DEFAULT 0,
                posted_twitter BOOLEAN DEFAULT 0,
                posted_linkedin BOOLEAN DEFAULT 0,
                posted_telegram BOOLEAN DEFAULT 0,
                engagement_twitter INTEGER DEFAULT 0,
                engagement_linkedin INTEGER DEFAULT 0,
                engagement_telegram INTEGER DEFAULT 0
            )''',
            
            '''CREATE TABLE IF NOT EXISTS growth_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                platform TEXT NOT NULL,
                followers INTEGER DEFAULT 0,
                following INTEGER DEFAULT 0,
                posts_count INTEGER DEFAULT 0,
                likes_received INTEGER DEFAULT 0,
                shares_received INTEGER DEFAULT 0,
                comments_received INTEGER DEFAULT 0,
                engagement_rate REAL DEFAULT 0.0,
                reach INTEGER DEFAULT 0,
                impressions INTEGER DEFAULT 0
            )''',
            
            '''CREATE TABLE IF NOT EXISTS viral_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_title TEXT NOT NULL,
                viral_score INTEGER NOT NULL,
                trending_hashtags TEXT,
                recommended_action TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                acted_upon BOOLEAN DEFAULT 0,
                result_engagement INTEGER DEFAULT 0
            )''',
            
            '''CREATE TABLE IF NOT EXISTS posting_schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                scheduled_time TIMESTAMP NOT NULL,
                content_type TEXT,
                content TEXT,
                status TEXT DEFAULT 'pending',
                posted_at TIMESTAMP,
                engagement_score INTEGER DEFAULT 0
            )''',
            
            '''CREATE TABLE IF NOT EXISTS growth_targets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                target_date DATE NOT NULL,
                target_followers INTEGER NOT NULL,
                current_followers INTEGER DEFAULT 0,
                daily_target REAL NOT NULL,
                progress_percentage REAL DEFAULT 0.0
            )'''
        ]
        
        for table_sql in tables:
            cursor.execute(table_sql)
        
        # Insert initial growth targets for 2-month aggressive plan
        targets = [
            ('twitter', '2024-04-01', 4500, 0, 75.0, 0.0),
            ('linkedin', '2024-04-01', 3500, 0, 58.3, 0.0),
            ('telegram', '2024-04-01', 2000, 0, 33.3, 0.0)
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO growth_targets 
            (platform, target_date, target_followers, current_followers, daily_target, progress_percentage)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', targets)
        
        conn.commit()
        conn.close()
        
        logger.info("✅ Database initialized with aggressive growth schema!")
    
    def build_mobile_app(self):
        """Build the React Native mobile app"""
        logger.info("📱 Building mobile app...")
        
        # Create package.json for mobile app
        mobile_dir = self.base_dir / 'TreasureCorpCommander'
        mobile_dir.mkdir(exist_ok=True)
        
        package_json = {
            "name": "treasurecorp-commander",
            "version": "1.0.0",
            "main": "node_modules/expo/AppEntry.js",
            "scripts": {
                "start": "expo start",
                "android": "expo start --android",
                "ios": "expo start --ios",
                "web": "expo start --web",
                "build:android": "eas build --platform android",
                "build:ios": "eas build --platform ios"
            },
            "dependencies": {
                "@expo/vector-icons": "^13.0.0",
                "@react-navigation/bottom-tabs": "^6.5.0",
                "@react-navigation/native": "^6.1.0",
                "@react-navigation/stack": "^6.3.0",
                "@reduxjs/toolkit": "^1.9.0",
                "axios": "^1.6.0",
                "expo": "~49.0.0",
                "react": "18.2.0",
                "react-native": "0.72.0",
                "react-native-chart-kit": "^6.12.0",
                "react-native-paper": "^5.11.0",
                "react-redux": "^8.1.0",
                "socket.io-client": "^4.7.0"
            },
            "devDependencies": {
                "@types/react": "~18.2.0",
                "typescript": "^5.1.0"
            }
        }
        
        with open(mobile_dir / 'package.json', 'w') as f:
            json.dump(package_json, f, indent=2)
        
        # Copy mobile app files
        mobile_files = [
            ('TreasureCorpCommander_App.tsx', 'App.tsx'),
            ('mobile_screens/DashboardScreen.tsx', 'src/screens/DashboardScreen.tsx')
        ]
        
        for src, dst in mobile_files:
            src_path = self.base_dir / src
            dst_path = mobile_dir / dst
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            
            if src_path.exists():
                import shutil
                shutil.copy2(src_path, dst_path)
        
        logger.info("✅ Mobile app structure created!")
    
    async def start_all_services(self):
        """Start all services concurrently"""
        logger.info("🚀 Starting all TreasureCorp Commander services...")
        
        services = []
        
        # Start FastAPI backend
        backend_process = subprocess.Popen([
            sys.executable, 'mobile_app_backend.py'
        ], cwd=self.base_dir)
        services.append(('Backend API', backend_process))
        
        # Start DAO monitoring
        monitor_process = subprocess.Popen([
            sys.executable, 'dao_monitoring_llm.py'
        ], cwd=self.base_dir)
        services.append(('DAO Monitor', monitor_process))
        
        # Start mobile app (if in development)
        try:
            mobile_dir = self.base_dir / 'TreasureCorpCommander'
            if mobile_dir.exists():
                mobile_process = subprocess.Popen([
                    'npm', 'start'
                ], cwd=mobile_dir)
                services.append(('Mobile App', mobile_process))
        except Exception as e:
            logger.warning(f"Could not start mobile app: {e}")
        
        logger.info("✅ All services started!")
        
        # Monitor services
        try:
            while True:
                await asyncio.sleep(30)
                for name, process in services:
                    if process.poll() is not None:
                        logger.error(f"❌ Service {name} has stopped!")
                        
        except KeyboardInterrupt:
            logger.info("🛑 Shutting down services...")
            for name, process in services:
                process.terminate()
                logger.info(f"Stopped {name}")
    
    def create_systemd_services(self):
        """Create systemd service files for production deployment"""
        logger.info("⚙️ Creating systemd services...")
        
        services = {
            'treasurecorp-backend.service': f'''[Unit]
Description=TreasureCorp Commander Backend API
After=network.target

[Service]
Type=simple
User=treasurecorp
WorkingDirectory={self.base_dir}
ExecStart={sys.executable} mobile_app_backend.py
Restart=always
RestartSec=10
Environment=PYTHONPATH={self.base_dir}

[Install]
WantedBy=multi-user.target
''',
            'treasurecorp-monitor.service': f'''[Unit]
Description=TreasureCorp DAO Monitoring Service
After=network.target

[Service]
Type=simple
User=treasurecorp
WorkingDirectory={self.base_dir}
ExecStart={sys.executable} dao_monitoring_llm.py
Restart=always
RestartSec=10
Environment=PYTHONPATH={self.base_dir}

[Install]
WantedBy=multi-user.target
'''
        }
        
        for filename, content in services.items():
            with open(self.base_dir / filename, 'w') as f:
                f.write(content)
        
        logger.info("✅ Systemd services created!")
        logger.info("To install:")
        logger.info("  sudo cp *.service /etc/systemd/system/")
        logger.info("  sudo systemctl enable treasurecorp-backend treasurecorp-monitor")
        logger.info("  sudo systemctl start treasurecorp-backend treasurecorp-monitor")
    
    def generate_deployment_summary(self):
        """Generate deployment summary and next steps"""
        summary = f"""
🚀 TreasureCorp Commander Deployment Complete!
================================================

📊 AGGRESSIVE 2-MONTH GROWTH STRATEGY
Target: 10,000 followers in 60 days
- Twitter: 4,500 followers (75/day)
- LinkedIn: 3,500 followers (58/day) 
- Telegram: 2,000 followers (33/day)

📱 COMPONENTS DEPLOYED:
✅ DAO Monitoring LLM (dao_monitoring_llm.py)
✅ Mobile App Backend API (mobile_app_backend.py)
✅ Aggressive Growth Config (aggressive_growth_config.py)
✅ React Native Mobile App (TreasureCorpCommander)
✅ Database Schema (dao_monitoring.db)

🎯 POSTING SCHEDULE (AGGRESSIVE):
- Twitter: 15 posts/day (every 1.6 hours)
- LinkedIn: 5 posts/day (professional limit)
- Telegram: 12 posts/day (high-frequency updates)

📱 MOBILE APP FEATURES:
- Real-time growth dashboard
- Viral content alerts
- Content creation AI
- Posting scheduler
- Analytics tracking
- Competitor analysis

🔧 NEXT STEPS:
1. Edit .env file with your API keys
2. Start services: python unified_deployment.py --start
3. Install mobile app: cd TreasureCorpCommander && npm install && npm start
4. Monitor progress at http://localhost:8000/docs
5. Use mobile app to manage on-the-go

⚡ GROWTH TACTICS INCLUDED:
- Automated content discovery
- Real-time viral alerts
- Cross-platform optimization
- Engagement automation
- Competitor tracking
- Performance analytics

🎉 Ready to grow from 0 to 10K followers in 2 months!

Deployment completed at: {datetime.now().isoformat()}
        """
        
        print(summary)
        
        # Save summary to file
        with open(self.base_dir / 'deployment_summary.txt', 'w') as f:
            f.write(summary)
    
    async def deploy(self):
        """Run complete deployment process"""
        logger.info("🚀 Starting TreasureCorp Commander deployment...")
        
        try:
            # Check dependencies
            if not self.check_dependencies():
                return False
            
            # Setup environment
            self.setup_environment()
            
            # Initialize database
            self.initialize_database()
            
            # Build mobile app
            self.build_mobile_app()
            
            # Create systemd services
            self.create_systemd_services()
            
            # Generate summary
            self.generate_deployment_summary()
            
            logger.info("✅ Deployment completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Deployment failed: {e}")
            return False

async def main():
    """Main deployment function"""
    deployment = TreasureCorpDeployment()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--start':
        # Start all services
        await deployment.start_all_services()
    else:
        # Run deployment
        success = await deployment.deploy()
        if success:
            print("\n🎯 To start all services:")
            print("python unified_deployment.py --start")
        else:
            print("\n❌ Deployment failed. Check logs for details.")

if __name__ == "__main__":
    asyncio.run(main())