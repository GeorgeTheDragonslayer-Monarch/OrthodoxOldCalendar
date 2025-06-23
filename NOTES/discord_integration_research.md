# Discord Integration Methods Research

## 1. Discord Webhooks (Recommended)

### Overview
- **Low-effort** way to post messages to Discord channels
- **No bot user or authentication** required
- Simple HTTP POST requests to webhook URL

### Webhook Creation
1. Go to Discord server settings → Webhooks
2. Create webhook for target channel (#new-calendar)
3. Copy webhook URL (format: `https://discord.com/api/webhooks/{webhook.id}/{webhook.token}`)

### Execute Webhook API
- **Method**: POST
- **URL**: `/webhooks/{webhook.id}/{webhook.token}`
- **Content-Type**: application/json

### JSON Parameters
- `content` (string): Message text (up to 2000 characters)
- `username` (string): Override default webhook username
- `avatar_url` (string): Override default webhook avatar
- `embeds` (array): Rich embed objects for formatted content
- `tts` (boolean): Text-to-speech message
- `allowed_mentions`: Control mention behavior

### Example Request
```json
{
  "content": "Daily Orthodox Calendar Update",
  "username": "Orthodox Calendar",
  "embeds": [
    {
      "title": "June 22, 2025 - 2nd Sunday after Pentecost",
      "description": "Apostles Fast — Fish, Wine and Oil are Allowed",
      "color": 5814783,
      "fields": [
        {
          "name": "Feasts",
          "value": "All Saints of America, All Saints of Russia"
        },
        {
          "name": "Commemorations", 
          "value": "Hieromartyr Eusebius, Bishop of Samosata • St Alban, First Martyr of Great Britain"
        }
      ]
    }
  ]
}
```

## 2. Discord Bots with Scheduling

### Advantages
- More control over message formatting
- Can handle complex interactions
- Built-in scheduling capabilities

### Disadvantages
- Requires bot creation and permissions
- More complex setup and maintenance
- Need to host bot application

### Popular Libraries
- **Python**: discord.py with scheduling libraries
- **JavaScript**: discord.js with node-cron
- **Hosted Solutions**: Various Discord bot hosting services

## 3. RSS to Discord Integration Services

### Third-Party Services
1. **RSS.app Discord Bot**
   - Automated RSS feed monitoring
   - Custom message formatting
   - Multiple feed support

2. **MonitoRSS**
   - Free and open-source
   - Customizable message templates
   - Advanced filtering options

3. **Zapier/IFTTT Integration**
   - No-code automation
   - RSS feed triggers
   - Discord webhook actions

4. **Readybot**
   - Supports RSS, YouTube, Reddit, Twitter
   - Advanced filtering and formatting

### RSS Feed Approach
- **Orthocal RSS**: https://orthocal.info/api/feed/gregorian/
- **Pros**: No custom coding required, automatic updates
- **Cons**: Less control over formatting, potential delays

## 4. Automation Platforms

### Zapier
- RSS feed trigger → Discord webhook action
- Visual workflow builder
- Reliable but paid service

### Make (formerly Integromat)
- Similar to Zapier with more customization
- Free tier available

### IFTTT
- Simple if-this-then-that automation
- Limited customization options

## Recommended Implementation Strategy

### Option 1: Custom Webhook Solution (Best Control)
1. Create Discord webhook for #new-calendar channel
2. Build Python/Node.js script to:
   - Fetch daily data from orthocal.info API
   - Format as Discord embed message
   - POST to webhook URL
3. Schedule with cron job or cloud function

### Option 2: RSS Integration Service (Easiest Setup)
1. Use MonitoRSS or RSS.app bot
2. Configure with orthocal.info RSS feed
3. Customize message template
4. Set posting schedule

### Option 3: Hybrid Approach
1. Use orthocal.info RSS feed for reliability
2. Custom webhook script for formatting
3. RSS monitoring service triggers webhook

## Technical Considerations

### Scheduling Options
- **Cron jobs** on VPS/server
- **GitHub Actions** with scheduled workflows
- **Cloud Functions** (AWS Lambda, Google Cloud Functions)
- **Heroku Scheduler** for simple deployments

### Error Handling
- API rate limiting (Discord: 5 requests per 2 seconds per webhook)
- Network failure retry logic
- Fallback to simple text if embed formatting fails

### Message Formatting
- Use Discord embeds for rich formatting
- Include liturgical colors via embed colors
- Organize content in fields for readability
- Consider message length limits (2000 characters for content)

