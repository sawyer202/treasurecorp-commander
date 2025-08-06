#!/usr/bin/env python3
"""
TreasureCorp Commander - Mobile App Backend API
FastAPI backend that ties all components together
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import json
import sqlite3
from datetime import datetime, timedelta
import logging
import os
from contextlib import asynccontextmanager

# Import our existing modules
from dao_monitoring_llm import DAOMonitoringLLM
from aggressive_growth_config import AggressiveGrowthConfig
from growth_strategy_config import GrowthStrategyConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global instances
dao_monitor = None
growth_config = None
active_connections: List[WebSocket] = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global dao_monitor, growth_config
    dao_monitor = DAOMonitoringLLM()
    growth_config = AggressiveGrowthConfig()
    
    # Start background monitoring
    asyncio.create_task(background_monitoring())
    
    yield
    
    # Shutdown
    logger.info("Shutting down TreasureCorp Commander API")

app = FastAPI(
    title="TreasureCorp Commander API",
    description="Mobile app backend for DAO monitoring and social media growth",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Pydantic models
class ContentItem(BaseModel):
    id: int
    title: str
    summary: str
    platform: str
    status: str
    engagement_score: int
    created_at: datetime

class GrowthMetrics(BaseModel):
    platform: str
    followers: int
    daily_growth: int
    posts_count: int
    engagement_rate: float
    target_progress: float

class PostRequest(BaseModel):
    platform: str
    content: str
    image_url: Optional[str] = None
    schedule_time: Optional[datetime] = None

class ViralAlert(BaseModel):
    content_id: int
    title: str
    viral_score: int
    trending_hashtags: List[str]
    recommended_action: str

# Database helper
def get_db_connection():
    """Get database connection"""
    return sqlite3.connect('dao_monitoring.db')

# Authentication dependency
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify API token"""
    # In production, implement proper JWT validation
    if credentials.credentials != os.getenv("API_TOKEN", "treasurecorp-mobile-2024"):
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return credentials

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected: {len(self.active_connections)} active connections")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected: {len(self.active_connections)} active connections")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")

manager = ConnectionManager()

# API Endpoints

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "active",
        "service": "TreasureCorp Commander API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/dashboard/metrics", response_model=List[GrowthMetrics])
