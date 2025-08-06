import os
import requests
import json
import datetime
import random
from typing import List, Dict, Tuple

# Configuration - Use environment variables
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
COMPANY_NAME = "Treasure.Corp"
INDUSTRY = "DAO Treasury Management"
PRODUCT_SERVICE = "Data-driven treasury solutions for DAOs"
KEY_BENEFITS = [
    "confident decision-making", 
    "seamless governance", 
    "sustainable growth", 
    "treasury clarity", 
    "decentralized financial management"
]
PAIN_POINTS = [
    "complex treasury management", 
    "lack of financial clarity", 
    "governance bottlenecks", 
    "unsustainable growth models", 
    "difficulty tracking decentralized assets"
]
HASHTAGS = {
    "brand": ["#TreasureCorp", "#TreasuryClarity", "#DecentralizedTreasury"],
    "industry": ["#DAO", "#DeFi", "#Web3Treasury", "#CryptoGovernance", "#DAOTreasury"], 
    "trending": ["#Blockchain", "#CryptoInnovation", "#DAOFinance", "#DecentralizedGrowth", "#Web3"] 
}

# Content themes by day of week
WEEKLY_THEMES = {
    0: "Brand & Product", # Monday
    1: "Treasury Education", # Tuesday
    2: "Community Questions", # Wednesday
    3: "Industry Insights", # Thursday
    4: "Governance Engagement", # Friday
    5: "Treasury Management Polls", # Saturday
    6: "DAO Wisdom & Motivation" # Sunday
}

# Post types with templates - NO EMOJIS VERSION
POST_TEMPLATES = {
    "Brand & Product": [
        "Discover how {benefit} can transform your {activity} with {company}'s {product}. {hashtags}",
        "Our vision at {company}: {mission_statement} - building tools to {goal}. {hashtags}",
        "Data-driven treasury decisions lead to stronger DAOs - our {product} helps achieve {benefit}. {hashtags}"
    ],
    "Treasury Education": [
        "{statistic}% of DAOs struggle with {pain_point} - we solve this with real-time analytics and governance tools. {hashtags}",
        "Data-driven treasury tip: {quick_tip} - improve your DAO's financial clarity today. {hashtags}",
        "Did you know our {product} can help you {benefit}? Simple implementation, powerful results. {hashtags}"
    ],
    "Community Questions": [
        "Question for DAO treasurers: How are you currently tracking multi-chain assets? Our {product} helps simplify this challenge. {hashtags}",
        "What's your biggest treasury management challenge - asset diversification, transparency, or governance approvals? {hashtags}",
        "Curious: What percentage of your DAO treasury is held in stablecoins vs. protocol tokens? {hashtags}"
    ],
    "Industry Insights": [
        "Industry update: {recent_development} is changing how DAOs approach {topic} - our take: {company_perspective} {hashtags}",
        "Trend alert! {percentage}% of DAOs now focus on {trend} - this directly impacts community engagement and treasury efficiency. {hashtags}",
        "Our prediction for {industry} in 2025: {prediction} - what's your take? {hashtags}"
    ],
    "Governance Engagement": [
        "How does your DAO make treasury decisions? Snapshot voting, on-chain, multi-sig, or working group delegation? {hashtags}",
        "Only {statistic}% of DAOs have real-time treasury dashboards - how is your community tracking this vital metric? {hashtags}",
        "What KPIs does your DAO use to measure treasury effectiveness? We're building better tools based on your feedback. {hashtags}"
    ],
    "Treasury Management Polls": [
        "How often does your DAO review its treasury allocation strategy - weekly, monthly, quarterly, or only when needed? {hashtags}",
        "Treasury diversification check: What's your split between protocol tokens, stables, other crypto, and real-world assets? {hashtags}",
        "The one treasury tool our DAO needs most is ____________. Share your wishlist item and we might build it! {hashtags}"
    ],
    "DAO Wisdom & Motivation": [
        "DAO Best Practice: Diversify your treasury assets across multiple chains to reduce single-point-of-failure risk. {hashtags}",
        "DAO Best Practice: Set clear allocation thresholds for operating expenses vs. long-term treasury reserves. {hashtags}",
        "DAO Best Practice: Create governance structures with multi-level approval thresholds based on spending amount. {hashtags}"
    ]
}

# Fill-in content for the templates
CONTENT_FILLERS = {
    "activity": ["DAO governance", "treasury management", "community decision-making", "token allocation", "protocol growth", "financial planning"],
    "topic": ["decentralized governance", "treasury optimization", "sustainable DAO models", "on-chain transparency", "community-driven finance"],
    "statistic": [75, 82, 67, 91, 63],
    "solution_point_1": ["Visualizing treasury data for better governance", "Simplifying complex financial decisions", "Enhancing community transparency", "Optimizing token allocations", "Eliminating manual tracking errors"],
    "solution_point_2": ["Providing real-time on-chain analytics", "Offering customizable DAO dashboards", "Integrating with your existing Web3 tools", "Delivering actionable treasury insights", "Supporting your community with governance tools"],
    "solution_point_3": ["Ensuring scalability for growing DAOs", "Maintaining compliance with evolving regulations", "Providing 24/7 support for global communities", "Regular feature updates based on community feedback", "Custom reporting for multisig holders"],
    "step_1": ["Connect your DAO treasury wallets", "Identify your governance requirements", "Link your multisig accounts", "Select your preferred dashboard views", "Input your token information"],
    "step_2": ["Customize your treasury dashboard", "Onboard your core contributors", "Import your historical treasury data", "Configure voting thresholds", "Schedule your first governance review"],
    "step_3": ["Start making data-driven decisions", "Scale as your DAO community grows", "Measure your treasury efficiency", "Share insights across working groups", "Optimize allocations based on analytics"],
    "quick_tip": ["Use the 'Treasury Snapshot' feature for governance calls", "Configure weekly reports for token holders", "Track proposal spending in real-time", "Set up treasury diversification alerts", "Create custom dashboards for different working groups"],
    "customer_name": ["CryptoDAO", "DeFi Collective", "GovStack DAO", "Metaverse Creators", "Blockchain Foundation"],
    "specific_result": ["a 45% increase in treasury efficiency", "30% reduction in governance overhead", "$1.2M in optimized token allocations", "community participation up by 65%", "proposal processing time reduced by 80%"],
    "timeframe": ["3 months", "2 governance cycles", "the first quarter", "6 weeks", "just one month"],
    "customer_title": ["DAO Facilitator", "Treasury Multi-sig", "Governance Lead", "Protocol Steward", "Community Manager"],
    "problem": ["inefficient treasury management", "high governance overhead", "community disengagement", "manual tracking errors", "transparency gaps"],
    "result": ["doubled governance participation", "40% faster proposal execution", "significant gas savings", "seamless cross-chain treasury visibility", "rapid protocol development"],
    "pain_point_description": ["Spending hours reconciling on-chain transactions", "Losing community trust due to lack of transparency", "Struggling with multiple treasury wallets", "Working groups making siloed decisions", "Limited visibility into token performance"],
    "success_description": ["Automated treasury dashboard saving 20+ hours weekly", "95% voting participation on key proposals", "Real-time multi-chain reporting", "Unified governance platform", "Comprehensive treasury performance metrics"],
    "recent_development": ["Zero-knowledge proofs for privacy", "Regulatory clarity in DeFi", "L2 scalability solutions", "On-chain governance innovations", "Multi-chain treasury management"],
    "company_perspective": ["it's an opportunity for DAOs to evolve governance models", "early adopters will gain significant protocol advantages", "a balanced treasury strategy yields the best results", "this requires rethinking traditional DAO structures", "focusing on sustainability is key to long-term success"],
    "percentage": [67, 78, 54, 82, 71],
    "trend": ["real-world asset tokenization", "DAO-to-DAO collaboration", "decentralized governance frameworks", "data-driven treasury management", "quadratic funding models"],
    "brief_explanation": ["it directly impacts community engagement and retention", "it significantly reduces governance overhead long-term", "it provides protocol advantages in a competitive ecosystem", "it helps future-proof your DAO model", "it addresses evolving token holder expectations"],
    "prediction": ["analytics will transform DAO governance models", "treasury diversification will become the standard rather than exception", "integrated multi-chain dashboards will replace single-chain views", "sustainability metrics will impact token value", "cross-DAO collaboration tools will evolve dramatically"],
    "activity": ["celebrates governance milestones", "collaborates across working groups", "starts each week with a community call", "contributes to public goods funding", "promotes continuous DAO education"],
    "value": ["transparency", "innovation", "community-first", "continuous improvement", "decentralized decision-making"],
    "outcome": ["DAO experiences", "protocol development", "contributor satisfaction", "ecosystem leadership", "sustainable treasury growth"],
    "employee_name": ["Alex", "Jordan", "Taylor", "Casey", "Morgan"],
    "job_title": ["DAO Success Steward", "Lead Protocol Developer", "Community Growth Strategist", "Treasury Dashboard Designer", "Governance Facilitator"],
    "job_description": ["helping DAOs achieve their governance goals", "coding on-chain treasury solutions", "creating impactful community campaigns", "designing intuitive treasury interfaces", "optimizing governance processes"],
    "hobby": ["contributing to other DAOs", "hosting crypto podcasts", "participating in hackathons", "competing in trading competitions", "writing Web3 education materials"],
    "value_1": ["Community First", "Continuous Innovation", "Radical Transparency", "Decentralized Governance", "Excellence in Treasury Management"],
    "value_2": ["Data-Driven Decisions", "Token Holder Empowerment", "Sustainable DAO Practices", "Inclusive Governance", "Growth Mindset"],
    "value_3": ["Cross-Chain Interoperability", "Public Goods Impact", "Ethical Treasury Management", "Adaptive Resilience", "Protocol Excellence"],
    "example": ["our weekly DAO spotlight sessions", "our open-source contribution policy", "our transparent treasury dashboard visible on-chain", "our cross-functional working groups", "our token-weighted feedback system"],
    "industry_problem": ["treasury diversification", "governance participation", "contributor retention", "multi-chain management", "protocol differentiation"],
    "feature_1": ["Automated treasury reporting", "Data-driven allocation recommendations", "Multi-chain integration capabilities", "Mobile governance access", "Custom DAO dashboards"],
    "feature_2": ["Working group collaboration tools", "Real-time on-chain analytics", "Proposal template library", "Priority community support", "Governance education resources"],
    "feature_3": ["Advanced multi-sig features", "DAO scalability options", "On-chain API access", "Custom DAO branding", "Regulatory compliance tools"],
    "common_approach": ["focusing only on token price", "following traditional DAO models", "prioritizing features over governance experience", "reactive treasury management", "siloed working groups"],
    "better_approach": ["building sustainable treasury systems", "setting new governance benchmarks", "designing for token holder engagement", "proactive treasury optimization", "cross-DAO collaboration"],
    "limitation": ["single-chain exposure", "market volatility", "limited treasury diversification", "governance skill gaps", "proposal inefficiencies"],
    "person_name": ["Jamie Rodriguez", "Taylor Kim", "Alex Washington", "Jordan Smith", "Casey Morgan"],
    "title": ["Head of DAO Solutions", "Treasury Success Director", "Chief Governance Officer", "VP of Protocol Operations", "Strategic Growth Lead"],
    "years": [8, 12, 15, 10, 20],
    "speciality": ["treasury dashboard development", "DAO governance experience", "multi-chain integration", "operational efficiency for DAOs", "protocol partnerships"],
    "mission_statement": ["to empower DAOs with data-driven solutions", "to transform how communities manage their treasury", "to create technology that makes governance accessible", "to simplify complex on-chain processes", "to build tools that enable sustainable DAO growth"],
    "goal": ["make DAOs more efficient", "help communities reach their governance potential", "transform treasury management standards", "create exceptional token holder experiences", "develop solutions that scale with your protocol"],
    "benefit": ["increased treasury efficiency", "better on-chain insights", "streamlined governance", "enhanced community participation", "gas cost reduction"]
}

def get_anthropic_response(prompt: str) -> str:
    """Get a response from Anthropic API"""
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "content-type": "application/json"
    }
    
    data = {
        "model": "claude-3-opus-20240229",
        "max_tokens": 1000,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        return response.json()["content"][0]["text"]
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return f"Error generating content: {response.status_code}"

def generate_post_with_anthropic(theme: str, company_info: Dict) -> str:
    """Generate a Twitter post using Anthropic API"""
    prompt = f"""
    Create a Twitter post for {company_info['company_name']}, a company in the {company_info['industry']} industry.
    The post should focus on the theme: {theme}.
    Key product benefits: {', '.join(company_info['benefits'])}
    Customer pain points: {', '.join(company_info['pain_points'])}
    
    The post should be catchy, professional, and have a clear call to action.
    Keep it under 280 characters, include relevant hashtags, and make it engaging.
    DO NOT include any emojis or special characters, only use standard ASCII characters.
    
    Only give me the text for the Twitter post, nothing else.
    """
    
    return get_anthropic_response(prompt)

def fill_template(template: str, company_info: Dict) -> str:
    """Fill in a template with random content from our library"""
    filled_template = template
    
    # Basic company info
    filled_template = filled_template.replace("{company}", company_info["company_name"])
    filled_template = filled_template.replace("{product}", company_info["product_service"])
    
    # Identify all placeholders in the template
    import re
    placeholders = re.findall(r'\{([^}]+)\}', filled_template)
    
    # Fill each placeholder
    for placeholder in placeholders:
        # Skip if we already replaced company or product
        if placeholder in ["company", "product"]:
            continue
            
        # If we have content for this placeholder, use it
        if placeholder in CONTENT_FILLERS:
            replacement = random.choice(CONTENT_FILLERS[placeholder])
            filled_template = filled_template.replace(f"{{{placeholder}}}", str(replacement))
        # If it's a hashtag placeholder, insert hashtags
        elif placeholder == "hashtags":
            # Select some hashtags
            selected_hashtags = random.sample(company_info["hashtags"]["brand"], 1)
            selected_hashtags += random.sample(company_info["hashtags"]["industry"], 1)
            selected_hashtags += random.sample(company_info["hashtags"]["trending"], 1)
            hashtag_str = " ".join(selected_hashtags)
            filled_template = filled_template.replace(f"{{{placeholder}}}", hashtag_str)
    
    return filled_template

def generate_post_from_template(theme: str, company_info: Dict) -> str:
    """Generate a post from our template library"""
    if theme in POST_TEMPLATES:
        template = random.choice(POST_TEMPLATES[theme])
        return fill_template(template, company_info)
    else:
        # Fallback to Anthropic if we don't have templates for this theme
        return generate_post_with_anthropic(theme, company_info)

def get_day_theme(date: datetime.datetime) -> str:
    """Get the theme for a specific day"""
    day_of_week = date.weekday()
    return WEEKLY_THEMES[day_of_week]

def generate_posts_for_week(company_info: Dict) -> List[Tuple[str, str]]:
    """Generate posts for the entire week"""
    today = datetime.datetime.now()
    posts = []
    
    # Generate a post for each day of the week
    for i in range(7):
        day = today + datetime.timedelta(days=i)
        theme = get_day_theme(day)
        post = generate_post_from_template(theme, company_info)
        posts.append((day.strftime("%A"), post))
    
    return posts

def save_posts_to_file(posts: List[Tuple[str, str]], filename: str):
    """Save generated posts to a file for easy copy-pasting to Buffer"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("# Generated Twitter Posts for Treasure.Corp\n\n")
            f.write(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n")
            
            for day, post in posts:
                f.write(f"## {day}\n\n")
                f.write(f"{post}\n\n")
                f.write("-" * 80 + "\n\n")
        print(f"Successfully wrote posts to {filename}")
    except Exception as e:
        # Fallback to ASCII encoding if UTF-8 fails
        print(f"Error with UTF-8 encoding: {e}")
        print("Trying with ASCII encoding and ignoring errors...")
        
        with open(filename, "w", encoding="ascii", errors="ignore") as f:
            f.write("# Generated Twitter Posts for Treasure.Corp\n\n")
            f.write(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n")
            
            for day, post in posts:
                f.write(f"## {day}\n\n")
                f.write(f"{post}\n\n")
                f.write("-" * 80 + "\n\n")
        print(f"Successfully wrote posts with ASCII encoding to {filename}")

def main():
    """Main function to generate posts"""
    print("Generating Twitter posts for Treasure.Corp...")
    
    company_info = {
        "company_name": COMPANY_NAME,
        "industry": INDUSTRY,
        "product_service": PRODUCT_SERVICE,
        "benefits": KEY_BENEFITS,
        "pain_points": PAIN_POINTS,
        "hashtags": HASHTAGS
    }
    
    # Generate posts
    posts = generate_posts_for_week(company_info)
    
    # Save to file
    filename = f"treasure_corp_twitter_posts_{datetime.datetime.now().strftime('%Y%m%d')}.md"
    save_posts_to_file(posts, filename)
    
    print(f"Generated {len(posts)} posts and saved to {filename}")
    print("\nSample post for today:")
    print("-" * 50)
    print(posts[0][1])
    print("-" * 50)
    print(f"\nOpen {filename} to view all posts for copy-pasting to Buffer.")
    input("\nPress Enter to exit...")  # Add this line to keep console window open

if __name__ == "__main__":
    main()