#!/usr/bin/env python3
"""
Test script to manually trigger DAO monitoring and post creation
"""

import asyncio
from dao_monitoring_llm import DAOMonitoringLLM
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_automatic_post():
    """Test the automatic post creation system"""
    logger.info("Starting ad-hoc automatic post test...")
    
    # Initialize the monitoring system
    monitor = DAOMonitoringLLM()
    
    # Run the daily monitoring cycle (this will collect content and post automatically)
    await monitor.daily_monitoring_cycle()
    
    logger.info("Ad-hoc test completed!")

if __name__ == "__main__":
    asyncio.run(test_automatic_post())