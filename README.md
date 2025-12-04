# Kung Fu Panda Instagram Bot

Automated Instagram posting with AI-generated captions and web dashboard.

## Features
- 🤖 Automated daily posts at 5 AM
- 🎨 AI-generated captions using OpenAI Vision API
- 📊 Web dashboard to monitor and trigger posts
- 🖼️ 769 Kung Fu Panda images included
- 📝 Post history tracking

## Deploy to Fly.io (Free)

### 1. Install Fly CLI
```bash
curl -L https://fly.io/install.sh | sh
```

### 2. Login to Fly.io
```bash
flyctl auth login
```

### 3. Create app and deploy
```bash
cd /home/haris/kungfupanda-web
flyctl launch --no-deploy
```

### 4. Set secrets
```bash
flyctl secrets set INSTAGRAM_USERNAME=kungfu.painda
flyctl secrets set INSTAGRAM_PASSWORD="htybrertf:;:45635879c"
flyctl secrets set OPENAI_API_KEY=your_openai_key
```

### 5. Create volume for persistent storage
```bash
flyctl volumes create kungfupanda_data --size 1
```

### 6. Deploy
```bash
flyctl deploy
```

### 7. Open dashboard
```bash
flyctl open
```

## Local Testing
```bash
python app.py
# Visit http://localhost:8080
```

## Dashboard Features
- **Next Post**: Shows when next scheduled post will happen
- **Last Post**: Timestamp of most recent post
- **Post Now**: Manual trigger button
- **History**: Last 10 posts with status

## Environment Variables
- `INSTAGRAM_USERNAME`: Instagram account username
- `INSTAGRAM_PASSWORD`: Instagram account password
- `OPENAI_API_KEY`: OpenAI API key (optional, uses default captions if not set)
