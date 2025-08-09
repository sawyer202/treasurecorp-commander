#!/usr/bin/env python3
"""
Analyze TreasureCorp tweet engagement patterns
"""

import asyncio
from dao_monitoring_llm import DAOMonitoringLLM
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def analyze_engagement():
    """Analyze tweet engagement patterns"""
    logger.info("Analyzing TreasureCorp tweet engagement...")
    
    monitor = DAOMonitoringLLM()
    engagement_data = monitor.analyze_tweet_engagement(limit=30)
    
    if engagement_data:
        print("\n" + "="*80)
        print("TREASURECORP TWEET ENGAGEMENT ANALYSIS")
        print("="*80)
        
        print(f"\nTop 10 Performing Tweets (by engagement rate):")
        print("-" * 60)
        
        for i, tweet in enumerate(engagement_data[:10], 1):
            print(f"\n{i}. Engagement Rate: {tweet['engagement_rate']}%")
            print(f"   Impressions: {tweet['impressions']:,}")
            print(f"   Likes: {tweet['likes']} | Retweets: {tweet['retweets']} | Replies: {tweet['replies']}")
            print(f"   Date: {tweet['created_at']}")
            print(f"   Text: {tweet['text']}")
            print("-" * 60)
        
        # Engagement patterns
        avg_engagement = sum(t['engagement_rate'] for t in engagement_data) / len(engagement_data)
        high_performing = [t for t in engagement_data if t['engagement_rate'] > avg_engagement * 1.5]
        
        print(f"\n📊 INSIGHTS:")
        print(f"   Average Engagement Rate: {avg_engagement:.2f}%")
        print(f"   High Performing Tweets: {len(high_performing)}")
        print(f"   Total Tweets Analyzed: {len(engagement_data)}")
        
        if high_performing:
            print(f"\n🎯 PATTERNS IN HIGH-PERFORMING TWEETS:")
            for tweet in high_performing[:3]:
                print(f"   • {tweet['engagement_rate']}% - {tweet['text'][:80]}...")
    else:
        print("❌ Could not retrieve engagement data. Check API credentials.")

if __name__ == "__main__":
    analyze_engagement()