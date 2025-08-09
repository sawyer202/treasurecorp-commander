#!/usr/bin/env python3
"""
DAO Monitoring LLM System
Custom AI agent for monitoring DAO ecosystem and generating social media content
"""

import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
import feedparser
import anthropic
from PIL import Image, ImageDraw, ImageFont
import tweepy
import telegram
# LinkedIn API removed for deployment simplicity
import schedule
import time
import os
import json
import sqlite3
from datetime import datetime, timedelta
import hashlib
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DAOMonitoringLLM:
    def __init__(self):
        # API clients
        self.claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        # Social media clients
        self.twitter_api = self._setup_twitter()
        self.telegram_bot = self._setup_telegram()
        # LinkedIn API removed for deployment simplicity
        
        # Database setup
        self._setup_database()
        
        # DAO sources configuration
        self.dao_sources = {
            'snapshot': 'https://hub.snapshot.org/graphql',
            'commonwealth': 'https://commonwealth.im/api',
            'governance_forums': [
                'https://gov.uniswap.org',
                'https://governance.aave.com', 
                'https://forum.makerdao.com',
                'https://research.lido.fi',
                'https://forum.compound.finance'
            ],
            'dao_websites': [
                'https://www.moondao.com',
                'https://www.banklessdao.com',
                'https://www.developerdao.com'
            ]
        }
        
        # News sources for DAO monitoring
        self.news_sources = [
            'https://feeds.feedburner.com/oreilly/radar/atom10',
            'https://rss.cnn.com/rss/money_news_international.rss',
            'https://www.coindesk.com/arc/outboundfeeds/rss/',
            'https://cointelegraph.com/rss',
            'https://decrypt.co/feed'
        ]

    def _setup_database(self):
        """Initialize SQLite database for tracking content and avoiding duplicates"""
        self.db_connection = sqlite3.connect('dao_monitoring.db', check_same_thread=False)
        cursor = self.db_connection.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monitored_content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                title TEXT,
                url TEXT UNIQUE,
                content_hash TEXT,
                discovered_at TIMESTAMP,
                processed_at TIMESTAMP,
                summary TEXT,
                posted_twitter BOOLEAN DEFAULT 0,
                posted_linkedin BOOLEAN DEFAULT 0,
                posted_telegram BOOLEAN DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dao_proposals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dao_name TEXT,
                proposal_id TEXT,
                title TEXT,
                description TEXT,
                status TEXT,
                votes_for INTEGER,
                votes_against INTEGER,
                end_date TIMESTAMP,
                url TEXT UNIQUE,
                discovered_at TIMESTAMP
            )
        ''')
        
        self.db_connection.commit()

    def _setup_twitter(self):
        """Setup Twitter API v2"""
        try:
            client = tweepy.Client(
                bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
                consumer_key=os.getenv("TWITTER_CONSUMER_KEY"),
                consumer_secret=os.getenv("TWITTER_CONSUMER_SECRET"),
                access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
                access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
                wait_on_rate_limit=True
            )
            return client
        except Exception as e:
            logger.error(f"Twitter setup failed: {e}")
            return None

    def _setup_telegram(self):
        """Setup Telegram bot"""
        try:
            bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
            return telegram.Bot(token=bot_token) if bot_token else None
        except Exception as e:
            logger.error(f"Telegram setup failed: {e}")
            return None

    def _setup_linkedin(self):
        """Setup LinkedIn API"""
        try:
            username = os.getenv("LINKEDIN_USERNAME")
            password = os.getenv("LINKEDIN_PASSWORD")
            return Linkedin(username, password) if username and password else None
        except Exception as e:
            logger.error(f"LinkedIn setup failed: {e}")
            return None

    async def monitor_dao_proposals(self) -> List[Dict]:
        """Monitor DAO governance proposals from various platforms"""
        proposals = []
        
        async with aiohttp.ClientSession() as session:
            # Snapshot proposals - query popular spaces directly
            try:
                proposals.extend(await self._fetch_snapshot_proposals(session))
            except Exception as e:
                logger.error(f"Error fetching Snapshot data: {e}")

            # Commonwealth proposals
            try:
                proposals.extend(await self._fetch_commonwealth_proposals(session))
            except Exception as e:
                logger.error(f"Error fetching Commonwealth data: {e}")

        return proposals

    async def _fetch_snapshot_proposals(self, session: aiohttp.ClientSession) -> List[Dict]:
        """Fetch active proposals from popular Snapshot spaces"""
        proposals = []
        
        # Popular DAO spaces to monitor
        popular_spaces = [
            "uniswap.eth",
            "aave.eth", 
            "compound-governance.eth",
            "banklessvault.eth",
            "gitcoindao.eth"
        ]
        
        query = '''
        {
          proposals(
            where: { space_in: %s, state: "active" }
            orderBy: "created"
            orderDirection: desc
            first: 10
          ) {
            id
            title
            body
            choices
            start
            end
            state
            scores
            scores_total
            votes
            author
            space {
              id
              name
            }
          }
        }
        ''' % str(popular_spaces).replace("'", '"')

        try:
            async with session.post(
                'https://hub.snapshot.org/graphql',
                json={'query': query},
                headers={'Content-Type': 'application/json'}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    for proposal in data.get('data', {}).get('proposals', []):
                        proposals.append({
                            'source': 'snapshot',
                            'dao_name': proposal['space']['name'],
                            'proposal_id': proposal['id'],
                            'title': proposal['title'],
                            'description': proposal['body'][:500] if proposal['body'] else '',
                            'status': proposal['state'],
                            'votes_total': proposal['votes'],
                            'end_date': datetime.fromtimestamp(proposal['end']) if proposal['end'] else None,
                            'url': f"https://snapshot.org/#/{proposal['space']['id']}/proposal/{proposal['id']}"
                        })
                else:
                    logger.error(f"Snapshot API returned status {response.status}")
        except Exception as e:
            logger.error(f"Error fetching Snapshot proposals: {e}")

        return proposals

    async def _fetch_commonwealth_proposals(self, session: aiohttp.ClientSession) -> List[Dict]:
        """Fetch proposals from Commonwealth"""
        proposals = []
        # Implementation would depend on Commonwealth API structure
        # This is a placeholder for the actual implementation
        return proposals

    async def monitor_dao_websites(self) -> List[Dict]:
        """Scrape DAO websites for news, updates, and reports"""
        content = []
        
        async with aiohttp.ClientSession() as session:
            for website_url in self.dao_sources['dao_websites']:
                try:
                    async with session.get(website_url) as response:
                        if response.status == 200:
                            html = await response.text()
                            soup = BeautifulSoup(html, 'html.parser')
                            
                            # Extract recent news/blog posts
                            articles = await self._extract_articles(soup, website_url)
                            content.extend(articles)
                            
                            # Look for downloadable reports
                            reports = await self._find_reports(soup, website_url)
                            content.extend(reports)
                            
                except Exception as e:
                    logger.error(f"Error scraping {website_url}: {e}")

        return content

    async def _extract_articles(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Extract article information from website"""
        articles = []
        
        # Common selectors for blog posts/news
        selectors = [
            'article',
            '.post', '.blog-post', '.news-item',
            '[class*="article"]', '[class*="post"]'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)[:5]  # Limit to 5 most recent
            
            for element in elements:
                title_elem = element.find(['h1', 'h2', 'h3', 'h4'])
                link_elem = element.find('a')
                
                if title_elem and link_elem:
                    articles.append({
                        'source': base_url,
                        'title': title_elem.get_text().strip(),
                        'url': self._resolve_url(base_url, link_elem.get('href')),
                        'snippet': element.get_text()[:200].strip(),
                        'type': 'article'
                    })
        
        return articles

    async def _find_reports(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Find downloadable reports on the website"""
        reports = []
        
        # Look for PDF links and report downloads
        pdf_links = soup.find_all('a', href=lambda x: x and x.endswith('.pdf'))
        
        for link in pdf_links[:3]:  # Limit to 3 reports
            reports.append({
                'source': base_url,
                'title': link.get_text().strip() or 'Report',
                'url': self._resolve_url(base_url, link.get('href')),
                'type': 'report'
            })
        
        return reports

    def _resolve_url(self, base_url: str, relative_url: str) -> str:
        """Resolve relative URLs to absolute URLs"""
        from urllib.parse import urljoin
        return urljoin(base_url, relative_url)

    async def monitor_news_feeds(self) -> List[Dict]:
        """Monitor RSS feeds for DAO-related news"""
        news_items = []
        
        for feed_url in self.news_sources:
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:5]:  # Last 5 entries per feed
                    # Filter for DAO-related content
                    if self._is_dao_relevant(entry.title + " " + entry.get('summary', '')):
                        news_items.append({
                            'source': feed_url,
                            'title': entry.title,
                            'url': entry.link,
                            'summary': entry.get('summary', '')[:300],
                            'published': entry.get('published_parsed'),
                            'type': 'news'
                        })
                        
            except Exception as e:
                logger.error(f"Error parsing feed {feed_url}: {e}")
        
        return news_items

    def _is_dao_relevant(self, text: str) -> bool:
        """Check if content is relevant to DAOs using keyword matching"""
        dao_keywords = [
            'dao', 'decentralized autonomous organization', 'governance token',
            'voting', 'proposal', 'treasury', 'defi', 'decentralized finance',
            'blockchain governance', 'token holder', 'snapshot', 'multisig'
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in dao_keywords)

    async def process_and_summarize(self, content_items: List[Dict]) -> List[Dict]:
        """Process content items and generate summaries using LLM"""
        processed_items = []
        
        for item in content_items:
            try:
                # Check if already processed
                content_hash = hashlib.md5(item['title'].encode()).hexdigest()
                cursor = self.db_connection.cursor()
                cursor.execute("SELECT id FROM monitored_content WHERE content_hash = ?", (content_hash,))
                
                if cursor.fetchone():
                    continue  # Skip already processed content
                
                # Generate summary
                summary = await self._generate_summary(item)
                
                if summary:
                    processed_item = {
                        **item,
                        'summary': summary,
                        'content_hash': content_hash
                    }
                    processed_items.append(processed_item)
                    
                    # Store in database
                    cursor.execute('''
                        INSERT INTO monitored_content 
                        (source, title, url, content_hash, discovered_at, summary)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        item['source'], item['title'], item['url'],
                        content_hash, datetime.now(), summary
                    ))
                    self.db_connection.commit()
                    
            except Exception as e:
                logger.error(f"Error processing item {item.get('title', 'Unknown')}: {e}")
        
        return processed_items

    async def _generate_summary(self, item: Dict) -> str:
        """Generate a concise summary using Claude"""
        try:
            # Fetch full content if it's a URL
            content_text = item.get('summary', item.get('snippet', ''))
            
            if item.get('url') and item.get('type') != 'report':
                try:
                    response = requests.get(item['url'], timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        content_text = soup.get_text()[:2000]  # Limit content length
                except:
                    pass  # Use existing content if fetch fails

            prompt = f"""
            You are creating social media content for Treasure.Corp, a platform that provides seamless governance solutions for DAOs and solves treasury management challenges.

            Treasure.Corp Brand Voice:
            - Professional but accessible
            - Focus on governance and treasury solutions
            - Emphasize problem-solving for DAOs
            - Use relevant emojis (📊, 💰, 🏛️, ⚡, 🔍)
            - Always position Treasure.Corp as the solution provider
            
            Content to analyze:
            Title: {item['title']}
            Content: {content_text}
            Source: {item['source']}
            
            Create 2 versions:
            
            1. Twitter (280 chars max):
            - Start with relevant emoji (📊, 💰, 🏛️, ⚡, 🔍)
            - Connect the news/update to treasury management or governance challenges
            - Show how this relates to DAO operations
            - End with "Treasure.Corp solves [specific challenge]" or similar
            - Use hashtags: #DecentralizedTreasury #DAO #DAOFinance plus 1-2 relevant ones
            
            2. Telegram (400 chars max):
            - More detailed analysis
            - Explain implications for DAO treasuries and governance
            - Include actionable insights
            - Mention how Treasure.Corp addresses these challenges
            - Community-focused tone with discussion prompts
            """

            response = self.claude_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=400,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return None

    def generate_social_images(self, content: Dict) -> Dict[str, str]:
        """Generate platform-specific images for social media posts"""
        image_paths = {}
        
        try:
            # Image specifications for each platform
            specs = {
                'twitter': (1200, 675),
                'linkedin': (1200, 627),
                'telegram': (800, 600)
            }
            
            for platform, (width, height) in specs.items():
                # Create image
                img = Image.new('RGB', (width, height), color='#1a1a1a')
                draw = ImageDraw.Draw(img)
                
                # Try to load custom font
                try:
                    title_font = ImageFont.truetype("arial.ttf", 48)
                    subtitle_font = ImageFont.truetype("arial.ttf", 32)
                except:
                    title_font = ImageFont.load_default()
                    subtitle_font = ImageFont.load_default()
                
                # Add TreasureCorp branding
                draw.text((50, 50), "TreasureCorp", fill='#00ff88', font=title_font)
                draw.text((50, 120), "DAO Intelligence", fill='#ffffff', font=subtitle_font)
                
                # Add content title (wrapped)
                title = content['title'][:80] + "..." if len(content['title']) > 80 else content['title']
                draw.text((50, 200), title, fill='#ffffff', font=subtitle_font)
                
                # Add platform-specific elements
                if platform == 'twitter':
                    draw.text((50, height - 100), "#DAO #Web3 #Governance", fill='#1da1f2', font=subtitle_font)
                elif platform == 'linkedin':
                    draw.text((50, height - 100), "Professional DAO Insights", fill='#0077b5', font=subtitle_font)
                elif platform == 'telegram':
                    draw.text((50, height - 100), "💡 DAO Update Alert", fill='#0088cc', font=subtitle_font)
                
                # Save image
                filename = f"dao_content_{platform}_{int(time.time())}.png"
                filepath = f"/tmp/{filename}"
                img.save(filepath)
                image_paths[platform] = filepath
                
        except Exception as e:
            logger.error(f"Error generating images: {e}")
            
        return image_paths

    async def post_to_social_media(self, content: Dict, summaries: Dict, images: Dict):
        """Post content to all configured social media platforms"""
        
        # Post to Twitter
        if self.twitter_api and 'twitter' in summaries:
            try:
                # Twitter API v2 doesn't support media uploads directly
                # For now, just post text content
                self.twitter_api.create_tweet(text=summaries['twitter'])
                logger.info(f"Posted to Twitter: {content['title']}")
            except Exception as e:
                logger.error(f"Twitter posting failed: {e}")
        
        # LinkedIn posting removed for deployment simplification
        
        # Post to Telegram
        if self.telegram_bot and 'telegram' in summaries:
            try:
                chat_id = os.getenv("TELEGRAM_CHAT_ID")
                if chat_id:
                    if 'telegram' in images:
                        self.telegram_bot.send_photo(
                            chat_id=chat_id,
                            photo=open(images['telegram'], 'rb'),
                            caption=summaries['telegram']
                        )
                    else:
                        self.telegram_bot.send_message(
                            chat_id=chat_id,
                            text=summaries['telegram']
                        )
                logger.info(f"Posted to Telegram: {content['title']}")
            except Exception as e:
                logger.error(f"Telegram posting failed: {e}")

    async def daily_monitoring_cycle(self):
        """Run the complete daily monitoring and posting cycle"""
        logger.info("Starting daily DAO monitoring cycle...")
        
        try:
            # Collect content from all sources
            all_content = []
            
            # Monitor proposals
            proposals = await self.monitor_dao_proposals()
            all_content.extend(proposals)
            
            # Monitor websites
            website_content = await self.monitor_dao_websites()
            all_content.extend(website_content)
            
            # Monitor news feeds
            news_content = await self.monitor_news_feeds()
            all_content.extend(news_content)
            
            logger.info(f"Collected {len(all_content)} content items")
            
            # Process and summarize
            processed_content = await self.process_and_summarize(all_content)
            logger.info(f"Processed {len(processed_content)} new items")
            
            # Post to social media
            for item in processed_content[:5]:  # Limit to 5 posts per day
                try:
                    # Parse summaries (assuming they're formatted properly)
                    summaries = self._parse_summaries(item['summary'])
                    
                    # Generate images
                    images = self.generate_social_images(item)
                    
                    # Post to social media
                    await self.post_to_social_media(item, summaries, images)
                    
                    # Clean up temporary images
                    for img_path in images.values():
                        try:
                            os.remove(img_path)
                        except:
                            pass
                    
                    # Delay between posts to avoid rate limiting
                    await asyncio.sleep(300)  # 5 minutes between posts
                    
                except Exception as e:
                    logger.error(f"Error posting content: {e}")
            
            logger.info("Daily monitoring cycle completed")
            
        except Exception as e:
            logger.error(f"Error in daily monitoring cycle: {e}")

    def _parse_summaries(self, summary_text: str) -> Dict[str, str]:
        """Parse the formatted summary text into platform-specific versions"""
        summaries = {}
        
        # Simple parsing - in production, use more robust parsing
        lines = summary_text.split('\n')
        current_platform = None
        current_text = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('1. Twitter'):
                current_platform = 'twitter'
                current_text = []
            elif line.startswith('2. Telegram'):
                if current_platform:
                    summaries[current_platform] = '\n'.join(current_text).strip()
                current_platform = 'telegram'
                current_text = []
            elif current_platform and line:
                current_text.append(line)
        
        # Add the last platform
        if current_platform:
            summaries[current_platform] = '\n'.join(current_text).strip()
        
        return summaries

    def start_scheduler(self):
        """Start the scheduling system"""
        logger.info("Starting DAO Monitoring LLM scheduler...")
        
        # Schedule daily monitoring at 9 AM
        schedule.every().day.at("09:00").do(
            lambda: asyncio.run(self.daily_monitoring_cycle())
        )
        
        # Schedule additional checks every 6 hours for urgent updates
        schedule.every(6).hours.do(
            lambda: asyncio.run(self.daily_monitoring_cycle())
        )
        
        # Run once immediately for testing
        asyncio.run(self.daily_monitoring_cycle())
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

def main():
    """Main function to start the DAO monitoring system"""
    monitor = DAOMonitoringLLM()
    monitor.start_scheduler()

if __name__ == "__main__":
    main()