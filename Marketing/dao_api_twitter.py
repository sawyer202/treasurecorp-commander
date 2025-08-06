import requests
import json
import datetime
import random
import os
import hashlib

class TwitterPostGenerator:
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
        
        # DAO benchmarks for reference
        self.benchmarks = [
            "MakerDAO maintains a 45% stablecoin treasury allocation, setting industry standards for stability",
            "Uniswap governance achieved 87% voter participation by implementing delegation dashboards",
            "Aave's treasury grew 3.2x in 12 months with their multi-chain diversification strategy",
            "Gitcoin reduced proposal approval time by 72% using streamlined governance processes",
            "Lido DAO increased operational efficiency by 58% through transparent treasury reporting",
            "ENS governance maintains 40/30/30 allocation between stables/ETH/investments for sustainability",
            "Optimism achieved 92% governance participation through their delegate incentive program",
            "Compound's treasury management yielded 14.2% annualized returns through strategic diversification",
            "dYdX DAO reduced operational costs by 31% with automated treasury management tools",
            "Arbitrum foundation benchmarks at 60% voter participation across all significant proposals"
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
            
            # Also check for high similarity (optional - can be removed if too strict)
            if self.similarity_score(post, existing_post["content"]) > 0.85:
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
        """Generate a post using the Anthropic API"""
        
        # Construct the prompt
        emoji_instruction = "Include relevant emojis in the post." if include_emojis else "Do not use emojis in the post."
        
        # Reference a random benchmark
        benchmark = random.choice(self.benchmarks)
        
        prompt = f"""
        Create a Twitter post for {self.company_name}, a company that provides {self.product}.
        The company vision is: "{self.vision}"
        
        The post should focus on the theme: {theme}
        
        For context, here's a real-world benchmark you can reference if relevant:
        "{benchmark}"
        
        Requirements:
        - Be concise and impactful (max 280 characters)
        - Include relevant hashtags (#DAO, #DeFi, #Web3, #TreasureCorp, etc.)
        - {emoji_instruction}
        - Focus on treasury management for DAOs
        - Include a clear value proposition or call to action
        - Do not use generic language - be specific and informative
        
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
    
    def generate_daily_posts(self, count=7):
        """Generate a week's worth of posts, one for each day"""
        themes = [
            "Product Overview & Benefits",
            "Treasury Management Education",
            "DAO Governance Best Practices",
            "Community Questions & Engagement",
            "Industry Trends & Insights", 
            "Benchmark Comparisons",
            "Treasury Management Tools & Tips"
        ]
        
        posts = []
        
        for i in range(min(count, len(themes))):
            theme = themes[i]
            day = (datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%A")
            
            print(f"Generating post for {day} with theme: {theme}")
            post = self.generate_unique_post(theme)
            posts.append({"day": day, "theme": theme, "content": post})
        
        return posts
    
    def save_posts_to_file(self, posts, filename=None):
        """Save posts to a markdown file"""
        if filename is None:
            filename = f"treasure_corp_twitter_posts_{datetime.datetime.now().strftime('%Y%m%d')}.md"
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("# Generated Twitter Posts for Treasure.Corp\n\n")
                f.write(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n")
                
                f.write("## Text-to-Image Tools Recommendation\n\n")
                f.write("To convert these posts to eye-catching images for higher engagement, try these tools:\n\n")
                f.write("1. **Canva** - Free templates specifically designed for social media\n")
                f.write("2. **Pablo by Buffer** - Since you're using Buffer, their built-in image creator is convenient\n")
                f.write("3. **Adobe Express** - Professional-quality templates with free tier\n")
                f.write("4. **Visme** - Great for data visualization if sharing treasury metrics\n")
                f.write("5. **Piktochart** - Good for creating infographics about DAO benchmarks\n\n")
                
                f.write("## Weekly Posts\n\n")
                for post in posts:
                    f.write(f"### {post['day']} - {post['theme']}\n\n")
                    f.write(f"{post['content']}\n\n")
                    f.write("-" * 80 + "\n\n")
            
            print(f"Successfully wrote {len(posts)} posts to {filename}")
            return filename
        except Exception as e:
            print(f"Error saving file: {e}")
            return None
    
    def get_post_count(self):
        """Get the count of posts in history"""
        return len(self.post_history["posts"])


def main():
    print("Treasure.Corp Twitter Post Generator - API Version")
    print("===============================================")
    
    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        api_key = input("Enter your Anthropic API key: ").strip()
        if not api_key:
            print("No API key provided. Exiting.")
            return
    
    generator = TwitterPostGenerator(api_key)
    
    # Show existing post count
    existing_posts = generator.get_post_count()
    print(f"Current post history contains {existing_posts} posts")
    
    # Generate posts
    print("\nGenerating weekly posts...")
    posts = generator.generate_daily_posts(7)
    
    # Save to file
    filename = generator.save_posts_to_file(posts)
    
    if filename:
        print("\nPost generation complete!")
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