async def get_dashboard_metrics(credentials: HTTPAuthorizationCredentials = Depends(verify_token)):
    """Get real-time growth metrics for mobile dashboard"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get follower counts (mock data for demo)
        platforms = ['twitter', 'linkedin', 'telegram']
        metrics = []
        
        for platform in platforms:
            cursor.execute('''
                SELECT 
                    COALESCE(MAX(followers), 0) as followers,
                    COUNT(DISTINCT DATE(date)) as active_days,
                    COALESCE(AVG(engagement_rate), 0.0) as avg_engagement
                FROM growth_metrics 
                WHERE platform = ? AND date >= date('now', '-7 days')
            ''', (platform,))
            
            result = cursor.fetchone()
            followers = result[0] if result else 0
            
            # Calculate target progress
            target = growth_config.follower_targets.get(platform, 1000)
            progress = (followers / target) * 100 if target > 0 else 0
            
            metrics.append(GrowthMetrics(
                platform=platform,
                followers=followers,
                daily_growth=int(followers / max(result[1], 1)) if result else 0,
                posts_count=growth_config.posting_strategies[platform]['posts_per_day'],
                engagement_rate=result[2] if result and result[2] else 0.0,
                target_progress=min(progress, 100.0)
            ))
        
        conn.close()
        return metrics
        
    except Exception as e:
        logger.error(f"Error fetching dashboard metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch metrics")

@app.get("/api/content/recent", response_model=List[ContentItem])
async def get_recent_content(
    limit: int = 20,
    platform: Optional[str] = None,
    credentials: HTTPAuthorizationCredentials = Depends(verify_token)
):
    """Get recent content items for mobile app"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = '''
            SELECT id, title, summary, 'multi' as platform, 
                   CASE WHEN posted_twitter OR posted_linkedin OR posted_telegram 
                        THEN 'posted' ELSE 'pending' END as status,
                   engagement_score, discovered_at
            FROM monitored_content 
            ORDER BY discovered_at DESC 
            LIMIT ?
        '''
        
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()
        
        content_items = []
        for row in rows:
            content_items.append(ContentItem(
                id=row[0],
                title=row[1],
                summary=row[2][:200] + "..." if len(row[2]) > 200 else row[2],
                platform=row[3],
                status=row[4],
                engagement_score=row[5] or 0,
                created_at=datetime.fromisoformat(row[6])
            ))
        
        conn.close()
        return content_items
        
    except Exception as e:
        logger.error(f"Error fetching recent content: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch content")

@app.post("/api/content/post")
async def create_post(
    post_request: PostRequest,
    background_tasks: BackgroundTasks,
    credentials: HTTPAuthorizationCredentials = Depends(verify_token)
):
    """Create and schedule a new post"""
    try:
        # Add to background task queue
        background_tasks.add_task(process_manual_post, post_request)
        
        # Broadcast to connected mobile apps
        await manager.broadcast(json.dumps({
            "type": "post_created",
            "platform": post_request.platform,
            "content": post_request.content[:100] + "...",
            "timestamp": datetime.now().isoformat()
        }))
        
        return {
            "status": "success",
            "message": f"Post scheduled for {post_request.platform}",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error creating post: {e}")
        raise HTTPException(status_code=500, detail="Failed to create post")

@app.get("/api/viral/alerts", response_model=List[ViralAlert])
async def get_viral_alerts(credentials: HTTPAuthorizationCredentials = Depends(verify_token)):
    """Get trending content and viral opportunities"""
    try:
        # Mock viral alerts - integrate with real trend analysis
        alerts = [
            ViralAlert(
                content_id=1,
                title="Major DAO Treasury Hack Detected",
                viral_score=95,
                trending_hashtags=["#DAOHack", "#TreasuryDrain", "#DeFiSecurity"],
                recommended_action="Create breaking news thread immediately"
            ),
            ViralAlert(
                content_id=2,
                title="New Governance Proposal Going Viral",
                viral_score=88,
                trending_hashtags=["#DAOGovernance", "#Voting", "#Community"],
                recommended_action="Share analysis and predictions"
            )
        ]
        
        return alerts
        
    except Exception as e:
        logger.error(f"Error fetching viral alerts: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch viral alerts")

@app.get("/api/growth/schedule")
async def get_posting_schedule(
    date: Optional[str] = None,
    credentials: HTTPAuthorizationCredentials = Depends(verify_token)
):
    """Get optimized posting schedule for the day"""
    try:
        target_date = datetime.fromisoformat(date) if date else datetime.now()
        day_of_week = target_date.weekday()
        
        schedule = {}
        for platform in ['twitter', 'linkedin', 'telegram']:
            platform_schedule = growth_config.get_daily_aggressive_schedule(platform, day_of_week)
            schedule[platform] = platform_schedule
        
        return {
            "date": target_date.date().isoformat(),
            "total_posts": sum(len(s) for s in schedule.values()),
            "schedule": schedule
        }
        
    except Exception as e:
        logger.error(f"Error fetching posting schedule: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch schedule")

@app.post("/api/monitoring/start")
async def start_monitoring(
    background_tasks: BackgroundTasks,
    credentials: HTTPAuthorizationCredentials = Depends(verify_token)
):
    """Start the monitoring process manually"""
    try:
        background_tasks.add_task(dao_monitor.daily_monitoring_cycle)
        
        return {
            "status": "success",
            "message": "Monitoring cycle started",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error starting monitoring: {e}")
        raise HTTPException(status_code=500, detail="Failed to start monitoring")

@app.get("/api/analytics/competitors")
async def get_competitor_analysis(credentials: HTTPAuthorizationCredentials = Depends(verify_token)):
    """Get competitor analysis data"""
    competitors = growth_config.get_competitive_analysis_targets()
    
    # Mock competitor data - integrate with real social media APIs
    analysis = {
        "last_updated": datetime.now().isoformat(),
        "competitors": {
            "twitter": [
                {"handle": "@DeepDAOTweets", "followers": 45000, "daily_growth": 125, "engagement_rate": 3.2},
                {"handle": "@MessariCrypto", "followers": 380000, "daily_growth": 200, "engagement_rate": 2.8},
                {"handle": "@DeFiPulse", "followers": 180000, "daily_growth": 85, "engagement_rate": 4.1}
            ],
            "linkedin": [
                {"company": "ConsenSys", "followers": 850000, "weekly_posts": 12, "engagement_rate": 2.5},
                {"company": "Chainanalysis", "followers": 120000, "weekly_posts": 8, "engagement_rate": 3.1}
            ]
        },
        "insights": [
            "Competitors post 12-15 times daily on Twitter",
            "Viral content focuses on breaking news and predictions",
            "LinkedIn performs best with thought leadership content"
        ]
    }
    
    return analysis

# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and send periodic updates
            await asyncio.sleep(30)
            await websocket.send_text(json.dumps({
                "type": "heartbeat",
                "timestamp": datetime.now().isoformat(),
                "active_connections": len(manager.active_connections)
            }))
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Background tasks
async def background_monitoring():
    """Continuous background monitoring"""
    while True:
        try:
            logger.info("Running background monitoring cycle...")
            await dao_monitor.daily_monitoring_cycle()
            
            # Broadcast update to mobile apps
            await manager.broadcast(json.dumps({
                "type": "monitoring_complete",
                "timestamp": datetime.now().isoformat(),
                "message": "New content discovered and processed"
            }))
            
            # Wait 1 hour before next cycle (aggressive monitoring)
            await asyncio.sleep(3600)
            
        except Exception as e:
            logger.error(f"Error in background monitoring: {e}")
            await asyncio.sleep(300)  # Wait 5 minutes on error

async def process_manual_post(post_request: PostRequest):
    """Process a manual post request"""
    try:
        # Generate platform-specific content
        summaries = {post_request.platform: post_request.content}
        
        # Create mock content item
        content_item = {
            'title': 'Manual Post',
            'source': 'mobile_app',
            'url': '',
            'type': 'manual'
        }
        
        # Generate images if needed
        images = dao_monitor.generate_social_images(content_item)
        
        # Post to social media
        await dao_monitor.post_to_social_media(content_item, summaries, images)
        
        logger.info(f"Manual post processed for {post_request.platform}")
        
    except Exception as e:
        logger.error(f"Error processing manual post: {e}")

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Endpoint not found", "status": 404}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "status": 500}

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting TreasureCorp Commander API...")
    print("📱 Mobile app backend ready")
    print("🔗 WebSocket support enabled")
    print("⚡ Real-time monitoring active")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )