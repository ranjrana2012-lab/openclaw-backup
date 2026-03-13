---
name: daily-life
description: "Daily life assistant - coffee shop finder, weather alerts, recurring reminders"
metadata:
  openclaw:
    emoji: "☕"
    requires:
      config: []
---

# Daily Life Assistant

Coffee shops, weather, and reminders.

## Coffee Shop Finder

### Query Examples
- "Find me a coffee shop nearby"
- "Coffee shops within walking distance"
- "Best rated cafes near me"

### What You Get
- Name and rating (⭐ 4.5)
- Walking distance (12 min walk)
- WiFi availability (if known)
- Opening hours
- One-line review summary

### Preferences
- Prefer independent shops over chains
- "Walking distance" = under 20 minutes on foot
- Sort by rating + distance combo

### API
```bash
GOOGLE_PLACES_API_KEY=xxx
HOME_LOCATION="lat,lng"
```

## Weather

### Query Examples
- "What's the weather?"
- "Do I need a jacket today?"
- "Weekend forecast?"

### What You Get
- Current conditions
- Today's high/low
- 7-day forecast summary
- Extreme weather warnings (if any)

### Proactive Alerts
Even without asking, warn about:
- Extreme cold (< -10°C)
- Extreme heat (> 35°C)
- Storms incoming
- Heavy rain/snow

### Keep It Brief
No hourly breakdowns unless asked.

## Reminders

### Recurring Reminders
- **Rehab exercises**: Daily at 10am and 6pm
- **Weekly standup**: Every Monday 9:45am (15 min before 10am meeting)

### One-Time Reminders
- "Remind me to call mom tomorrow"
- "Remind me about the meeting in 2 hours"

### Snooze Support
- "Snooze 30 min" → Remind again in 30 minutes
- "Snooze until tomorrow" → Remind at 9am next day

### Confirmation
Always confirm before setting:
```
⏰ Setting reminder:
- What: [Description]
- When: [Date/Time]
- Recurring: [Yes/No]

Confirm? (yes/no)
```

## APIs

```bash
# Google Places (coffee shops)
GOOGLE_PLACES_API_KEY=xxx

# Weather (OpenWeatherMap or similar)
WEATHER_API_KEY=xxx
HOME_LOCATION="lat,lng"

# Timezone
TIMEZONE="UTC"
```
