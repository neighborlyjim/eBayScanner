#!/usr/bin/env python3
"""
eBay API Diagnostic Test
Helps diagnose eBay API configuration issues using centralized API helper
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import config
from ebay_api import ebay_api

def test_api_endpoints():
    """Test different API endpoints to identify working configuration"""
    
    print("🔍 eBay API Diagnostic Test")
    print("=" * 50)
    
    tests = [
        {
            "name": "Find Items by Keywords",
            "test_func": lambda: ebay_api.find_items_by_keywords("test", pagination={"entriesPerPage": 1})
        },
        {
            "name": "Find Items Advanced",
            "test_func": lambda: ebay_api.find_items_advanced({"keywords": "test"}, pagination={"entriesPerPage": 1})
        },
        {
            "name": "Find Completed Items",
            "test_func": lambda: ebay_api.find_completed_items("test", pagination={"entriesPerPage": 1})
        }
    ]
    
    working_tests = []
    
    for test in tests:
        print(f"\n🧪 Testing: {test['name']}")
        print("-" * 30)
        
        try:
            response = test['test_func']()
            items = ebay_api.extract_items_from_response(response)
            
            print(f"✅ Success with {test['name']}")
            print(f"   Found {len(items)} items")
            working_tests.append(test['name'])
            
        except Exception as e:
            print(f"❌ Failed: {e}")
            
            # Parse the error for more details
            error_str = str(e)
            if "Invalid Application" in error_str:
                print("   💡 App ID might not be valid for this API")
            elif "Authentication failed" in error_str:
                print("   💡 Authentication issue - check your App ID")
            elif "Access denied" in error_str:
                print("   💡 App doesn't have permission for this API")
    
    return working_tests

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

def test_configuration():
    """Test centralized configuration"""
    print("🔧 Testing Centralized Configuration...")
    print("-" * 40)
    
    try:
        # Test getting eBay connection
        connection = ebay_api.get_connection()
        print("✅ eBay connection created successfully")
        
        # Test configuration access
        print(f"📋 App ID configured: {bool(config.APP_ID)}")
        print(f"📋 Client ID configured: {bool(config.CLIENT_ID)}")
        print(f"📋 Environment: {'Sandbox' if 'sandbox' in str(ebay_api.domain) else 'Production'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 eBay Scanner API Diagnostic")
    print("=" * 50)
    
    # Test configuration first
    if not test_configuration():
        print("\n❌ Configuration test failed")
        show_troubleshooting()
        sys.exit(1)
    
    print()
    
    # Test API endpoints
    working_tests = test_api_endpoints()
    
    if working_tests:
        print(f"\n🎉 Found {len(working_tests)} working API endpoints:")
        for test in working_tests:
            print(f"   ✅ {test}")
    else:
        print("\n❌ No working API endpoints found")
        show_troubleshooting()
        
        print("\n📧 Next Steps:")
        print("1. Double-check your App ID in eBay Developer Console")
        print("2. Verify Finding API is enabled for your application")
        print("3. Or consider switching to Browse API (uses OAuth)")
