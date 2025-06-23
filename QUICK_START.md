# Orthodox Calendar Discord Integration - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### What You'll Get
- **Automated daily posts** of Orthodox calendar information to your Discord #new-calendar channel
- **Rich formatted messages** with feast days, saints, fasting info, and scripture readings
- **Multiple deployment options** from simple cron jobs to cloud solutions
- **Fully tested and ready-to-use** solution

### Prerequisites
- Discord server with webhook creation permissions
- One of: VPS/server, GitHub account, or Docker environment

## Option 1: GitHub Actions (Easiest - No Server Required)

**Perfect for beginners - completely free and automatic**

1. **Create Discord Webhook**
   - Go to your Discord server → Settings → Integrations → Webhooks
   - Create webhook for #new-calendar channel
   - Copy the webhook URL

2. **Set Up GitHub Repository**
   - Fork or create new repository with the provided files
   - Go to Settings → Secrets and variables → Actions
   - Add secret: `DISCORD_WEBHOOK_URL` = your webhook URL

3. **Done!** 
   - The bot will post daily at 8 AM UTC automatically
   - Check the Actions tab to monitor execution

## Option 2: Simple Server Setup (Most Control)

**Best for users with VPS or dedicated server**

1. **Download and Configure**
   ```bash
   # Download files to your server
   wget [download-link] -O orthodox-calendar-bot.tar.gz
   tar -xzf orthodox-calendar-bot.tar.gz
   cd orthodox-calendar-discord-integration
   
   # Configure
   cp config.json.template config.json
   nano config.json  # Add your webhook URL
   ```

2. **Deploy**
   ```bash
   chmod +x deploy_cron.sh
   ./deploy_cron.sh
   ```

3. **Schedule**
   ```bash
   crontab -e
   # Add: 0 8 * * * /path/to/your/bot/run_bot.sh
   ```

## Option 3: Docker (Containerized)

**Best for Docker users or cloud platforms**

1. **Set Environment**
   ```bash
   export DISCORD_WEBHOOK_URL="your_webhook_url_here"
   ```

2. **Run**
   ```bash
   docker-compose up -d
   ```

## What the Bot Posts

### Sample Message Format:
```
📅 June 22, 2025 - 2nd Sunday after Pentecost
🍷 Apostles Fast — Fish, Wine and Oil are Allowed

🎉 Feasts
All Saints of America, All Saints of Russia

✨ Commemorations  
Hieromartyr Eusebius, Bishop of Samosata • St Alban, First Martyr of Great Britain

📖 Scripture Readings
Isaiah 43.9-14 • Wisdom of Solomon 3.1-9 • Mark 16.1-8 • Romans 2.10-16 • ...

Orthodox Calendar • orthocal.info
```

## Customization Options

- **Timing**: Change schedule in cron job or GitHub Actions workflow
- **Calendar Type**: Switch between Gregorian and Julian in config
- **Content**: Modify which fields to include/exclude
- **Multiple Channels**: Create additional webhooks for other channels

## Support Files Included

- `README.md` - Complete documentation
- `deployment_guide.md` - Detailed deployment instructions  
- `test_bot.py` - Test script to verify setup
- `orthodox_calendar_bot.py` - Main application
- Multiple deployment configurations (Docker, GitHub Actions, etc.)

## Troubleshooting

### Bot Not Posting?
1. Check webhook URL is correct
2. Verify Discord channel permissions
3. Run test: `python3 test_bot.py`
4. Check logs: `tail -f orthodox_calendar_bot.log`

### Need Help?
- Review the comprehensive `README.md`
- Check `deployment_guide.md` for detailed instructions
- Verify your setup with the included test script

## Next Steps

1. **Choose your deployment method** based on your technical setup
2. **Follow the specific guide** for your chosen method
3. **Test the setup** using the provided test script
4. **Monitor the first few days** to ensure everything works correctly
5. **Customize as needed** for your community's preferences

---

**Ready to bring daily Orthodox calendar information to your Discord community!** ☦️

Choose your deployment method above and follow the detailed guides in the included documentation.

