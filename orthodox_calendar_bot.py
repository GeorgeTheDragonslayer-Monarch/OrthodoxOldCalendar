#!/usr/bin/env python3
"""
Orthodox Calendar Discord Bot

Fetches daily Orthodox calendar information from orthocal.info
and posts it to a Discord channel via webhook.

Author: Manus AI Assistant
License: MIT
"""

import json
import requests
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('orthodox_calendar_bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class OrthodoxCalendarBot:
    """Main bot class for fetching and posting Orthodox calendar data."""
    
    def __init__(self, webhook_url: str, calendar_type: str = "gregorian"):
        """
        Initialize the bot with webhook URL and calendar type.
        
        Args:
            webhook_url: Discord webhook URL
            calendar_type: Either "gregorian" or "julian"
        """
        self.webhook_url = webhook_url
        self.calendar_type = calendar_type
        self.api_base_url = "https://orthocal.info/api"
        
        # Discord embed color codes (liturgical colors)
        self.colors = {
            "gold": 16766720,      # Gold/Yellow for major feasts
            "red": 16711680,       # Red for martyrs
            "purple": 8388736,     # Purple for Lent
            "green": 65280,        # Green for ordinary time
            "white": 16777215,     # White for major feasts
            "blue": 255,           # Blue for Theotokos
            "default": 5814783     # Default Discord blue
        }
    
    def fetch_calendar_data(self) -> Optional[Dict[str, Any]]:
        """
        Fetch today's calendar data from orthocal.info API.
        
        Returns:
            Dictionary containing calendar data or None if failed
        """
        try:
            url = f"{self.api_base_url}/{self.calendar_type}/"
            logger.info(f"Fetching calendar data from: {url}")
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info("Successfully fetched calendar data")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch calendar data: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return None
    
    def format_date_title(self, data: Dict[str, Any]) -> str:
        """
        Format the main title with date and liturgical information.
        
        Args:
            data: Calendar data from API
            
        Returns:
            Formatted title string
        """
        try:
            # Extract date information
            year = data.get('year', '')
            month = data.get('month', '')
            day = data.get('day', '')
            
            # Create date object for formatting
            if year and month and day:
                date_obj = datetime(int(year), int(month), int(day))
                date_str = date_obj.strftime("%B %d, %Y")
            else:
                date_str = "Today"
            
            # Get liturgical title
            titles = data.get('titles', [])
            liturgical_title = ""
            if titles:
                liturgical_title = " - " + titles[0]
            
            return f"{date_str}{liturgical_title}"
            
        except (ValueError, TypeError) as e:
            logger.warning(f"Error formatting date title: {e}")
            return "Orthodox Calendar - Today"
    
    def format_fast_info(self, data: Dict[str, Any]) -> str:
        """
        Format fasting information.
        
        Args:
            data: Calendar data from API
            
        Returns:
            Formatted fast description
        """
        fast_level = data.get('fast_level', 0)
        fast_desc = data.get('fast_level_desc', '')
        fast_exception = data.get('fast_exception_desc', '')
        
        if fast_level == 0:
            return "No fasting"
        elif fast_desc:
            result = fast_desc
            if fast_exception:
                result += f" — {fast_exception}"
            return result
        else:
            return "Fasting day"
    
    def format_feasts(self, data: Dict[str, Any]) -> Optional[str]:
        """
        Format feast information.
        
        Args:
            data: Calendar data from API
            
        Returns:
            Formatted feast string or None if no feasts
        """
        feasts = data.get('feasts', [])
        if not feasts:
            return None
        
        return ", ".join(feasts)
    
    def format_saints(self, data: Dict[str, Any]) -> Optional[str]:
        """
        Format saints commemorations.
        
        Args:
            data: Calendar data from API
            
        Returns:
            Formatted saints string or None if no saints
        """
        saints = data.get('saints', [])
        if not saints:
            return None
        
        # Limit to first 5 saints to avoid message length issues
        saints_list = saints[:5]
        result = " • ".join(saints_list)
        
        if len(saints) > 5:
            result += f" • and {len(saints) - 5} more..."
        
        return result
    
    def format_readings(self, data: Dict[str, Any]) -> Optional[str]:
        """
        Format scripture readings (abbreviated).
        
        Args:
            data: Calendar data from API
            
        Returns:
            Formatted readings string or None if no readings
        """
        readings = data.get('readings', [])
        if not readings:
            return None
        
        # Extract reading references (not full text)
        reading_refs = []
        for reading in readings[:6]:  # Limit to first 6 readings
            if 'display' in reading:
                reading_refs.append(reading['display'])
        
        if reading_refs:
            result = " • ".join(reading_refs)
            if len(readings) > 6:
                result += " • ..."
            return result
        
        return None
    
    def determine_embed_color(self, data: Dict[str, Any]) -> int:
        """
        Determine appropriate embed color based on liturgical information.
        
        Args:
            data: Calendar data from API
            
        Returns:
            Discord color integer
        """
        # Check for major feasts
        feasts = data.get('feasts', [])
        if feasts:
            # Major feasts typically use gold/white
            return self.colors['gold']
        
        # Check fast level for purple (Lent)
        fast_level = data.get('fast_level', 0)
        if fast_level >= 3:  # Strict fasting
            return self.colors['purple']
        
        # Check for martyrs in saints
        saints = data.get('saints', [])
        for saint in saints:
            if 'martyr' in saint.lower():
                return self.colors['red']
        
        # Default color
        return self.colors['default']
    
    def create_discord_embed(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create Discord embed structure from calendar data.
        
        Args:
            data: Calendar data from API
            
        Returns:
            Discord embed dictionary
        """
        embed = {
            "title": self.format_date_title(data),
            "color": self.determine_embed_color(data),
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {
                "text": "Orthodox Calendar • orthocal.info",
                "icon_url": "https://orthocal.info/favicon.ico"
            },
            "fields": []
        }
        
        # Add fast information as description
        fast_info = self.format_fast_info(data)
        if fast_info:
            embed["description"] = fast_info
        
        # Add feasts field
        feasts = self.format_feasts(data)
        if feasts:
            embed["fields"].append({
                "name": "🎉 Feasts",
                "value": feasts,
                "inline": False
            })
        
        # Add saints field
        saints = self.format_saints(data)
        if saints:
            embed["fields"].append({
                "name": "✨ Commemorations",
                "value": saints,
                "inline": False
            })
        
        # Add readings field
        readings = self.format_readings(data)
        if readings:
            embed["fields"].append({
                "name": "📖 Scripture Readings",
                "value": readings,
                "inline": False
            })
        
        return embed
    
    def post_to_discord(self, embed: Dict[str, Any]) -> bool:
        """
        Post the formatted message to Discord via webhook.
        
        Args:
            embed: Discord embed dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            payload = {
                "username": "Orthodox Calendar",
                "avatar_url": "https://orthocal.info/favicon.ico",
                "embeds": [embed]
            }
            
            logger.info("Posting message to Discord...")
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            logger.info("Successfully posted to Discord")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to post to Discord: {e}")
            
            # Try fallback simple message
            try:
                fallback_payload = {
                    "content": f"**{embed['title']}**\n{embed.get('description', '')}\n\nView full details at https://orthocal.info/",
                    "username": "Orthodox Calendar"
                }
                
                response = requests.post(
                    self.webhook_url,
                    json=fallback_payload,
                    timeout=30
                )
                response.raise_for_status()
                
                logger.info("Posted fallback message to Discord")
                return True
                
            except requests.exceptions.RequestException as fallback_error:
                logger.error(f"Fallback message also failed: {fallback_error}")
                return False
    
    def run(self) -> bool:
        """
        Main execution method.
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("Starting Orthodox Calendar Bot")
        
        # Fetch calendar data
        data = self.fetch_calendar_data()
        if not data:
            logger.error("Failed to fetch calendar data")
            return False
        
        # Create Discord embed
        embed = self.create_discord_embed(data)
        
        # Post to Discord
        success = self.post_to_discord(embed)
        
        if success:
            logger.info("Bot execution completed successfully")
        else:
            logger.error("Bot execution failed")
        
        return success

def load_config() -> Dict[str, Any]:
    """
    Load configuration from file or environment variables.
    
    Returns:
        Configuration dictionary
    """
    config = {}
    
    # Try to load from config.json file
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        logger.info("No config.json found, using environment variables")
    except json.JSONDecodeError as e:
        logger.warning(f"Invalid config.json: {e}")
    
    # Override with environment variables if present
    if 'DISCORD_WEBHOOK_URL' in os.environ:
        config['webhook_url'] = os.environ['DISCORD_WEBHOOK_URL']
    
    if 'CALENDAR_TYPE' in os.environ:
        config['calendar_type'] = os.environ['CALENDAR_TYPE']
    
    # Set defaults
    config.setdefault('calendar_type', 'gregorian')
    
    return config

def main():
    """Main entry point."""
    try:
        # Load configuration
        config = load_config()
        
        # Validate required configuration
        if 'webhook_url' not in config:
            logger.error("Discord webhook URL not configured. Set DISCORD_WEBHOOK_URL environment variable or add to config.json")
            sys.exit(1)
        
        # Create and run bot
        bot = OrthodoxCalendarBot(
            webhook_url=config['webhook_url'],
            calendar_type=config['calendar_type']
        )
        
        success = bot.run()
        sys.exit(0 if success else 1)
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

