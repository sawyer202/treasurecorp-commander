#!/usr/bin/env python3
"""
TreasureCorp Marketing AI Agent
Powered by Anthropic Claude API
"""

import anthropic
import tweepy
import requests
import schedule
import time
import os
from datetime import datetime
import json

class TreasureCorpMarketingAgent:
    def __init__(self):
        # API Keys (set as environment variables)
        self.claude_client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        
        # Twitter API (optional)
        self.twitter_api = self.setup_twitter()
        
        # Content topics for rotation
        self.content_topics = [
            "DAO treasury management challenges",
            "Multi-chain analytics benefits", 
            "Treasury automation ROI",
            "Governance analytics insights",
            "DeFi treasury best practices",
            "Cross-chain treasury tracking",
            "DAO operational efficiency",
            "Treasury transparency tools"
        ]
        
        self.current_topic_index = 0

    def setup_twitter(self):
        """Setup Twitter API connection"""
        try:
            auth = tweepy.OAuthHandler(
                os.getenv("TWITTER_CONSUMER_KEY"),
                os.getenv("TWITTER_CONSUMER_SECRET")
            )
            auth.set_access_token(
                os.getenv("TWITTER_ACCESS_TOKEN"),
                os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
            )
            return tweepy.API(auth)
        except:
            print("Twitter API not configured")
            return None

    def generate_content(self, content_type, topic):
        """Generate content using Claude API"""
        
        prompts = {
            "linkedin_post": f"""
            Create a professional LinkedIn post for TreasureCorp about {topic}.
            
            Requirements:
            - 150-200 words
            - Professional, insightful tone
            - Highlight TreasureCorp's multi-chain treasury analytics
            - Include 3-5 relevant hashtags
            - End with an engagement question
            - Focus on value for DAO treasury managers
            
            TreasureCorp Context:
            - DAO treasury management and analytics platform
            - Multi-chain tracking (Ethereum, Arbitrum, etc.)
            - Automated reporting and governance insights
            - Proven ROI with customers like MoonDAO
            """,
            
            "twitter_thread": f"""
            Create a 3-tweet thread for TreasureCorp about {topic}.
            
            Tweet 1: Hook - identify a problem in DAO treasury management
            Tweet 2: Solution - how TreasureCorp addresses this
            Tweet 3: Call-to-action with value proposition
            
            Include hashtags: #DAO #Treasury #DeFi #Web3 #TreasureCorp
            Keep each tweet under 280 characters.
            """,
            
            "email_subject": f"""
            Generate 5 compelling email subject lines for TreasureCorp newsletter about {topic}.
            Focus on benefits like cost savings, automation, transparency.
            """,
            
            "blog_outline": f"""
            Create a detailed blog post outline about {topic} for TreasureCorp.
            
            Include:
            - Compelling headline
            - 5-7 section headers
            - Key points for each section
            - Call-to-action
            - Target audience: DAO treasury managers and operators
            """
        }
        
        try:
            response = self.claude_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=500,
                messages=[{
                    "role": "user",
                    "content": prompts[content_type]
                }]
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"Error generating content: {e}")
            return None

    def post_to_twitter(self, content):
        """Post content to Twitter"""
        if not self.twitter_api:
            print("Twitter not configured")
            return False
            
        try:
            # If it's a thread, split by tweets
            if "Tweet 1:" in content:
                tweets = []
                for i in range(1, 4):
                    start = content.find(f"Tweet {i}:")
                    end = content.find(f"Tweet {i+1}:") if i < 3 else len(content)
                    if start != -1:
                        tweet = content[start:end].replace(f"Tweet {i}:", "").strip()
                        tweets.append(tweet)
                
                # Post thread
                previous_tweet = None
                for tweet in tweets:
                    if previous_tweet:
                        response = self.twitter_api.update_status(
                            tweet, 
                            in_reply_to_status_id=previous_tweet.id
                        )
                    else:
                        response = self.twitter_api.update_status(tweet)
                    previous_tweet = response
                    time.sleep(1)  # Rate limiting
                    
                print("Twitter thread posted successfully")
                return True
            else:
                # Single tweet
                self.twitter_api.update_status(content)
                print("Tweet posted successfully")
                return True
                
        except Exception as e:
            print(f"Error posting to Twitter: {e}")
            return False

    def post_to_linkedin(self, content):
        """Post to LinkedIn (requires LinkedIn API setup)"""
        # This requires LinkedIn API setup - placeholder for now
        print("LinkedIn posting would go here")
        print(f"Content: {content[:100]}...")
        return True

    def save_content(self, content_type, topic, content):
        """Save generated content to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"content_{content_type}_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write(f"Topic: {topic}\n")
            f.write(f"Type: {content_type}\n")
            f.write(f"Generated: {datetime.now()}\n")
            f.write(f"{'='*50}\n\n")
            f.write(content)
        
        print(f"Content saved to {filename}")

    def daily_linkedin_post(self):
        """Generate and post daily LinkedIn content"""
        topic = self.content_topics[self.current_topic_index]
        content = self.generate_content("linkedin_post", topic)
        
        if content:
            print(f"Generated LinkedIn post about: {topic}")
            print(content)
            print("-" * 50)
            
            # Save content
            self.save_content("linkedin_post", topic, content)
            
            # Post to LinkedIn (implement API connection)
            self.post_to_linkedin(content)
            
            # Rotate topic
            self.current_topic_index = (self.current_topic_index + 1) % len(self.content_topics)

    def weekly_twitter_thread(self):
        """Generate and post weekly Twitter thread"""
        topic = self.content_topics[self.current_topic_index]
        content = self.generate_content("twitter_thread", topic)
        
        if content:
            print(f"Generated Twitter thread about: {topic}")
            print(content)
            print("-" * 50)
            
            # Save content
            self.save_content("twitter_thread", topic, content)
            
            # Post to Twitter
            self.post_to_twitter(content)

    def generate_newsletter_content(self):
        """Generate weekly newsletter content"""
        topic = "weekly DAO treasury insights"
        content = self.generate_content("blog_outline", topic)
        
        if content:
            print("Generated newsletter outline:")
            print(content)
            self.save_content("newsletter", topic, content)

    def run_scheduler(self):
        """Run the scheduled content generation"""
        print("TreasureCorp Marketing Agent Starting...")
        
        # Schedule tasks
        schedule.every().day.at("09:00").do(self.daily_linkedin_post)
        schedule.every().monday.at("10:00").do(self.weekly_twitter_thread)
        schedule.every().monday.at("11:00").do(self.generate_newsletter_content)
        
        # For testing - generate content now
        print("Generating test content...")
        self.daily_linkedin_post()
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

def main():
    """Main function"""
    agent = TreasureCorpMarketingAgent()
    
    # Test content generation
    topic = "DAO treasury management challenges"
    
    print("Testing LinkedIn post generation...")
    linkedin_content = agent.generate_content("linkedin_post", topic)
    if linkedin_content:
        print(linkedin_content)
        print("\n" + "="*50 + "\n")
    
    print("Testing Twitter thread generation...")
    twitter_content = agent.generate_content("twitter_thread", topic)
    if twitter_content:
        print(twitter_content)
    
    # Uncomment to run scheduler
    # agent.run_scheduler()

if __name__ == "__main__":
    main()