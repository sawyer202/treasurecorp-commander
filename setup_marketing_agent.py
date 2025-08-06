#!/usr/bin/env python3
"""
Quick Setup Script for TreasureCorp Marketing Agent
Run this to install dependencies and set up environment
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    packages = [
        "anthropic",
        "tweepy", 
        "requests",
        "schedule",
        "python-dotenv"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def create_env_file():
    """Create .env file template"""
    env_content = """# TreasureCorp Marketing Agent Environment Variables

# Anthropic Claude API
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Twitter API (optional)
TWITTER_CONSUMER_KEY=your_twitter_consumer_key
TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

# LinkedIn API (optional)
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret

# Buffer API (optional)
BUFFER_ACCESS_TOKEN=your_buffer_access_token
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("Created .env file template")
    print("Please edit .env file with your actual API keys")

def create_simple_agent():
    """Create a simplified version for immediate use"""
    simple_agent = '''#!/usr/bin/env python3
"""
Simple TreasureCorp Marketing Agent - No external APIs required
"""

import anthropic
import os
from datetime import datetime

# Set your Anthropic API key here
ANTHROPIC_API_KEY = "your_api_key_here"

def generate_marketing_content():
    """Generate marketing content using Claude"""
    
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    topics = [
        "DAO treasury management challenges",
        "Multi-chain analytics benefits",
        "Treasury automation ROI", 
        "Governance transparency tools"
    ]
    
    for topic in topics:
        print(f"\\n{'='*60}")
        print(f"GENERATING CONTENT FOR: {topic}")
        print('='*60)
        
        # LinkedIn Post
        linkedin_prompt = f"""
        Create a professional LinkedIn post for TreasureCorp about {topic}.
        
        Requirements:
        - 150-200 words
        - Professional tone
        - Highlight multi-chain treasury analytics
        - Include hashtags #DAO #Treasury #Web3
        - End with engagement question
        
        TreasureCorp is a DAO treasury management platform that provides:
        - Multi-chain tracking (Ethereum, Arbitrum)
        - Automated reporting
        - Governance insights
        - Cost savings vs manual processes
        """
        
        try:
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=400,
                messages=[{"role": "user", "content": linkedin_prompt}]
            )
            
            linkedin_content = response.content[0].text
            print("\\nLINKEDIN POST:")
            print("-" * 30)
            print(linkedin_content)
            
            # Save to file
            filename = f"linkedin_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt"
            with open(filename, 'w') as f:
                f.write(linkedin_content)
            print(f"\\nSaved to: {filename}")
            
        except Exception as e:
            print(f"Error: {e}")
            print("Make sure to set your ANTHROPIC_API_KEY")

if __name__ == "__main__":
    generate_marketing_content()
'''
    
    with open('simple_marketing_agent.py', 'w') as f:
        f.write(simple_agent)
    
    print("Created simple_marketing_agent.py")

def main():
    print("Setting up TreasureCorp Marketing Agent...")
    
    # Install requirements
    try:
        install_requirements()
        print("✅ Dependencies installed")
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
    
    # Create environment file
    create_env_file()
    print("✅ Environment template created")
    
    # Create simple agent
    create_simple_agent()
    print("✅ Simple agent created")
    
    print("""
🚀 SETUP COMPLETE!

Next steps:
1. Get your Anthropic API key from console.anthropic.com
2. Edit the ANTHROPIC_API_KEY in simple_marketing_agent.py
3. Run: python simple_marketing_agent.py

For full functionality:
1. Edit .env file with all API keys
2. Run: python marketing_agent.py

Cost: ~$15-30/month for Claude API
    """)

if __name__ == "__main__":
    main()