import requests
import json
import datetime
import random
import os
import hashlib

class RefinedTweetGenerator:
    def __init__(self, api_key):
        # API configuration
        self.api_key = api_key
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.model = "claude-3-opus-20240229"
        
        # Company information
        self.company_name = "Treasure.Corp"
        self.product = "Data-driven treasury solutions for DAOs"
        self.vision = "Treasury Clarity for the Decentralized World"
        
        # Database for tracking generated posts
        self.post_history_file = "post_history.json"
        self.post_history = self.load_post_history()
        
        # High-engagement post for reference
        self.high_engagement_post = (
            "Exploring DAO treasury analytics is fascinating, as on-chain data reveals governance health. "
            "Tracking asset diversification, spending patterns, and voter participation signals sustainability. "
            "The future of DAOs may hinge more on data literacy than we realize. #DAOanalytics #Web3"
        )
        
        # Professional DAO benchmarks and metrics
        self.benchmarks = [
            "MakerDAO's treasury data reveals a 45% stablecoin allocation, resulting in 38% lower volatility during market fluctuations",
            "On-chain analytics show Uniswap governance participation increased 64% after implementing data visualization dashboards",
            "Tracking Aave's treasury diversification reveals fascinating patterns: 18.2% returns while maintaining governance health",
            "ENS governance data shows a carefully balanced 40/30/30 allocation between stables/ETH/investments signaling sustainability",
            "Compound's treasury analytics reveal 14.2% annualized returns through data-driven diversification decisions",
            "Our on-chain analysis of top DAOs shows an average of 24 months runway in stablecoins, a key sustainability metric",
            "Data reveals DAOs with transparent treasury dashboards show 2.7x higher governance participation, a critical health signal",
            "Tracking multi-chain treasury allocations shows 31% lower impermanent loss during volatility—data literacy matters",
            "Analytics reveal properly structured multi-sig treasuries achieve 58% faster capital deployment while maintaining governance",
            "Fascinating on-chain data: DAOs with structured treasury frameworks outperform ad-hoc management by 41% on sustainability metrics"
        ]
        
        # Key topics from high-engagement post
        self.key_topics = [
            "DAO treasury analytics",
            "on-chain data",
            "governance health",
            "asset diversification",
            "spending patterns",
            "voter participation",
            "sustainability signals",
            "data literacy",
            "treasury transparency",
            "governance efficiency"
        ]
    
    def load_post_history(self):
        """Load previously generated posts from JSON file"""
        if os.path.exists(self.post_history_file):
            try:
                with open(self.post_history_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading post history: {e}")
                return {"posts": []}
        else:
            return {"posts": []}
    
    def save_post_history(self):
        """Save post history to JSON file"""
        with open(self.post_history_file, 'w') as f:
            json.dump(self.post_history, f, indent=2)
    
    def is_duplicate(self, post):
        """Check if a post is a duplicate based on content hash"""
        post_hash = hashlib.md5(post.encode()).hexdigest()
        
        # Check if this hash already exists in our history
        for existing_post in self.post_history["posts"]:
            if existing_post["hash"] == post_hash:
                return True
            
            # Also check for high similarity
            if self.similarity_score(post, existing_post["content"]) > 0.80:
                return True
                
        return False
    
    def similarity_score(self, text1, text2):
        """Calculate a simple similarity score between two texts"""
        # Convert both texts to sets of words
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        # Calculate Jaccard similarity
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        if len(union) == 0:
            return 0
        return len(intersection) / len(union)
    
    def add_to_history(self, post):
        """Add a post to history to prevent future duplication"""
        post_hash = hashlib.md5(post.encode()).hexdigest()
        
        self.post_history["posts"].append({
            "content": post,
            "hash": post_hash,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Limit history size to prevent unlimited growth
        if len(self.post_history["posts"]) > 1000:
            self.post_history["posts"] = self.post_history["posts"][-1000:]
            
        self.save_post_history()
    
    def generate_post_with_api(self, theme, include_emojis=True):
        """Generate a post using the Anthropic API based on high-engagement patterns"""
        
        # Construct the prompt
        emoji_instruction = "Include 1-2 relevant emojis in the post." if include_emojis else "Do not use emojis in the post."
        
        # Reference a random benchmark and key topic
        benchmark = random.choice(self.benchmarks)
        key_topic = random.choice(self.key_topics)
        
        prompt = f"""
        Create a Twitter post for {self.company_name} about {self.product}.
        
        The post should focus on the theme: {theme}
        
        For context, this previous post received high engagement from our audience:
        "{self.high_engagement_post}"
        
        Also, here's a relevant benchmark that could be referenced:
        "{benchmark}"
        
        Requirements:
        - Use a similar thoughtful, insight-driven tone as the high-engagement post
        - Focus on {key_topic} and how it relates to treasury management
        - Include terms like "fascinating," "reveals," "tracking," "signals," or similar analytical language
        - Structure as an observation followed by implications, similar to the high-engagement post
        - Be concise yet substantive (max 280 characters)
        - Include 1-2 relevant hashtags (like #DAOanalytics #Web3)
        - {emoji_instruction}
        - Focus on analysis rather than promotion
        - End with a thoughtful insight about data or governance
        
        Format: Just provide the post text, nothing else.
        """
        
        # Prepare the API request
        headers = {
            "x-api-key": self.api_key,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": self.model,
            "max_tokens": 300,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        # Make the API request
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data
            )
            
            response.raise_for_status()  # Raise exception for HTTP errors
            result = response.json()
            
            if "content" in result and len(result["content"]) > 0:
                post = result["content"][0]["text"].strip()
                return post
            else:
                raise Exception("Empty response from API")
                
        except Exception as e:
            print(f"API Error: {e}")
            return None
    
    def generate_unique_post(self, theme, max_attempts=5):
        """Generate a unique post that isn't a duplicate of previous posts"""
        attempts = 0
        
        while attempts < max_attempts:
            post = self.generate_post_with_api(theme)
            
            if post and not self.is_duplicate(post):
                # Add to history and return
                self.add_to_history(post)
                return post
            
            attempts += 1
            if post:
                print(f"Generated duplicate post, retrying... (Attempt {attempts}/{max_attempts})")
            else:
                print(f"Failed to generate post, retrying... (Attempt {attempts}/{max_attempts})")
        
        # If we couldn't generate a unique post after max attempts
        return "Failed to generate a unique post after multiple attempts. Please try again later."
    
    def generate_engagement_focused_posts(self, count=7):
        """Generate posts based on patterns from high-engagement content"""
        themes = [
            "DAO Treasury Analytics",
            "On-Chain Governance Data",
            "Treasury Diversification Insights",
            "Voter Participation Metrics",
            "Sustainability Signals", 
            "Data Literacy in DAOs",
            "Treasury Transparency"
        ]
        
        posts = []
        
        for i in range(min(count, len(themes))):
            theme = themes[i]
            day = (datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%A")
            
            print(f"Generating engagement-optimized post for {day} with theme: {theme}")
            post = self.generate_unique_post(theme)
            posts.append({"day": day, "theme": theme, "content": post})
        
        return posts
    
    def save_posts_to_file(self, posts, filename=None):
        """Save posts to a markdown file with engagement insights"""
        if filename is None:
            filename = f"treasure_corp_high_engagement_posts_{datetime.datetime.now().strftime('%Y%m%d')}.md"
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("# High-Engagement Twitter Content: Treasure.Corp\n\n")
                f.write(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n")
                
                f.write("## Content Strategy Overview\n\n")
                f.write("This content is modeled after our highest-performing post:\n\n")
                f.write(f"```\n{self.high_engagement_post}\n```\n\n")
                f.write("Key engagement factors include:\n")
                f.write("- Thoughtful, insight-driven tone\n")
                f.write("- Focus on data analytics and governance\n")
                f.write("- Observation → Implication structure\n")
                f.write("- Ending with forward-looking insights\n")
                f.write("- Specific, relevant hashtags\n\n")
                
                f.write("## Weekly Content Calendar\n\n")
                
                # Create a clean table for the content calendar
                f.write("| Day | Theme | Post |\n")
                f.write("|-----|-------|------|\n")
                
                for post in posts:
                    # Clean up post content for table display (remove line breaks)
                    clean_content = post['content'].replace('\n', ' ')
                    f.write(f"| {post['day']} | {post['theme']} | {clean_content} |\n")
                
                f.write("\n## Individual Posts\n\n")
                for post in posts:
                    f.write(f"### {post['day']}: {post['theme']}\n\n")
                    f.write(f"{post['content']}\n\n")
                    f.write("-" * 80 + "\n\n")
                
                f.write("## Visual Content Enhancement\n\n")
                f.write("For maximum engagement, consider enhancing these posts with:\n\n")
                f.write("1. **Data Visualizations**: Simple charts showing governance participation or treasury allocation\n")
                f.write("2. **Comparative Graphics**: Before/after implementing data-driven treasury management\n")
                f.write("3. **Quote Cards**: Pull out the insightful conclusions as standalone graphics\n")
                f.write("4. **Analytics Dashboards**: Screenshots of anonymized dashboard examples\n")
                
                f.write("\n## Recommended Tools\n\n")
                f.write("* **Canva**: For quick, professional graphics with data visualization templates\n")
                f.write("* **Buffer's Pablo**: For simpler quote cards and text overlays\n")
                f.write("* **Adobe Express**: For more polished, brand-consistent visuals\n")
                f.write("* **Visme**: Specifically for data-heavy visualizations and charts\n")
            
            print(f"Successfully wrote {len(posts)} engagement-optimized posts to {filename}")
            return filename
        except Exception as e:
            print(f"Error saving file: {e}")
            return None
    
    def get_post_count(self):
        """Get the count of posts in history"""
        return len(self.post_history["posts"])


def main():
    print("Treasure.Corp High-Engagement Twitter Generator")
    print("==============================================")
    
    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        api_key = input("Enter your Anthropic API key: ").strip()
        if not api_key:
            print("No API key provided. Exiting.")
            return
    
    generator = RefinedTweetGenerator(api_key)
    
    # Show existing post count
    existing_posts = generator.get_post_count()
    print(f"Current post history contains {existing_posts} posts")
    
    # Generate posts
    print("\nGenerating high-engagement content based on successful patterns...")
    posts = generator.generate_engagement_focused_posts(7)
    
    # Save to file
    filename = generator.save_posts_to_file(posts)
    
    if filename:
        print("\nHigh-engagement content generation complete!")
        print(f"\nNew posts have been saved to: {filename}")
        print(f"Total posts in history: {generator.get_post_count()}")
        
        # Display sample
        print("\nSample post:")
        print("-" * 50)
        if posts:
            print(f"Theme: {posts[0]['theme']}")
            print(posts[0]['content'])
        print("-" * 50)
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()