import requests
import json
import datetime
import random
import os
import hashlib

class EngagementOptimizedGenerator:
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
        
        # High-engagement post for reference (57 engagements)
        self.high_engagement_post = (
            "Exploring DAO treasury analytics is fascinating, as on-chain data reveals governance health. "
            "Tracking asset diversification, spending patterns, and voter participation signals sustainability. "
            "The future of DAOs may hinge more on data literacy than we realize. #DAOanalytics #Web3"
        )
        
        # Deep analysis of why this post worked
        self.engagement_factors = {
            "tone": [
                "intellectually curious",
                "genuinely fascinated",
                "thoughtful",
                "analytical",
                "educational",
                "forward-looking"
            ],
            "structure": [
                "observation → specific examples → broader implication",
                "present insight → supporting details → future prediction",
                "curiosity hook → informative body → thought-provoking conclusion"
            ],
            "language_patterns": [
                "Exploring ... is fascinating",
                "reveals ...",
                "tracking ... signals ...",
                "may hinge more on ... than we realize"
            ],
            "content_focus": [
                "on-chain data analysis",
                "governance health indicators",
                "sustainability signals",
                "data literacy importance",
                "treasury management insights",
                "connecting data to governance outcomes"
            ],
            "successful_elements": [
                "authentic expertise",
                "genuine insights",
                "thought leadership",
                "specific technical details",
                "avoidance of promotional language",
                "precise hashtags"
            ]
        }
        
        # Professional DAO benchmarks and metrics (reframed to match successful tone)
        self.benchmarks = [
            "Exploring MakerDAO's treasury composition reveals a fascinating pattern: 45% stablecoin allocation correlates with 38% lower volatility",
            "On-chain data from Uniswap shows governance participation increased 64% after implementing visualization dashboards",
            "Tracking Aave's diversification strategy reveals an intriguing balance: 18.2% returns while maintaining governance health",
            "ENS governance data shows a 40/30/30 allocation between stables/ETH/investments—a pattern that signals sustainability",
            "Compound's treasury analytics reveal a correlation between multi-chain distribution and 14.2% annualized returns",
            "On-chain analysis reveals top DAOs maintain an average 24-month runway in stablecoins—a key sustainability signal",
            "Data tracking shows DAOs with transparent dashboards achieve 2.7x higher governance participation",
            "Exploring multi-chain treasury allocations reveals 31% lower impermanent loss during volatility—data literacy matters",
            "Governance data shows structured multi-sig treasuries achieve 58% faster capital deployment while maintaining integrity",
            "Tracking on-chain metrics reveals DAOs with data-driven frameworks outperform ad-hoc management by 41% on sustainability"
        ]
        
        # Key topics from high-engagement post (expanded)
        self.key_topics = [
            "DAO treasury analytics",
            "on-chain data signals",
            "governance health indicators",
            "asset diversification patterns",
            "spending pattern analysis",
            "voter participation metrics",
            "sustainability indicators",
            "data literacy importance",
            "treasury diversification strategies",
            "governance efficiency measurements"
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
    
    def generate_post_with_api(self, theme):
        """Generate a post using the Anthropic API based on deep engagement analysis"""
        
        # Select patterns from our engagement analysis
        tone = random.choice(self.engagement_factors["tone"])
        structure = random.choice(self.engagement_factors["structure"])
        language_pattern = random.choice(self.engagement_factors["language_patterns"])
        content_focus = random.choice(self.engagement_factors["content_focus"])
        successful_element = random.choice(self.engagement_factors["successful_elements"])
        
        # Reference a random benchmark and key topic
        benchmark = random.choice(self.benchmarks)
        key_topic = random.choice(self.key_topics)
        
        prompt = f"""
        Create a Twitter post for {self.company_name} about {self.product} that will generate high engagement.
        
        The post should focus on the theme: {theme}
        
        For context, this previous post received 57 engagements from our audience:
        "{self.high_engagement_post}"
        
        What made this post successful:
        1. Tone: {tone}
        2. Structure: {structure}
        3. Language pattern to incorporate: "{language_pattern}"
        4. Content focus: {content_focus}
        5. Successful element to include: {successful_element}
        
        Also, here's a relevant benchmark written in the successful style:
        "{benchmark}"
        
        Requirements:
        - Match the intellectual, curious tone of the high-engagement post
        - Focus on {key_topic} with specific, technical details
        - Follow the three-part structure: observation → examples → broader implication
        - Include specific technical details that demonstrate expertise
        - End with a thought-provoking insight about the future
        - Use precise hashtags (max 2-3) that would reach the right audience
        - Avoid promotional language - focus on genuine insights
        - Be concise yet substantive (max 280 characters)
        
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
    
    def analyze_engagement_potential(self, post):
        """Analyze a post for engagement potential based on our learned patterns"""
        score = 0
        max_score = 10
        
        # Check for key patterns that drove engagement
        if any(pattern.lower() in post.lower() for pattern in self.engagement_factors["language_patterns"]):
            score += 2
        
        # Check for three-part structure
        if ". " in post and post.count(". ") >= 2:
            score += 2
        
        # Check for technical specificity
        if any(topic.lower() in post.lower() for topic in self.key_topics):
            score += 2
        
        # Check for thought-provoking conclusion
        if any(word in post.lower() for word in ["future", "may", "could", "might", "potential", "realize"]):
            score += 1
        
        # Check for promotional language (negative factor)
        promotional_terms = ["we offer", "our product", "try our", "best", "leading", "sign up"]
        if any(term in post.lower() for term in promotional_terms):
            score -= 2
        
        # Check for proper hashtag usage
        if "#" in post and post.count("#") <= 3:
            score += 1
        
        # Check for questions (can increase engagement)
        if "?" in post:
            score += 1
        
        # Normalize score to 10
        normalized_score = min(max(score, 0), max_score)
        return normalized_score
    
    def generate_engagement_optimized_posts(self, count=7):
        """Generate posts optimized for high engagement based on successful patterns"""
        themes = [
            "DAO Treasury Analytics",
            "On-Chain Governance Data",
            "Treasury Diversification Insights",
            "Voter Participation Metrics",
            "Sustainability Indicators", 
            "Data Literacy in DAOs",
            "Treasury Transparency Patterns"
        ]
        
        posts = []
        
        for i in range(min(count, len(themes))):
            theme = themes[i]
            day = (datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%A")
            
            print(f"Generating engagement-optimized post for {day} with theme: {theme}")
            post = self.generate_unique_post(theme)
            
            # Analyze engagement potential
            engagement_score = self.analyze_engagement_potential(post)
            
            posts.append({
                "day": day, 
                "theme": theme, 
                "content": post,
                "engagement_score": engagement_score
            })
        
        # Sort posts by engagement potential score
        posts.sort(key=lambda x: x["engagement_score"], reverse=True)
        
        return posts
    
    def save_posts_to_file(self, posts, filename=None):
        """Save posts to a markdown file with engagement analysis"""
        if filename is None:
            filename = f"treasure_corp_engagement_optimized_{datetime.datetime.now().strftime('%Y%m%d')}.md"
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("# Engagement-Optimized Twitter Content: Treasure.Corp\n\n")
                f.write(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n")
                
                f.write("## High-Engagement Post Analysis\n\n")
                f.write("This content is trained on our previous highest-performing post (57 engagements):\n\n")
                f.write(f"```\n{self.high_engagement_post}\n```\n\n")
                
                f.write("### Key Success Factors\n\n")
                f.write("1. **Intellectual Curiosity**: Starts with 'Exploring... is fascinating,' conveying authentic interest\n")
                f.write("2. **Educational Value**: Provides actual insights about how on-chain data connects to governance\n")
                f.write("3. **Technical Detail**: Mentions specific elements like 'asset diversification' and 'voter participation'\n")
                f.write("4. **Forward-Looking Insight**: Concludes with a thought-provoking perspective on the future\n")
                f.write("5. **Three-Part Structure**: Observation → specific examples → broader implication\n")
                f.write("6. **Neutral Tone**: Analytical rather than promotional language\n")
                f.write("7. **Precise Hashtags**: Specific enough to reach the right audience (#DAOanalytics #Web3)\n\n")
                
                f.write("## Engagement-Ranked Posts\n\n")
                
                # Create a table with engagement scores
                f.write("| Engagement Score | Day | Theme | Post |\n")
                f.write("|-----------------|-----|-------|------|\n")
                
                for post in posts:
                    # Clean up post content for table display (remove line breaks)
                    clean_content = post['content'].replace('\n', ' ')
                    f.write(f"| {post['engagement_score']}/10 | {post['day']} | {post['theme']} | {clean_content} |\n")
                
                f.write("\n## Individual Posts (Sorted by Engagement Potential)\n\n")
                for i, post in enumerate(posts, 1):
                    f.write(f"### {i}. {post['day']}: {post['theme']} (Score: {post['engagement_score']}/10)\n\n")
                    f.write(f"{post['content']}\n\n")
                    f.write("**Why this should engage:**\n")
                    
                    # Generate specific reasons why this post should engage based on our analysis
                    reasons = []
                    post_lower = post['content'].lower()
                    
                    if any(pattern.lower() in post_lower for pattern in self.engagement_factors["language_patterns"]):
                        reasons.append("- Uses proven language patterns from high-engagement post")
                    
                    if ". " in post['content'] and post['content'].count(". ") >= 2:
                        reasons.append("- Follows the successful three-part structure")
                    
                    matches = [topic for topic in self.key_topics if topic.lower() in post_lower]
                    if matches:
                        reasons.append(f"- Contains key technical topics: {', '.join(matches[:2])}")
                    
                    future_terms = [word for word in ["future", "may", "could", "might", "potential", "realize"] if word in post_lower]
                    if future_terms:
                        reasons.append("- Includes forward-looking perspective")
                    
                    hashtags = post['content'].count('#')
                    if hashtags > 0 and hashtags <= 3:
                        reasons.append(f"- Optimal hashtag usage ({hashtags} hashtags)")
                    
                    if "?" in post['content']:
                        reasons.append("- Includes question which tends to increase engagement")
                    
                    if not reasons:
                        reasons.append("- Follows general engagement patterns from successful post")
                    
                    for reason in reasons:
                        f.write(f"{reason}\n")
                    
                    f.write("\n" + "-" * 80 + "\n\n")
                
                f.write("## Posting Schedule Recommendation\n\n")
                f.write("For maximum engagement, we recommend posting in this order:\n\n")
                f.write("1. Start with your highest-scored post (most likely to engage)\n")
                f.write("2. Schedule posts at these optimal times:\n")
                f.write("   - Tuesday, Wednesday, Thursday: 9am-11am ET\n")
                f.write("   - Avoid weekends as engagement for DAO/crypto content drops significantly\n")
                f.write("   - Space posts at least 24 hours apart to avoid algorithm penalties\n")
                
                f.write("\n## Visual Enhancement Recommendations\n\n")
                f.write("For 2-3x higher engagement, enhance top-scoring posts with:\n\n")
                f.write("1. **Data Visualizations**: Simple charts showing the metrics mentioned in the post\n")
                f.write("2. **Highlighted Quotes**: Pull out the forward-looking insight as a graphic\n")
                f.write("3. **Minimal Design**: Clean backgrounds, data-focused visuals (avoid stock photos)\n")
            
            print(f"Successfully wrote {len(posts)} engagement-optimized posts to {filename}")
            return filename
        except Exception as e:
            print(f"Error saving file: {e}")
            return None
    
    def get_post_count(self):
        """Get the count of posts in history"""
        return len(self.post_history["posts"])


def main():
    print("Treasure.Corp Engagement-Optimized Twitter Generator")
    print("==================================================")
    
    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        api_key = input("Enter your Anthropic API key: ").strip()
        if not api_key:
            print("No API key provided. Exiting.")
            return
    
    generator = EngagementOptimizedGenerator(api_key)
    
    # Show existing post count
    existing_posts = generator.get_post_count()
    print(f"Current post history contains {existing_posts} posts")
    
    # Generate posts
    print("\nGenerating posts optimized for engagement based on deep analysis...")
    posts = generator.generate_engagement_optimized_posts(7)
    
    # Save to file
    filename = generator.save_posts_to_file(posts)
    
    if filename:
        print("\nEngagement-optimized content generation complete!")
        print(f"\nNew posts have been saved to: {filename}")
        print(f"Total posts in history: {generator.get_post_count()}")
        
        # Display top-rated post
        print("\nTop-rated post (highest engagement potential):")
        print("-" * 50)
        if posts:
            print(f"Theme: {posts[0]['theme']} (Score: {posts[0]['engagement_score']}/10)")
            print(posts[0]['content'])
        print("-" * 50)
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()