# Orthocal.info Analysis

## Available Data Sources

### 1. REST API
- **Base URL**: https://orthocal.info/api/
- **Get Today's Data**: `/api/{cal}/` where cal = "gregorian" or "julian"
- **Get Specific Date**: `/api/{cal}/{year}/{month}/{day}/`
- **Response Format**: JSON
- **Timezone**: Pacific Time

### 2. RSS Feeds
- **Default (Gregorian)**: https://orthocal.info/api/feed/
- **Gregorian**: https://orthocal.info/api/feed/gregorian/
- **Julian**: https://orthocal.info/api/feed/julian/

### 3. iCal Feeds
- **Gregorian**: https://orthocal.info/api/gregorian/ical/
- **Julian**: https://orthocal.info/api/julian/ical/

## Data Structure (JSON Response)
The API returns comprehensive liturgical information including:
- Date information (year, month, day, weekday)
- Liturgical titles and feast descriptions
- Feast level and descriptions
- Saints commemorations
- Scripture readings with full text
- Service notes
- Fast level information

## Key Features for Discord Integration
1. **Daily Data**: Perfect for automated daily posts
2. **Rich Content**: Includes feast days, saints, and scripture readings
3. **Multiple Formats**: API (JSON), RSS, and iCal options
4. **Reliable Source**: Well-maintained Orthodox calendar resource
5. **Free Access**: No authentication required

## Recommended Approach
Use the REST API endpoint `/api/gregorian/` for daily Discord posts as it:
- Returns current day's data automatically
- Provides structured JSON for easy parsing
- Includes all necessary liturgical information
- Doesn't require date calculations

