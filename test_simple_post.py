#!/usr/bin/env python3
"""
Simple test to post directly to Twitter without LLM processing
"""

import tweepy
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_twitter_post():
    """Test direct Twitter posting"""
    try:
        # Setup Twitter API
        client = tweepy.Client(
            bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
            consumer_key=os.getenv("TWITTER_CONSUMER_KEY"),
            consumer_secret=os.getenv("TWITTER_CONSUMER_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
            wait_on_rate_limit=True
        )
        
        # Test post content
        test_message = """🚀 TreasureCorp DAO Monitor Test

Testing automatic post creation system. Monitoring:
• Governance proposals
• DAO community updates  
• DeFi protocol changes

#DAO #Web3 #DeFi #Governance #TreasureCorp"""

        # Post to Twitter
        response = client.create_tweet(text=test_message)
        logger.info(f"✅ Successfully posted to Twitter! Tweet ID: {response.data['id']}")
        logger.info(f"🔗 https://twitter.com/Treasure_Corp/status/{response.data['id']}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Twitter posting failed: {e}")
        return False

if __name__ == "__main__":
    logger.info("Testing Twitter posting...")
    success = test_twitter_post()
    if success:
        logger.info("✅ Test completed successfully!")
    else:
        logger.info("❌ Test failed - check API credentials")