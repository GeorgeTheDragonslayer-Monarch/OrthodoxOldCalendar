# Orthodox Calendar Discord Integration

Automatically post daily Orthodox calendar information from [orthocal.info](https://orthocal.info/) to your Discord server.

## Features

- 📅 **Daily Calendar Posts**: Automatically fetches and posts daily Orthodox calendar information
- 🎨 **Rich Formatting**: Beautiful Discord embeds with liturgical colors
- ⛪ **Comprehensive Content**: Includes feast days, saint commemorations, fasting information, and scripture readings
- 🔧 **Multiple Deployment Options**: Cron jobs, GitHub Actions, Docker, cloud functions
- 🛡️ **Robust Error Handling**: Fallback mechanisms and detailed logging
- 🌍 **Calendar Support**: Both Gregorian and Julian calendar options

## Quick Start

### 1. Create Discord Webhook

1. Go to your Discord server settings
2. Navigate to **Integrations** → **Webhooks**
3. Click **Create Webhook**
4. Set the channel to `#new-calendar` (or your preferred channel)
5. Copy the webhook URL

### 2. Download and Configure

```bash
# Clone or download the files
git clone <repository-url>
cd orthodox-calendar-discord

# Copy and edit configuration
cp config.json.template config.json
nano config.json  # Add your webhook URL
```

### 3. Choose Deployment Method

#### Option A: Cron Job (Recommended for VPS)

```bash
# Run the setup script
chmod +x deploy_cron.sh
./deploy_cron.sh

# Add to crontab for daily 8 AM execution
crontab -e
# Add: 0 8 * * * /path/to/your/bot/run_bot.sh
```

#### Option B: GitHub Actions (Free Cloud)

1. Fork this repository
2. Go to repository **Settings** → **Secrets and variables** → **Actions**
3. Add secret: `DISCORD_WEBHOOK_URL` with your webhook URL
4. The workflow will run daily at 8 AM UTC

#### Option C: Docker

```bash
# Set environment variable
export DISCORD_WEBHOOK_URL="your_webhook_url_here"

# Run with Docker Compose (includes scheduler)
docker-compose up -d

# Or run once manually
docker build -t orthodox-calendar-bot .
docker run -e DISCORD_WEBHOOK_URL="$DISCORD_WEBHOOK_URL" orthodox-calendar-bot
```

## Configuration

### config.json

```json
{
  "webhook_url": "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN",
  "calendar_type": "gregorian",
  "bot_settings": {
    "username": "Orthodox Calendar",
    "avatar_url": "https://orthocal.info/favicon.ico"
  },
  "message_settings": {
    "include_readings": true,
    "max_saints": 5,
    "max_readings": 6,
    "use_liturgical_colors": true
  }
}
```

### Environment Variables

- `DISCORD_WEBHOOK_URL`: Discord webhook URL (required)
- `CALENDAR_TYPE`: Either "gregorian" or "julian" (default: "gregorian")

## Deployment Options

### 1. Cron Job Deployment

**Best for**: VPS, dedicated servers, Raspberry Pi

**Pros**: 
- Simple and reliable
- Low resource usage
- Full control over timing

**Setup**:
```bash
./deploy_cron.sh
crontab -e
# Add: 0 8 * * * /path/to/run_bot.sh
```

### 2. GitHub Actions

**Best for**: Free cloud solution, no server maintenance

**Pros**:
- Completely free
- No server required
- Automatic updates

**Setup**:
1. Fork repository
2. Add `DISCORD_WEBHOOK_URL` secret
3. Workflow runs automatically

### 3. Docker Deployment

**Best for**: Containerized environments, cloud platforms

**Pros**:
- Consistent environment
- Easy scaling
- Platform independent

**Setup**:
```bash
docker-compose up -d
```

### 4. Cloud Functions

**Best for**: Serverless deployment, pay-per-use

**Platforms**: AWS Lambda, Google Cloud Functions, Azure Functions

**Setup**: Deploy `orthodox_calendar_bot.py` with appropriate triggers

### 5. Heroku

**Best for**: Easy cloud deployment with web interface

**Setup**:
```bash
# Create Procfile
echo "worker: python orthodox_calendar_bot.py" > Procfile

# Deploy to Heroku
heroku create your-app-name
heroku config:set DISCORD_WEBHOOK_URL="your_webhook_url"
git push heroku main

# Add Heroku Scheduler
heroku addons:create scheduler:standard
heroku addons:open scheduler
# Add job: python orthodox_calendar_bot.py
```

## Message Format

The bot posts rich Discord embeds with:

- **Title**: Date and liturgical day (e.g., "June 22, 2025 - 2nd Sunday after Pentecost")
- **Description**: Fasting information
- **Fields**:
  - 🎉 **Feasts**: Major feast days
  - ✨ **Commemorations**: Saints and martyrs
  - 📖 **Scripture Readings**: Daily readings (abbreviated)
- **Colors**: Liturgical colors (gold for feasts, red for martyrs, etc.)
- **Footer**: Attribution to orthocal.info

## Customization

### Timing

Modify the schedule in your chosen deployment method:

- **Cron**: `0 8 * * *` (8 AM daily)
- **GitHub Actions**: Edit `.github/workflows/daily-calendar.yml`
- **Docker**: Modify `docker-compose.yml` scheduler

### Content

Edit `orthodox_calendar_bot.py` to customize:

- Message formatting
- Field selection
- Color schemes
- Content limits

### Multiple Channels

Create multiple webhook URLs and run separate instances for different channels.

## Troubleshooting

### Common Issues

1. **Webhook URL Invalid**
   - Verify the webhook URL is correct
   - Check Discord server permissions

2. **Bot Not Running**
   - Check logs: `tail -f orthodox_calendar_bot.log`
   - Verify cron job: `crontab -l`

3. **API Errors**
   - Check internet connectivity
   - Verify orthocal.info is accessible

4. **Permission Errors**
   - Ensure webhook has permission to post in channel
   - Check file permissions for scripts

### Logs

- **Local**: `orthodox_calendar_bot.log`
- **GitHub Actions**: Check workflow run logs
- **Docker**: `docker logs <container_name>`

### Testing

Run manually to test:
```bash
python3 orthodox_calendar_bot.py
```

## Requirements

- Python 3.7+
- `requests` library
- Internet connection
- Discord webhook URL

## Security Notes

- Never commit webhook URLs to public repositories
- Use environment variables for sensitive data
- Regularly rotate webhook URLs if compromised
- Monitor logs for unusual activity

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- **Issues**: Create GitHub issue
- **Orthodox Calendar Data**: Contact [orthocal.info](https://orthocal.info/)
- **Discord API**: Check [Discord Developer Documentation](https://discord.com/developers/docs)

## Acknowledgments

- [orthocal.info](https://orthocal.info/) for providing the Orthodox calendar API
- Discord for webhook functionality
- The Orthodox community for inspiration

---

*May this tool help bring daily Orthodox calendar information to your community! ☦️*

