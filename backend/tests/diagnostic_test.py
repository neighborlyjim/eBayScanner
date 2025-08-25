#!/usr/bin/env python3
"""
eBay API Diagnostic Test
Helps diagnose eBay API configuration issues
"""

import config
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

def test_different_configs():
    """Test different API configurations to identify the issue"""
    
    print("🔍 eBay API Diagnostic Test")
    print("=" * 50)
    
    configs_to_test = [
        {
            "name": "Production Finding API",
            "config": {
                "appid": config.APP_ID,
                "siteid": "EBAY-US",
                "api_version": "1.13.0",
                "config_file": None
            }
        },
        {
            "name": "Sandbox Finding API", 
            "config": {
                "appid": config.APP_ID,
                "siteid": "EBAY-US", 
                "api_version": "1.13.0",
                "config_file": None,
                "domain": "svcs.sandbox.ebay.com"
            }
        }
    ]
    
    for test_config in configs_to_test:
        print(f"\n🧪 Testing: {test_config['name']}")
        print("-" * 30)
        
        try:
            api = Finding(**test_config['config'])
            
            # Try a simple API call
            response = api.execute("findItemsByKeywords", {
                "keywords": "test",
                "paginationInput": {"entriesPerPage": 1}
            })
            
            print(f"✅ Success with {test_config['name']}")
            return test_config
            
        except ConnectionError as e:
            print(f"❌ Failed: {e}")
            
            # Parse the error for more details
            error_str = str(e)
            if "Invalid Application" in error_str:
                print("   💡 App ID might not be valid for Finding API")
            elif "Authentication failed" in error_str:
                print("   💡 Authentication issue - check your App ID")
            elif "Access denied" in error_str:
                print("   💡 App doesn't have permission for Finding API")
                
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    return None

def show_troubleshooting():
    """Show troubleshooting steps"""
    print("\n🔧 Troubleshooting Steps:")
    print("=" * 50)
    print("1. 📋 Check your eBay Developer Account:")
    print("   - Go to: https://developer.ebay.com/my/keys")
    print("   - Verify your App ID is correct")
    print("   - Check if Finding API is enabled for your app")
    print()
    print("2. 🔑 App ID vs Client ID:")
    print("   - App ID (DevID): Used for Finding API")
    print("   - Client ID: Used for Browse/Buy APIs")
    print("   - Make sure you're using the right one!")
    print()
    print("3. 🌍 Environment:")
    print("   - Sandbox: For testing")
    print("   - Production: For live data")
    print("   - Your keys might be for different environments")
    print()
    print("4. 📱 Alternative: Try Browse API instead")
    print("   - Browse API uses OAuth (Client ID + Secret)")
    print("   - Might be what your app is configured for")

if __name__ == "__main__":
    working_config = test_different_configs()
    
    if working_config:
        print(f"\n🎉 Found working configuration: {working_config['name']}")
    else:
        print("\n❌ No working configurations found")
        show_troubleshooting()
        
        print("\n📧 Next Steps:")
        print("1. Double-check your App ID in eBay Developer Console")
        print("2. Verify Finding API is enabled for your application")
        print("3. Or consider switching to Browse API (uses OAuth)")
