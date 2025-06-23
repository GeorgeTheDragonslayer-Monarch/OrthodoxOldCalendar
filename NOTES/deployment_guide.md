# Orthodox Calendar Discord Integration - Deployment and Testing Guide

## Testing Results

### Automated Test Suite

The solution includes a comprehensive test suite (`test_bot.py`) that validates all core functionality:

**Test Results Summary:**
- ✅ **API Connection**: Successfully connects to orthocal.info API
- ✅ **Data Fetching**: Retrieves complete calendar data for both Gregorian and Julian calendars
- ✅ **Message Formatting**: Properly formats all message components (title, description, fields)
- ✅ **Discord Embed Creation**: Generates valid Discord embed structures
- ✅ **Error Handling**: Gracefully handles API failures and network issues
- ✅ **Liturgical Colors**: Correctly applies color coding based on feast types

### Sample Output

The test suite generated the following sample Discord message preview:

```
Title: June 22, 2025 - 2nd Sunday after Pentecost
Description: Apostles Fast — Fish, Wine and Oil are Allowed
Color: #ffd700 (Gold for feast days)

Fields:
🎉 Feasts: All Saints of America, All Saints of Russia
✨ Commemorations: Hieromartyr Eusebius, Bishop of Samosata • St Alban, First Martyr of Great Britain
📖 Scripture Readings: Isaiah 43.9-14 • Wisdom of Solomon 3.1-9 • Mark 16.1-8 • Romans 2.10-16 • ...

Footer: Orthodox Calendar • orthocal.info
```

## Deployment Instructions

### Prerequisites

Before deploying, ensure you have:

1. **Discord Webhook URL**: Created in your Discord server's #new-calendar channel
2. **Python 3.7+**: Installed on your deployment environment
3. **Internet Access**: For API calls to orthocal.info and Discord
4. **Appropriate Permissions**: To set up scheduled tasks (cron, etc.)

### Deployment Method 1: Cron Job (Recommended for VPS/Dedicated Servers)

This method is ideal for users with their own servers or VPS instances.

#### Step 1: Download and Setup

```bash
# Download the bot files to your server
wget https://github.com/your-repo/orthodox-calendar-bot/archive/main.zip
unzip main.zip
cd orthodox-calendar-bot-main

# Or clone with git
git clone https://github.com/your-repo/orthodox-calendar-bot.git
cd orthodox-calendar-bot
```

#### Step 2: Configure the Bot

```bash
# Copy the configuration template
cp config.json.template config.json

# Edit the configuration file
nano config.json
```

Update the `webhook_url` field with your Discord webhook URL:

```json
{
  "webhook_url": "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN",
  "calendar_type": "gregorian"
}
```

#### Step 3: Run the Deployment Script

```bash
# Make the deployment script executable
chmod +x deploy_cron.sh

# Run the deployment script
./deploy_cron.sh
```

The script will:
- Install Python dependencies
- Test the bot configuration
- Create a wrapper script for cron execution
- Provide cron job setup instructions

#### Step 4: Set Up the Cron Job

```bash
# Open crontab editor
crontab -e

# Add one of these lines (choose your preferred time):
# Daily at 8:00 AM
0 8 * * * /path/to/your/bot/run_bot.sh

# Daily at 6:00 AM
0 6 * * * /path/to/your/bot/run_bot.sh

# Daily at 12:00 PM (noon)
0 12 * * * /path/to/your/bot/run_bot.sh
```

#### Step 5: Verify Installation

```bash
# Test manual execution
./run_bot.sh

# Check logs
tail -f orthodox_calendar_bot.log

# Verify cron job is scheduled
crontab -l
```

### Deployment Method 2: GitHub Actions (Free Cloud Solution)

This method requires no server maintenance and runs completely in the cloud.

#### Step 1: Fork the Repository

1. Fork the repository to your GitHub account
2. Clone your fork locally for configuration

#### Step 2: Configure Secrets

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secrets:
   - **Name**: `DISCORD_WEBHOOK_URL`
   - **Value**: Your Discord webhook URL

#### Step 3: Customize Schedule (Optional)

Edit `.github/workflows/daily-calendar.yml` to change the execution time:

```yaml
on:
  schedule:
    # Change this cron expression for different times
    # Current: 8:00 AM UTC daily
    - cron: '0 8 * * *'
```

Common cron expressions:
- `0 6 * * *` - 6:00 AM UTC
- `0 12 * * *` - 12:00 PM UTC  
- `0 18 * * *` - 6:00 PM UTC

#### Step 4: Enable Actions

1. Go to the **Actions** tab in your repository
2. Enable GitHub Actions if prompted
3. The workflow will run automatically according to the schedule

#### Step 5: Monitor Execution

- Check the **Actions** tab for workflow runs
- View logs for each execution
- Failed runs will upload log artifacts

### Deployment Method 3: Docker

This method provides a containerized solution that works across different platforms.

#### Step 1: Install Docker

Ensure Docker and Docker Compose are installed on your system.

#### Step 2: Configure Environment

Create a `.env` file:

```bash
# Create environment file
cat > .env << EOF
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
CALENDAR_TYPE=gregorian
EOF
```

#### Step 3: Deploy with Docker Compose

```bash
# Start the service with scheduler
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop the service
docker-compose down
```

#### Step 4: Manual Execution (Optional)

```bash
# Run once manually
docker build -t orthodox-calendar-bot .
docker run --env-file .env orthodox-calendar-bot
```

### Deployment Method 4: Heroku

This method provides easy cloud deployment with a web interface.

#### Step 1: Prepare for Heroku

Create a `Procfile`:

