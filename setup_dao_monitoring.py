#!/usr/bin/env python3
"""
Setup script for TreasureCorp DAO Monitoring LLM
Installs dependencies and configures the system
"""

import os
import subprocess
import sys
from pathlib import Path

def install_requirements():
    """Install required Python packages"""
    requirements = [
        'anthropic>=0.25.0',
        'openai>=1.0.0',
        'tweepy>=4.14.0',
        'python-telegram-bot>=20.0',
        'linkedin-api>=2.0.0',
        'aiohttp>=3.8.0',
        'beautifulsoup4>=4.12.0',
        'feedparser>=6.0.0',
        'Pillow>=10.0.0',
        'schedule>=1.2.0',
        'requests>=2.31.0',
        'sqlite3'  # Built into Python
    ]
    
    print("Installing required packages...")
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package}")

def setup_environment():
    """Create environment variables template"""
    env_template = """
# TreasureCorp DAO Monitoring LLM Environment Variables
# Copy this to .env and fill in your actual API keys

# AI APIs
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Twitter API v2
TWITTER_BEARER_TOKEN=your_twitter_bearer_token
TWITTER_CONSUMER_KEY=your_twitter_consumer_key
TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_channel_id

# LinkedIn API
LINKEDIN_USERNAME=your_linkedin_email
LINKEDIN_PASSWORD=your_linkedin_password

# Database
DATABASE_PATH=dao_monitoring.db

# Monitoring Configuration
CHECK_INTERVAL_HOURS=6
MAX_POSTS_PER_DAY=8
CONTENT_RETENTION_DAYS=30
"""
    
    env_file = Path('.env.template')
    with open(env_file, 'w') as f:
        f.write(env_template)
    
    print(f"✓ Created environment template: {env_file}")
    print("Please copy .env.template to .env and fill in your API keys")

def create_directory_structure():
    """Create necessary directories"""
    directories = [
        'logs',
        'images',
        'temp',
        'content_archive',
        'reports'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}/")

