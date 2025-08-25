#!/usr/bin/env python3
"""
eBay API Connection Test
Tests the eBay Finding API connection using your configured credentials.
"""

import sys
import config
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

def test_api_connection():
    """Test the eBay Finding API connection"""
    print("🔍 Testing eBay API Connection...")
    print(f"📋 Using App ID: {config.APP_ID}")
    print(f"📋 Using Client ID: {config.CLIENT_ID}")
    print(f"📋 Marketplace: {config.MARKETPLACE_ID}")
    print("-" * 50)
    
    try:
        # Initialize the Finding API connection (using sandbox)
        api = Finding(
            appid=config.APP_ID, 
            siteid="EBAY-US", 
            api_version="1.13.0",
            config_file=None,  # Disable YAML config file
            domain="svcs.sandbox.ebay.com"  # Use sandbox environment for SBX keys
        )
        
        # Test with a simple search
        print("🔍 Testing Finding API with a simple search...")
        response = api.execute("findItemsByKeywords", {
            "keywords": "iPhone",
            "paginationInput": {
                "entriesPerPage": 3
            }
        })
        
        if hasattr(response.reply, 'searchResult'):
            search_result = response.reply.searchResult
            print(f"✅ API Connection Successful!")
            print(f"📊 Search result count: {getattr(search_result, '_count', 0)}")
            
            if hasattr(search_result, 'item'):
                items = search_result.item
                print(f"� Found {len(items)} items")
                
                # Show first item as example
                if items:
                    first_item = items[0]
                    print(f"\n📱 Sample item:")
                    print(f"   Title: {first_item.title}")
                    print(f"   Price: ${first_item.sellingStatus.currentPrice.value}")
                    print(f"   Condition: {getattr(first_item, 'condition', {}).get('conditionDisplayName', 'N/A')}")
                    print(f"   Time Left: {first_item.sellingStatus.timeLeft}")
            else:
                print("📦 No items returned (normal for sandbox environment)")
                
            print("\n🎉 eBay API connection test PASSED!")
            return True
        else:
            print("❌ Invalid response format")
            return False
            
    except ConnectionError as e:
        print(f"❌ Connection Error: {e}")
        if "Invalid App ID" in str(e):
            print("💡 Check your EBAY_APP_ID in the .env file")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
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
