# 🌐 ngrok Setup Guide - Share Your Site with Friends

## Quick Setup (2 minutes)

### Step 1: Create Free ngrok Account
1. Go to **https://dashboard.ngrok.com/signup**
2. Sign up with email (or GitHub/Google)
3. Verify your email

### Step 2: Get Your Auth Token
1. Visit **https://dashboard.ngrok.com/get-started/your-authtoken**
2. Copy your auth token (looks like: `your_auth_token_here`)

### Step 3: Run the Setup Script
1. Create a file named `.env.ngrok` in the project root
2. Add this line:
   ```
   NGROK_AUTH_TOKEN=your_auth_token_here
   ```
3. Replace `your_auth_token_here` with your actual token from Step 2

### Step 4: Start the Tunnel
Run this command in your terminal:
```bash
cd c:\rencedav_mart
python start_ngrok.py
```

### Step 5: Share the Public URL
The script will display something like:
```
✅ Tunnel created successfully!

🌐 PUBLIC URL: https://abc123def456.ngrok.io

📋 Share this URL with your friends to test: https://abc123def456.ngrok.io
```

Share that URL with your friends! ✨

---

## Manual ngrok Setup (Alternative Method)

If you prefer using ngrok directly without Python:

### 1. Download ngrok
- Visit: https://ngrok.com/download
- Download for Windows
- Extract to a folder

### 2. Configure Auth Token
```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

### 3. Start Tunnel
```bash
ngrok http 8000
```

This will give you a public URL like: `https://abc123def456.ngrok.io`

---

## Troubleshooting

**Q: "Authentication failed" error?**
- Make sure your auth token is correct (copy from https://dashboard.ngrok.com/get-started/your-authtoken)
- Recreate the `.env.ngrok` file with the correct token

**Q: Can't access the public URL?**
- Make sure Django server is still running on port 8000
- Check firewall settings allow port 8000

**Q: URL stopped working?**
- ngrok free tier URLs expire after disconnection
- Just restart the tunnel for a new URL

---

## Security Notes

🔒 Your ngrok URL is public and anyone with the link can access your site
- Don't share sensitive data on test site
- Share URL only with trusted friends
- URLs expire when you disconnect ngrok

---

## What to Share with Friends

```
Hey! I've set up a test version of my e-commerce site on ngrok:

🌐 https://abc123def456.ngrok.io

You can:
- Browse products
- Add items to cart
- Go through checkout
- Test the full ordering flow

Feel free to test and give me feedback!
```

---

## Keeping It Running

- Keep this terminal window open while friends are testing
- The tunnel stays active as long as ngrok is running
- To stop: Press `CTRL+C` in the ngrok terminal

Need help? Visit https://ngrok.com/docs for more info!
