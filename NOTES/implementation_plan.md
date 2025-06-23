# Orthodox Calendar Discord Integration - Implementation Plan

## Solution Design

### Chosen Approach: Custom Webhook Solution
After analyzing the options, the custom webhook solution provides the best balance of:
- **Control**: Full control over message formatting and content
- **Reliability**: Direct API calls without third-party dependencies
- **Flexibility**: Easy to modify and extend functionality
- **Simplicity**: No bot permissions or complex authentication required

## Architecture

### Components
1. **Data Fetcher**: Retrieves daily calendar data from orthocal.info API
2. **Message Formatter**: Converts API data into Discord embed format
3. **Discord Poster**: Sends formatted message via webhook
4. **Scheduler**: Triggers daily execution (multiple deployment options)

### Data Flow
```
orthocal.info API → Data Fetcher → Message Formatter → Discord Webhook → #new-calendar channel
```

## Implementation Details

### 1. Core Script (Python)
- **File**: `orthodox_calendar_bot.py`
- **Dependencies**: `requests`, `datetime`, `json`
- **Functions**:
  - `fetch_calendar_data()`: Get data from orthocal.info API
  - `format_discord_message()`: Create Discord embed structure
  - `post_to_discord()`: Send webhook request
  - `main()`: Orchestrate the process

### 2. Configuration
- **File**: `config.json`
- **Contents**:
  - Discord webhook URL
  - Calendar type (gregorian/julian)
  - Message formatting preferences
  - Error handling settings

### 3. Message Format Design
- **Title**: Date and liturgical day (e.g., "June 22, 2025 - 2nd Sunday after Pentecost")
- **Description**: Fast level and description
- **Fields**:
  - Feasts (if any)
  - Commemorations (saints)
  - Scripture Readings (abbreviated list)
- **Color**: Liturgical color coding
- **Footer**: Source attribution to orthocal.info

### 4. Error Handling
- Network timeout handling
- API response validation
- Discord rate limiting respect
- Fallback to simple text message if embed fails
- Logging for debugging

## Deployment Options

### Option A: Simple Cron Job (Recommended for VPS)
- Deploy script to server
- Set up daily cron job
- Minimal resource usage

### Option B: GitHub Actions (Free Cloud Solution)
- Store script in GitHub repository
- Use GitHub Actions scheduled workflow
- No server maintenance required

### Option C: Cloud Function (Serverless)
- Deploy to AWS Lambda, Google Cloud Functions, or Azure Functions
- Use cloud scheduler for triggering
- Pay-per-use pricing

### Option D: Heroku (Easy Deployment)
- Deploy as simple Python app
- Use Heroku Scheduler add-on
- Free tier available

## Configuration Requirements

### User Setup Steps
1. Create Discord webhook in #new-calendar channel
2. Copy webhook URL
3. Choose deployment method
4. Configure script with webhook URL
5. Set up scheduling

### Security Considerations
- Store webhook URL as environment variable
- Never commit webhook URL to public repositories
- Use HTTPS for all API calls
- Implement basic rate limiting

## Extensibility Features

### Future Enhancements
- Multiple calendar support (Gregorian + Julian)
- Custom message templates
- Multiple Discord channels
- Web interface for configuration
- Email notifications as backup
- Integration with other Orthodox resources

### Customization Options
- Message formatting preferences
- Field selection (show/hide specific content)
- Posting time configuration
- Language localization support

## Testing Strategy
1. **Unit Tests**: Test individual functions
2. **Integration Tests**: Test API interactions
3. **Manual Testing**: Verify Discord message formatting
4. **Error Simulation**: Test failure scenarios
5. **Schedule Testing**: Verify timing accuracy

## Success Metrics
- Daily messages posted successfully
- Accurate liturgical information
- Proper message formatting
- Minimal downtime/errors
- User satisfaction with content quality

