# PrecisionBot - AI-Powered Instagram Automation

<div align="center">
  <img src="docs/logo.png" alt="Precision Tech Insights" width="200"/>
  
  **From Code to Intelligence — We Deliver Precision**
  
  [![GitHub stars](https://img.shields.io/github/stars/harisXcyber/instagram-auto-bot?style=social)](https://github.com/harisXcyber/instagram-auto-bot)
  [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
  
  [🚀 Live Demo](https://harisxcyber.github.io/instagram-auto-bot/) | [📖 Documentation](https://harisxcyber.github.io/instagram-auto-bot/) | [💼 Company](https://precisiontechinsights.com)
</div>

---

## 🎯 What is PrecisionBot?

PrecisionBot is an open-source Instagram automation platform built by **Precision Tech Insights**. It uses GPT-4 Vision AI to analyze images and generate contextually relevant captions, then automatically posts to Instagram on your schedule.

**Save 182 hours annually. Post smarter, not harder.**

---

## ✨ Features

- 🧠 **GPT-4 Vision AI** - Intelligent image analysis and caption generation
- ⚡ **Smart Scheduling** - Daily recurring + one-time scheduled posts
- 🎯 **Web Dashboard** - Beautiful interface for monitoring and control
- 🔒 **Enterprise Security** - Password-protected with session persistence
- 🌐 **Cloud-Ready** - Docker-based, deploy anywhere
- 📊 **Analytics** - Track post history and performance
- 🚀 **One-Click Deploy** - Ready for Fly.io, AWS, or any cloud platform

---

## 🏢 About Precision Tech Insights

Founded in 2025, Precision Tech Insights transforms businesses through precision technology solutions. We specialize in:

- 💻 **Web Development** - MERN, Django, Laravel, React, Next.js
- 🔒 **Cybersecurity** - Penetration testing, security audits, ethical hacking
- 📊 **Data Science** - Analytics, visualization, automation, dashboards
- 🤖 **AI & Automation** - Chatbots, NLP, intelligent agents
- 🎨 **Content Creation** - Branding, video content, social media assets

**Our Mission:** From Code to Intelligence — We Deliver Precision

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Instagram account
- OpenAI API key

### Installation

```bash
# Clone the repository
git clone https://github.com/harisXcyber/instagram-auto-bot.git
cd instagram-auto-bot

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Add your images
# Place images in the images/ directory

# Run locally
python app.py
```

Visit `http://localhost:8080` and enter your dashboard password.

---

## ☁️ Deploy to Fly.io (Free)

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Deploy
flyctl launch
flyctl secrets set INSTAGRAM_USERNAME=your_username
flyctl secrets set INSTAGRAM_PASSWORD=your_password
flyctl secrets set OPENAI_API_KEY=your_key
flyctl secrets set DASHBOARD_PASSWORD=your_dashboard_password
flyctl deploy
```

---

## 💰 Pricing

### Open Source (FREE)
- Full source code access
- AI-generated captions
- Flexible scheduling
- Web dashboard
- Self-hosted deployment
- Community support

### PrecisionBot Pro (Coming Soon - $29/mo)
- Multi-account management
- Advanced AI agents
- Engagement analytics
- Content optimization
- Priority support
- Managed hosting

### Enterprise (Custom Pricing)
- Unlimited accounts
- Custom AI training
- White-label solution
- Dedicated support
- SLA guarantee
- On-premise deployment

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Scheduling:** APScheduler
- **Instagram API:** instagrapi
- **AI:** OpenAI GPT-4 Vision
- **Database:** SQLite
- **Deployment:** Docker + Fly.io

---

## 📖 Documentation

Full documentation available at: [https://harisxcyber.github.io/instagram-auto-bot/](https://harisxcyber.github.io/instagram-auto-bot/)

---

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request.

---

## 📧 Contact

**Precision Tech Insights**

- 🌐 Website: [precisiontechinsights.com](https://precisiontechinsights.com)
- 📧 Email: contact@precisiontechinsights.com
- 📱 Phone: +92 348 1383350
- 💼 LinkedIn: [Precision Tech Insights](https://www.linkedin.com/company/precision-tech-insights)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🌟 Star Us!

If PrecisionBot saves you time, please star the repo and share it with others!

---

<div align="center">
  <strong>Built with ☕ and AI by Precision Tech Insights</strong>
  
  From Code to Intelligence — We Deliver Precision
</div>
