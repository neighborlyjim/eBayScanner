#!/usr/bin/env python3
"""
eBay API Connection Test
Tests the eBay Finding API connection using centralized API helper.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import config
from ebay_api import ebay_api

def test_api_connection():
    """Test the eBay Finding API connection using centralized helper"""
    print("🔍 Testing eBay API Connection...")
    print(f"📋 Using App ID: {config.APP_ID}")
    print(f"📋 Using Client ID: {config.CLIENT_ID}")
    print(f"📋 Marketplace: {config.MARKETPLACE_ID}")
    print("-" * 50)
    
    try:
        # Test with a simple search using centralized API
        print("🔍 Testing Finding API with a simple search...")
        
        # Use the centralized API helper
        response = ebay_api.find_items_by_keywords("iPhone", pagination={"entriesPerPage": 3})
        
        # Extract items using the helper method
        items = ebay_api.extract_items_from_response(response)
        
        print(f"✅ API Connection Successful!")
        print(f"📊 Found {len(items)} items")
        
        # Show first item as example
        if items:
            first_item = items[0]
            print(f"\n📱 Sample item:")
            print(f"   Title: {first_item.get('title', 'N/A')}")
            if 'sellingStatus' in first_item and 'currentPrice' in first_item['sellingStatus']:
                price = first_item['sellingStatus']['currentPrice']
                print(f"   Price: ${price.get('value', 'N/A')}")
            else:
                print(f"   Price: N/A")
            print(f"   Time Left: {first_item.get('sellingStatus', {}).get('timeLeft', 'N/A')}")
        else:
            print("📦 No items returned (normal for sandbox environment)")
            
        print("\n🎉 eBay API connection test PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ API Error: {e}")
        if "Invalid App ID" in str(e):
            print("💡 Check your EBAY_APP_ID in the .env file")
        return False

def test_config():
    """Test if configuration is loaded correctly"""
    print("🔧 Testing Configuration...")
    
    issues = []
    if config.APP_ID == "your_app_id_here":
        issues.append("APP_ID not configured")
    if config.CLIENT_ID == "your_client_id_here":
        issues.append("CLIENT_ID not configured") 
    if config.CLIENT_SECRET == "your_client_secret_here":
        issues.append("CLIENT_SECRET not configured")
    
    if issues:
        print("❌ Configuration issues found:")
        for issue in issues:
            print(f"   - {issue}")
        print("\n💡 Make sure your .env file has the correct values")
        return False
    else:
        print("✅ Configuration looks good!")
        return True

if __name__ == "__main__":
    print("🚀 eBay Scanner API Connection Test")
    print("=" * 50)
    
    # Test configuration first
    if not test_config():
        sys.exit(1)
    
    print()
    
    # Test API connection
    if test_api_connection():
        print("\n🎉 All tests passed! Your eBay API is ready to use.")
        sys.exit(0)
    else:
        print("\n❌ Tests failed. Please check your configuration and try again.")
        sys.exit(1)
