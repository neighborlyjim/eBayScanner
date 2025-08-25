#!/usr/bin/env python3
"""
Simple test script to demonstrate MCP integration with eBay Scanner
This script tests the infrastructure and application workflow
"""

import subprocess
import sys
import os
import json

def test_terraform_container():
    """Test if Terraform MCP container is running"""
    try:
        result = subprocess.run(['docker', 'ps', '--filter', 'name=upbeat_ride', '--format', 'table {{.Names}}\t{{.Status}}'], 
                              capture_output=True, text=True, shell=True)
        if 'upbeat_ride' in result.stdout and 'Up' in result.stdout:
            print("✅ Terraform MCP container is running")
            return True
        else:
            print("❌ Terraform MCP container is not running")
            return False
    except Exception as e:
        print(f"❌ Error checking Terraform container: {e}")
        return False

def test_uvx_servers():
    """Test if uvx MCP servers are accessible"""
    servers = ['mcp-server-git', 'mcp-server-filesystem', 'mcp-server-fetch']
    results = {}
    
    for server in servers:
        try:
            result = subprocess.run(['uvx', server, '--help'], 
                                  capture_output=True, text=True, shell=True,
                                  timeout=30)
            if result.returncode == 0:
                print(f"✅ {server} is accessible")
                results[server] = True
            else:
                print(f"❌ {server} failed with return code {result.returncode}")
                results[server] = False
        except subprocess.TimeoutExpired:
            print(f"❌ {server} timed out")
            results[server] = False
        except Exception as e:
            print(f"❌ Error testing {server}: {e}")
            results[server] = False
    
    return results

def test_terraform_validation():
    """Test Terraform configuration validation"""
    try:
        os.chdir('terraform')
        result = subprocess.run(['terraform', 'validate'], 
                              capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            print("✅ Terraform configuration is valid")
            return True
        else:
            print(f"❌ Terraform validation failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error validating Terraform: {e}")
        return False
    finally:
        os.chdir('..')

def test_mcp_config():
    """Test MCP configuration file"""
    try:
        with open('.vscode/mcp.json', 'r') as f:
            config = json.load(f)
        
        servers = config.get('mcpServers', {})
        print(f"✅ MCP configuration loaded with {len(servers)} servers:")
        for name in servers.keys():
            print(f"   - {name}")
        return True
    except Exception as e:
        print(f"❌ Error reading MCP configuration: {e}")
        return False

def test_app_structure():
    """Test application structure"""
    required_files = [
        'app.py',
        'requirements.txt',
        'docker-compose.yml',
        'Dockerfile',
        'frontend/package.json',
        'terraform/main.tf'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    else:
        print("✅ All required application files present")
        return True

def main():
    print("🔍 Testing eBay Scanner MCP Integration")
    print("=" * 50)
    
    tests = [
        ("App Structure", test_app_structure),
        ("MCP Configuration", test_mcp_config),
        ("Terraform Container", test_terraform_container),
        ("UVX MCP Servers", test_uvx_servers),
        ("Terraform Validation", test_terraform_validation)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        results[test_name] = test_func()
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}: {test_name}")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All systems ready for AI-powered DevOps workflow!")
        print("\n💡 Next steps:")
        print("   1. Deploy infrastructure: terraform apply")
        print("   2. Build and push Docker images")
        print("   3. Test browser automation with MCP")
    else:
        print("⚠️  Some tests failed. Check the issues above.")

if __name__ == "__main__":
    main()
