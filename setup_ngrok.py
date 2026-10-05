#!/usr/bin/env python
"""
Simple ngrok setup that creates config and starts tunnel
"""
import subprocess
import os
import sys
import time

auth_token = sys.argv[1] if len(sys.argv) > 1 else None

if not auth_token:
    print("❌ Auth token required!")
    sys.exit(1)

print(f"🔧 Setting up ngrok with auth token...")

# Create ngrok config directory
ngrok_config_dir = os.path.expanduser("~/.ngrok2")
os.makedirs(ngrok_config_dir, exist_ok=True)

# Write ngrok config
config_file = os.path.join(ngrok_config_dir, "ngrok.yml")
config_content = f"""version: "2"
authtoken: {auth_token}
"""

try:
    with open(config_file, 'w') as f:
        f.write(config_content)
    print(f"✅ Config written to {config_file}")
except Exception as e:
    print(f"❌ Failed to write config: {e}")
    sys.exit(1)

# Try to download ngrok if not present
print("🚀 Starting ngrok tunnel...")
try:
    from pyngrok import ngrok as pyngrok_ngrok
    pyngrok_ngrok.kill()
    
    # Create tunnel
    public_url = pyngrok_ngrok.connect(8000, "http", pyngrok=None)
    
    print("\n" + "="*70)
    print("✅ TUNNEL CREATED SUCCESSFULLY!")
    print("="*70)
    print(f"\n🌐 PUBLIC URL: {public_url}")
    print(f"\n📋 Share this link with your friends:")
    print(f"   {public_url}")
    print(f"\n💡 The tunnel will stay active while this script runs.")
    print(f"Press CTRL+C to stop the tunnel.\n")
    print("="*70 + "\n")
    
    # Keep tunnel alive
    while True:
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\n\n✓ Stopping ngrok tunnel...")
    try:
        pyngrok_ngrok.kill()
    except:
        pass
    print("Tunnel closed.")
except Exception as e:
    print(f"\n❌ Error: {e}")
    print(f"\n💡 Try using ngrok CLI directly:")
    print(f"   ngrok config add-authtoken {auth_token}")
    print(f"   ngrok http 8000")
