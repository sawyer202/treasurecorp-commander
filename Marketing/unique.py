import random
import datetime
import os

class TwitterPostGenerator:
    def __init__(self):
        # Company information
        self.company_name = "Treasure.Corp"
        self.product = "Data-driven treasury solutions for DAOs"
        self.vision = "Treasury Clarity for the Decentralized World"
        
        # Emojis for visual appeal
        self.emojis = ["📊", "📈", "💰", "🚀", "⚡", "🔍", "🧠", "🔐", "🌐", "🧩", 
                       "⚙️", "📱", "🔄", "💼", "📝", "🏆", "📌", "💡", "🛠️", "⚖️"]
        
        # Real DAO benchmarks
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
        
        # Benefits and pain points
        self.benefits = [
            "confident decision-making",
            "seamless governance", 
            "sustainable growth", 
            "treasury clarity", 
            "decentralized financial management",
            "data-driven treasury allocation",
            "transparent governance processes",
            "efficient multi-chain management",
            "optimized token allocations"
        ]
        
        self.pain_points = [
            "complex treasury management", 
            "lack of financial clarity", 
            "governance bottlenecks", 
            "unsustainable growth models", 
            "difficulty tracking decentralized assets",
            "inefficient proposal execution",
            "limited cross-chain visibility",
            "manual treasury reconciliation",
            "poor governance participation"
        ]
        
        # Hashtags by category
        self.hashtags = {
            "brand": ["#TreasureCorp", "#TreasuryClarity", "#DecentralizedTreasury"],
            "industry": ["#DAO", "#DeFi", "#Web3Treasury", "#CryptoGovernance", "#DAOTreasury"],
            "trending": ["#Blockchain", "#CryptoInnovation", "#DAOFinance", "#DecentralizedGrowth", "#Web3"]
        }
        
        # Categories of post templates
        self.categories = {
            "Product": self.generate_product_post,
            "Education": self.generate_education_post,
            "Question": self.generate_question_post,
            "Insight": self.generate_insight_post,
            "Benchmark": self.generate_benchmark_post,
            "Best Practice": self.generate_best_practice_post,
            "Poll": self.generate_poll_post
        }
    
    def get_emoji(self):
        """Get a random emoji"""
        return random.choice(self.emojis)
    
    def get_hashtags(self, count=3):
        """Get a set of hashtags"""
        tags = []
        tags.append(random.choice(self.hashtags["brand"]))
        tags.append(random.choice(self.hashtags["industry"]))
        if count > 2:
            tags.append(random.choice(self.hashtags["trending"]))
        return " ".join(tags)
    
    def get_benefit(self):
        """Get a random benefit"""
        return random.choice(self.benefits)
    
    def get_pain_point(self):
        """Get a random pain point"""
        return random.choice(self.pain_points)
    
    def get_benchmark(self):
        """Get a random benchmark"""
        return random.choice(self.benchmarks)
    
    def generate_product_post(self):
        """Generate a product-focused post"""
        templates = [
            "{emoji} Our {product} helps DAOs achieve {benefit}, turning complex treasury data into actionable insights. {hashtags}",
            "{emoji} {company} provides {benefit} for DAOs, solving the challenge of {pain_point}. Learn more in our bio! {hashtags}",
            "{emoji} The future of DAO treasury management is here. {company}'s solutions deliver {benefit} and eliminate {pain_point}. {hashtags}"
        ]
        template = random.choice(templates)
        return template.format(
            emoji=self.get_emoji(),
            company=self.company_name,
            product=self.product,
            benefit=self.get_benefit(),
            pain_point=self.get_pain_point(),
            hashtags=self.get_hashtags()
        )
    
    def generate_education_post(self):
        """Generate an educational post"""
        stats = [67, 72, 85, 63, 78, 91]
        stat = random.choice(stats)
        templates = [
            "{emoji} Did you know? {stat}% of DAOs struggle with {pain_point}. Our solution provides {benefit} through real-time analytics. {hashtags}",
            "{emoji} Treasury tip: Improve {benefit} by implementing multi-sig thresholds based on spending amounts. {hashtags}",
            "{emoji} Smart DAOs diversify treasury holdings across at least 3 chains to mitigate risk and improve {benefit}. {hashtags}"
        ]
        template = random.choice(templates)
        return template.format(
            emoji=self.get_emoji(),
            stat=stat,
            pain_point=self.get_pain_point(),
            benefit=self.get_benefit(),
            hashtags=self.get_hashtags()
        )
    
    def generate_question_post(self):
        """Generate a question post"""
        templates = [
            "{emoji} How does your DAO currently handle {pain_point}? Our tooling provides {benefit} to solve this common challenge. {hashtags}",
            "{emoji} What metrics do you track to measure DAO treasury health? Most successful DAOs focus on diversification, runway, and governance participation. {hashtags}",
            "{emoji} Is your DAO treasury optimized for both stability and growth? Finding the right balance is key to long-term sustainability. {hashtags}"
        ]
        template = random.choice(templates)
        return template.format(
            emoji=self.get_emoji(),
            pain_point=self.get_pain_point(),
            benefit=self.get_benefit(),
            hashtags=self.get_hashtags()
        )
    
    def generate_insight_post(self):
        """Generate an insight post"""
        trends = [
            "real-world asset tokenization",
            "DAO-to-DAO collaboration",
            "decentralized governance frameworks",
            "data-driven treasury management",
            "multi-chain treasury diversification"
        ]
        percentages = [67, 78, 54, 82, 71]
        
        templates = [
            "{emoji} Industry insight: DAOs with diversified treasuries outperformed single-token treasuries by 3.2x in market downturns. {hashtags}",
            "{emoji} Trend alert! {percentage}% of top DAOs now focus on {trend} to achieve better governance outcomes. {hashtags}",
            "{emoji} Our analysis shows: DAOs using data dashboards achieve 58% higher member participation in governance. {hashtags}"
        ]
        template = random.choice(templates)
        return template.format(
            emoji=self.get_emoji(),
            percentage=random.choice(percentages),
            trend=random.choice(trends),
            hashtags=self.get_hashtags()
        )
    
    def generate_benchmark_post(self):
        """Generate a benchmark post"""
        templates = [
            "{emoji} Benchmark: {benchmark}. How does your DAO compare? Our tools help achieve similar results. {hashtags}",
            "{emoji} Leading DAOs are setting new standards: {benchmark}. We can help you implement similar best practices. {hashtags}",
            "{emoji} DAO excellence in action: {benchmark}. This level of performance is achievable with the right tools and processes. {hashtags}"
        ]
        template = random.choice(templates)
        return template.format(
            emoji=self.get_emoji(),
            benchmark=self.get_benchmark(),
            hashtags=self.get_hashtags()
        )
    
    def generate_best_practice_post(self):
        """Generate a best practice post"""
        best_practices = [
            "Diversify treasury assets across multiple chains to reduce single-point-of-failure risk",
            "Set clear allocation thresholds for operating expenses vs. long-term treasury reserves",
            "Create governance structures with multi-level approval thresholds based on spending amount",
            "Implement real-time treasury dashboards accessible to all token holders for transparency",
            "Establish quarter-by-quarter treasury allocation strategies with regular community review",
            "Maintain at least 18 months of runway in stablecoins for operational sustainability",
            "Use weighted voting systems to balance large and small token holder influence"
        ]
        
        templates = [
            "{emoji} DAO Best Practice: {practice}. {hashtags}",
            "{emoji} Treasury management tip: {practice}. Top DAOs implement this for improved governance. {hashtags}",
            "{emoji} Want better DAO operations? {practice}. This single change can significantly improve outcomes. {hashtags}"
        ]
        template = random.choice(templates)
        return template.format(
            emoji=self.get_emoji(),
            practice=random.choice(best_practices),
            hashtags=self.get_hashtags()
        )
    
    def generate_poll_post(self):
        """Generate a poll post"""
        polls = [
            "How often does your DAO review its treasury allocation strategy - weekly, monthly, quarterly, or only when needed?",
            "What's your DAO's percentage split between protocol tokens, stables, and other assets?",
            "Which treasury management challenge impacts your DAO most: volatility, diversification, or governance approval speeds?",
            "What's your preferred governance mechanism for treasury decisions: Snapshot, on-chain voting, multi-sig, or working groups?"
        ]
        
        templates = [
            "{emoji} Community poll: {question} Share your approach! {hashtags}",
            "{emoji} We're curious: {question} Your insights help us build better tools. {hashtags}",
            "{emoji} Quick question for DAO treasurers: {question} Comment below! {hashtags}"
        ]
        template = random.choice(templates)
        return template.format(
            emoji=self.get_emoji(),
            question=random.choice(polls),
            hashtags=self.get_hashtags()
        )
    
    def generate_random_post(self):
        """Generate a random post from any category"""
        category = random.choice(list(self.categories.keys()))
        generator_function = self.categories[category]
        return generator_function()
    
    def generate_posts(self, count=10):
        """Generate a specified number of posts"""
        posts = []
        for _ in range(count):
            posts.append(self.generate_random_post())
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
                
                f.write("## DAO Benchmark Data\n\n")
                f.write("These real-world examples can be referenced in your posts:\n\n")
                for benchmark in self.benchmarks:
                    f.write(f"- {benchmark}\n")
                f.write("\n")
                
                f.write("## Generated Posts\n\n")
                for i, post in enumerate(posts, 1):
                    f.write(f"### Post {i}\n\n")
                    f.write(f"{post}\n\n")
                    f.write("-" * 80 + "\n\n")
            
            print(f"Successfully wrote {len(posts)} posts to {filename}")
            return filename
        except Exception as e:
            print(f"Error with UTF-8 encoding: {e}")
            
            # Fallback to ASCII encoding
            try:
                with open(filename, "w", encoding="ascii", errors="ignore") as f:
                    f.write("# Generated Twitter Posts for Treasure.Corp\n\n")
                    for i, post in enumerate(posts, 1):
                        f.write(f"### Post {i}\n\n")
                        f.write(f"{post}\n\n")
                        f.write("-" * 80 + "\n\n")
                print(f"Successfully wrote posts with ASCII encoding to {filename}")
                return filename
            except Exception as e2:
                print(f"Could not save file: {e2}")
                return None

def main():
    """Main function"""
    print("Generating Twitter posts for Treasure.Corp...")
    
    generator = TwitterPostGenerator()
    
    # How many posts to generate
    num_posts = 15
    posts = generator.generate_posts(num_posts)
    
    # Save to file
    filename = generator.save_posts_to_file(posts)
    
    if filename:
        print("\nSample posts:")
        print("-" * 50)
        for i in range(min(3, len(posts))):
            print(posts[i])
            print()
        print("-" * 50)
        
        print(f"\nOpen {filename} to view all posts for copy-pasting to Buffer.")
        
        print("\nText-to-Image Tools for Twitter Posts:")
        print("1. Canva (www.canva.com)")
        print("2. Pablo by Buffer (built into Buffer)")
        print("3. Adobe Express (www.adobe.com/express)")
        print("4. Visme (www.visme.co)")
        print("5. Piktochart (piktochart.com)")
    
    # Keep console window open
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()