def setup_database():
    """Initialize the SQLite database"""
    import sqlite3
    
    db_path = 'dao_monitoring.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monitored_content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT UNIQUE,
            content_hash TEXT,
            discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            processed_at TIMESTAMP,
            summary TEXT,
            posted_twitter BOOLEAN DEFAULT 0,
            posted_linkedin BOOLEAN DEFAULT 0,
            posted_telegram BOOLEAN DEFAULT 0,
            engagement_score INTEGER DEFAULT 0,
            retweets INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0,
            shares INTEGER DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dao_proposals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dao_name TEXT NOT NULL,
            proposal_id TEXT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT,
            votes_for INTEGER DEFAULT 0,
            votes_against INTEGER DEFAULT 0,
            end_date TIMESTAMP,
            url TEXT UNIQUE,
            discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS growth_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            platform TEXT NOT NULL,
            followers INTEGER DEFAULT 0,
            posts_count INTEGER DEFAULT 0,
            engagement_rate REAL DEFAULT 0.0,
            reach INTEGER DEFAULT 0,
            impressions INTEGER DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS content_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_id INTEGER,
            platform TEXT,
            post_id TEXT,
            likes INTEGER DEFAULT 0,
            shares INTEGER DEFAULT 0,
            comments INTEGER DEFAULT 0,
            reach INTEGER DEFAULT 0,
            posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (content_id) REFERENCES monitored_content (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print(f"✓ Database initialized: {db_path}")

def create_systemd_service():
    """Create a systemd service file for Linux systems"""
    service_content = """[Unit]
Description=TreasureCorp DAO Monitoring LLM
After=network.target

[Service]
Type=simple
User=treasurecorp
WorkingDirectory={working_dir}
ExecStart={python_path} dao_monitoring_llm.py
Restart=always
RestartSec=10
Environment=PYTHONPATH={working_dir}

[Install]
WantedBy=multi-user.target
""".format(
        working_dir=os.getcwd(),
        python_path=sys.executable
    )
    
    service_file = Path('treasurecorp-dao-monitor.service')
    with open(service_file, 'w') as f:
        f.write(service_content)
    
    print(f"✓ Created systemd service file: {service_file}")
    print("To install as a system service:")
    print(f"  sudo cp {service_file} /etc/systemd/system/")
    print("  sudo systemctl enable treasurecorp-dao-monitor")
    print("  sudo systemctl start treasurecorp-dao-monitor")

def setup_logging():
    """Create logging configuration"""
    log_config = """
import logging
import logging.handlers
from pathlib import Path

def setup_logging():
    # Create logs directory
    Path('logs').mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # Console handler
            logging.StreamHandler(),
            # File handler with rotation
            logging.handlers.RotatingFileHandler(
                'logs/dao_monitoring.log',
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
        ]
    )
    
    # Separate handler for errors
    error_handler = logging.handlers.RotatingFileHandler(
        'logs/dao_monitoring_errors.log',
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    
    # Add error handler to root logger
    logging.getLogger().addHandler(error_handler)
    
    return logging.getLogger(__name__)
"""
    
    with open('logging_config.py', 'w') as f:
        f.write(log_config)
    
    print("✓ Created logging configuration")

def create_monitoring_dashboard():
    """Create a simple web dashboard for monitoring"""
    dashboard_code = """#!/usr/bin/env python3
import sqlite3
from flask import Flask, render_template, jsonify
import json
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/metrics')
def get_metrics():
    conn = sqlite3.connect('dao_monitoring.db')
    cursor = conn.cursor()
    
    # Get recent content
    cursor.execute('''
        SELECT COUNT(*) as total,
               SUM(posted_twitter) as twitter_posts,
               SUM(posted_linkedin) as linkedin_posts,
               SUM(posted_telegram) as telegram_posts
        FROM monitored_content 
        WHERE discovered_at > datetime('now', '-7 days')
    ''')
    
    metrics = cursor.fetchone()
    
    conn.close()
    
    return jsonify({
        'total_content': metrics[0],
        'twitter_posts': metrics[1],
        'linkedin_posts': metrics[2],
        'telegram_posts': metrics[3],
        'last_updated': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
"""
    
    # Create templates directory
    Path('templates').mkdir(exist_ok=True)
    
    dashboard_html = """<!DOCTYPE html>
<html>
<head>
    <title>TreasureCorp DAO Monitor Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #1a1a1a; color: #fff; }
        .metric { background: #2a2a2a; padding: 20px; margin: 10px; border-radius: 8px; }
        .metric h3 { color: #00ff88; margin-top: 0; }
        .metric .value { font-size: 2em; font-weight: bold; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
        h1 { color: #00ff88; text-align: center; }
    </style>
</head>
<body>
    <h1>TreasureCorp DAO Monitoring Dashboard</h1>
    <div class="grid">
        <div class="metric">
            <h3>Total Content (7 days)</h3>
            <div class="value" id="total-content">-</div>
        </div>
        <div class="metric">
            <h3>Twitter Posts</h3>
            <div class="value" id="twitter-posts">-</div>
        </div>
        <div class="metric">
            <h3>LinkedIn Posts</h3>
            <div class="value" id="linkedin-posts">-</div>
        </div>
        <div class="metric">
            <h3>Telegram Posts</h3>
            <div class="value" id="telegram-posts">-</div>
        </div>
    </div>
    
    <script>
        function updateMetrics() {
            fetch('/api/metrics')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('total-content').textContent = data.total_content;
                    document.getElementById('twitter-posts').textContent = data.twitter_posts;
                    document.getElementById('linkedin-posts').textContent = data.linkedin_posts;
                    document.getElementById('telegram-posts').textContent = data.telegram_posts;
                });
        }
        
        updateMetrics();
        setInterval(updateMetrics, 60000); // Update every minute
    </script>
</body>
</html>"""
    
    with open('dashboard.py', 'w') as f:
        f.write(dashboard_code)
    
    with open('templates/dashboard.html', 'w') as f:
        f.write(dashboard_html)
    
    print("✓ Created monitoring dashboard")
    print("Install Flask to use: pip install flask")
    print("Run with: python dashboard.py")

def main():
    """Run the complete setup"""
    print("🚀 Setting up TreasureCorp DAO Monitoring LLM...")
    print("=" * 50)
    
    # Install packages
    install_requirements()
    print()
    
    # Setup environment
    setup_environment()
    print()
    
    # Create directories
    create_directory_structure()
    print()
    
    # Setup database
    setup_database()
    print()
    
    # Setup logging
    setup_logging()
    print()
    
    # Create service file
    create_systemd_service()
    print()
    
    # Create dashboard
    create_monitoring_dashboard()
    print()
    
    print("=" * 50)
    print("🎉 Setup complete!")
    print()
    print("Next steps:")
    print("1. Copy .env.template to .env and add your API keys")
    print("2. Test the system: python dao_monitoring_llm.py")
    print("3. Monitor with dashboard: python dashboard.py")
    print("4. Check logs in logs/ directory")
    print()
    print("Growth targets:")
    print("📊 Twitter: 4,000 followers")
    print("💼 LinkedIn: 3,500 followers") 
    print("📱 Telegram: 2,500 followers")
    print("🎯 Total: 10,000 followers")
    print()
    print("Expected timeline: 6 months with aggressive growth strategy")

if __name__ == "__main__":
    main()