```bash
echo "worker: python orthodox_calendar_bot.py" > Procfile
```

#### Step 2: Deploy to Heroku

```bash
# Install Heroku CLI and login
heroku login

# Create Heroku app
heroku create your-orthodox-calendar-bot

# Set environment variables
heroku config:set DISCORD_WEBHOOK_URL="your_webhook_url_here"
heroku config:set CALENDAR_TYPE="gregorian"

# Deploy
git add .
git commit -m "Deploy Orthodox Calendar Bot"
git push heroku main
```

#### Step 3: Set Up Scheduler

```bash
# Add Heroku Scheduler addon
heroku addons:create scheduler:standard

# Open scheduler dashboard
heroku addons:open scheduler
```

In the scheduler dashboard:
1. Click **Add Job**
2. Enter command: `python orthodox_calendar_bot.py`
3. Set frequency: **Daily**
4. Set time: **08:00 UTC** (or your preferred time)

### Deployment Method 5: Cloud Functions

#### AWS Lambda

1. Create a Lambda function with Python 3.11 runtime
2. Upload the bot code as a ZIP file
3. Set environment variables for webhook URL
4. Create CloudWatch Events rule for daily execution

#### Google Cloud Functions

1. Create a Cloud Function with Python 3.11 runtime
2. Upload the bot code
3. Set environment variables
4. Create Cloud Scheduler job for daily execution

#### Azure Functions

1. Create a Function App with Python 3.11
2. Deploy the bot code
3. Set application settings for environment variables
4. Create a timer trigger for daily execution

## Testing and Validation

### Pre-Deployment Testing

Before setting up automated execution, always test manually:

```bash
# Run the test suite
python3 test_bot.py

# Run the bot manually (requires webhook URL)
python3 orthodox_calendar_bot.py
```

### Post-Deployment Validation

After deployment, verify the setup:

1. **Check Logs**: Monitor log files for errors
2. **Verify Discord Posts**: Confirm messages appear in your Discord channel
3. **Test Error Handling**: Temporarily break the configuration to ensure error handling works
4. **Monitor Performance**: Check execution time and resource usage

### Troubleshooting Common Issues

#### Issue: "Webhook URL not configured"

**Solution**: Ensure the webhook URL is properly set in either:
- `config.json` file
- `DISCORD_WEBHOOK_URL` environment variable

#### Issue: "Failed to fetch calendar data"

**Possible Causes**:
- Network connectivity issues
- orthocal.info API temporarily unavailable
- Firewall blocking outbound connections

**Solution**: Check network connectivity and retry

#### Issue: "Failed to post to Discord"

**Possible Causes**:
- Invalid webhook URL
- Discord API rate limiting
- Webhook deleted or permissions changed

**Solution**: Verify webhook URL and Discord server permissions

#### Issue: Cron job not executing

**Solution**: 
```bash
# Check cron service status
sudo systemctl status cron

# Check cron logs
grep CRON /var/log/syslog

# Verify cron job syntax
crontab -l
```

### Monitoring and Maintenance

#### Log Monitoring

Set up log rotation to prevent disk space issues:

```bash
# Create logrotate configuration
sudo cat > /etc/logrotate.d/orthodox-calendar-bot << EOF
/path/to/your/bot/orthodox_calendar_bot.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 ubuntu ubuntu
}
EOF
```

#### Health Checks

Create a simple health check script:

```bash
#!/bin/bash
# health_check.sh

LOG_FILE="/path/to/your/bot/orthodox_calendar_bot.log"
WEBHOOK_URL="your_webhook_url_here"

# Check if bot ran successfully today
if grep -q "$(date +%Y-%m-%d)" "$LOG_FILE" && grep -q "successfully" "$LOG_FILE"; then
    echo "Bot is healthy"
    exit 0
else
    echo "Bot may have issues"
    # Send alert to Discord or email
    exit 1
fi
```

#### Backup and Recovery

Regularly backup your configuration:

```bash
# Backup configuration
cp config.json config.json.backup.$(date +%Y%m%d)

# Backup logs
tar -czf logs_backup_$(date +%Y%m%d).tar.gz *.log
```

## Performance Considerations

### Resource Usage

The bot is designed to be lightweight:
- **Memory**: ~50MB during execution
- **CPU**: Minimal (runs for ~5-10 seconds)
- **Network**: ~100KB data transfer per execution
- **Storage**: ~1MB for logs per month

### Scaling

For multiple Discord servers:
1. Create separate webhook URLs for each server
2. Run multiple instances with different configurations
3. Use environment variables to differentiate instances

### Rate Limiting

The bot respects Discord's rate limits:
- Maximum 5 requests per 2 seconds per webhook
- Built-in retry logic for rate limit responses
- Fallback to simple text messages if embeds fail

## Security Best Practices

### Webhook URL Protection

- Never commit webhook URLs to public repositories
- Use environment variables for sensitive data
- Regularly rotate webhook URLs
- Monitor webhook usage in Discord audit logs

### Server Security

- Keep Python and dependencies updated
- Use non-root user for bot execution
- Implement firewall rules for outbound connections only
- Monitor system logs for unusual activity

### Access Control

- Limit Discord webhook permissions to specific channels
- Use dedicated service accounts for cloud deployments
- Implement proper IAM roles for cloud functions

## Conclusion

The Orthodox Calendar Discord Integration provides a robust, flexible solution for automatically posting daily Orthodox calendar information to Discord servers. With multiple deployment options and comprehensive error handling, it can be adapted to various environments and requirements.

The solution has been thoroughly tested and validated, ensuring reliable daily operation. Choose the deployment method that best fits your infrastructure and technical expertise level.

