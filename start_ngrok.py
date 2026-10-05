#!/usr/bin/env python
"""
Start ngrok tunnel to expose the Django development server
Usage: python start_ngrok.py [YOUR_NGROK_AUTH_TOKEN]
"""
import sys
import time
import os
from pyngrok import ngrok

def get_auth_token():
    """Get ngrok auth token from command line, environment, or prompt"""
    # Check command line argument
    if len(sys.argv) > 1:
        return sys.argv[1]
    
    # Check environment variable
    if "NGROK_AUTH_TOKEN" in os.environ:
        return os.environ["NGROK_AUTH_TOKEN"]
    
    # Prompt user
    print("\n" + "="*70)
    print("🔐 ngrok Requires Authentication (Free Account)")
    print("="*70)
    print("\n1. Sign up for FREE at: https://dashboard.ngrok.com/signup")
    print("2. Get your token at: https://dashboard.ngrok.com/get-started/your-authtoken")
    print("\n" + "-"*70 + "\n")
    token = input("Enter your ngrok auth token (or press Enter to skip): ").strip()
    return token if token else None

# Kill any existing tunnels first
try:
    ngrok.kill()
except:
    pass

# Get auth token
auth_token = get_auth_token()

if not auth_token:
    print("\n❌ ngrok auth token is required!")
    print("\n📖 For manual setup instructions, see: NGROK_SETUP.md")
    sys.exit(1)

# Configure ngrok with auth token
try:
    ngrok.set_auth_token(auth_token)
except Exception as e:
    print(f"❌ Failed to set auth token: {e}")
    sys.exit(1)

# Start HTTP tunnel on port 8000
print("🚀 Starting ngrok tunnel to expose http://127.0.0.1:8000")
print("-" * 70)

try:
    public_url = ngrok.connect(8000, "http")
    print(f"✅ Tunnel created successfully!")
    print(f"\n🌐 PUBLIC URL: {public_url}")
    print(f"\n📋 Share this URL with your friends to test: {public_url}")
    print(f"\n💡 The tunnel will stay active while this script is running.")
    print(f"Press CTRL+C to stop the tunnel.\n")
    print("-" * 70)
    
    # Keep the tunnel alive
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\n❌ Stopping ngrok tunnel...")
    ngrok.disconnect(public_url)
    ngrok.kill()
    print("✓ Tunnel closed.")
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Tip: ngrok may require authentication for longer-running tunnels.")
    print("   Sign up at https://dashboard.ngrok.com to get a free auth token.")
