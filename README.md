# Instagram Auto-Posting Bot

Automated Instagram bot with AI-generated captions, scheduling, and web dashboard.

## Features

- 🤖 Automated daily posts with AI-generated captions
- 🎨 OpenAI Vision API for context-aware content
- 📅 Flexible scheduling system (recurring & one-time posts)
- 🌐 Web dashboard for monitoring and control
- 🔒 Password-protected interface
- 📊 Post history tracking
- 🚀 One-click manual posting

## Tech Stack

- **Backend:** Flask + APScheduler
- **Instagram:** instagrapi
- **AI:** OpenAI GPT-4 Vision
- **Database:** SQLite
- **Deployment:** Fly.io (Docker)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

### 3. Add Images

Place your images in the `images/` directory.

### 4. Run Locally

```bash
python app.py
```

Visit `http://localhost:8080`

## Deployment (Fly.io)

### 1. Install Fly CLI

```bash
curl -L https://fly.io/install.sh | sh
```

### 2. Login

```bash
flyctl auth login
```

### 3. Deploy

```bash
flyctl launch
flyctl secrets set INSTAGRAM_USERNAME=your_username
flyctl secrets set INSTAGRAM_PASSWORD=your_password
flyctl secrets set OPENAI_API_KEY=your_key
flyctl secrets set DASHBOARD_PASSWORD=your_dashboard_password
flyctl deploy
```

## Dashboard Features

- **Next Post:** Shows countdown to next scheduled post
- **Manual Trigger:** Post immediately with one click
- **Schedules Tab:** View/add/remove scheduled posts
- **History Tab:** See recent posts and their status

## Security

- Password-protected dashboard
- Session-based authentication
- Instagram session persistence
- Environment variables for sensitive data

## License

MIT
