#!/usr/bin/env python3
"""
Test script for Orthodox Calendar Bot
Tests API connectivity and data formatting without posting to Discord
"""

import json
import sys
import os

# Add the current directory to Python path to import the bot
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orthodox_calendar_bot import OrthodoxCalendarBot

def test_api_connection():
    """Test API connection and data fetching."""
    print("Testing API connection...")
    
    # Create bot instance with dummy webhook URL for testing
    bot = OrthodoxCalendarBot("https://example.com/webhook", "gregorian")
    
    # Test data fetching
    data = bot.fetch_calendar_data()
    if data:
        print("✓ API connection successful")
        print(f"✓ Received data for: {data.get('year', 'N/A')}-{data.get('month', 'N/A')}-{data.get('day', 'N/A')}")
        return data
    else:
        print("✗ API connection failed")
        return None

def test_message_formatting(data):
    """Test message formatting functionality."""
    print("\nTesting message formatting...")
    
    bot = OrthodoxCalendarBot("https://example.com/webhook", "gregorian")
    
    try:
        # Test individual formatting functions
        title = bot.format_date_title(data)
        print(f"✓ Title: {title}")
        
        fast_info = bot.format_fast_info(data)
        print(f"✓ Fast info: {fast_info}")
        
        feasts = bot.format_feasts(data)
        if feasts:
            print(f"✓ Feasts: {feasts}")
        else:
            print("✓ No feasts today")
        
        saints = bot.format_saints(data)
        if saints:
            print(f"✓ Saints: {saints[:100]}..." if len(saints) > 100 else f"✓ Saints: {saints}")
        else:
            print("✓ No saints commemorated today")
        
        readings = bot.format_readings(data)
        if readings:
            print(f"✓ Readings: {readings[:100]}..." if len(readings) > 100 else f"✓ Readings: {readings}")
        else:
            print("✓ No readings available")
        
        # Test full embed creation
        embed = bot.create_discord_embed(data)
        print("✓ Discord embed created successfully")
        
        return embed
        
    except Exception as e:
        print(f"✗ Message formatting failed: {e}")
        return None

def display_embed_preview(embed):
    """Display a preview of the Discord embed."""
    print("\n" + "="*60)
    print("DISCORD MESSAGE PREVIEW")
    print("="*60)
    
    print(f"Title: {embed.get('title', 'N/A')}")
    print(f"Description: {embed.get('description', 'N/A')}")
    print(f"Color: #{embed.get('color', 0):06x}")
    
    fields = embed.get('fields', [])
    if fields:
        print("\nFields:")
        for field in fields:
            print(f"  {field.get('name', 'N/A')}: {field.get('value', 'N/A')}")
    
    footer = embed.get('footer', {})
    if footer:
        print(f"\nFooter: {footer.get('text', 'N/A')}")
    
    print("="*60)

def test_json_calendar_type():
    """Test Julian calendar type."""
    print("\nTesting Julian calendar...")
    
    bot = OrthodoxCalendarBot("https://example.com/webhook", "julian")
    data = bot.fetch_calendar_data()
    
    if data:
        print("✓ Julian calendar API connection successful")
        title = bot.format_date_title(data)
        print(f"✓ Julian date: {title}")
        return True
    else:
        print("✗ Julian calendar API connection failed")
        return False

def main():
    """Main test function."""
    print("Orthodox Calendar Bot - Test Suite")
    print("="*50)
    
    # Test Gregorian calendar
    data = test_api_connection()
    if not data:
        print("Cannot proceed with tests - API connection failed")
        return False
    
    # Test message formatting
    embed = test_message_formatting(data)
    if not embed:
        print("Message formatting tests failed")
        return False
    
    # Display preview
    display_embed_preview(embed)
    
    # Test Julian calendar
    julian_success = test_json_calendar_type()
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    print("✓ API Connection: PASSED")
    print("✓ Message Formatting: PASSED")
    print("✓ Embed Creation: PASSED")
    print(f"{'✓' if julian_success else '✗'} Julian Calendar: {'PASSED' if julian_success else 'FAILED'}")
    
    print("\nAll core functionality tests completed successfully!")
    print("The bot is ready for deployment.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

