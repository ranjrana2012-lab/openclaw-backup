---
name: calendar-family
description: "Google Calendar integration for personal and family schedule management - add events, check availability, get reminders"
metadata:
  openclaw:
    emoji: "📅"
    requires:
      config: []
---

# Calendar and Family Management

Google Calendar integration for schedule management.

## Capabilities

### Add Events
- "Schedule dentist Thursday at 3pm"
- "Block 2 hours for video editing tomorrow morning"
- "Add meeting with [person] next Tuesday at 2pm for 1 hour"

### Check Schedule
- "What do I have today?"
- "Am I free Friday afternoon?"
- "What's my week looking like?"

### Reminders
- Alert 30 minutes before video call meetings
- Daily schedule summary at 8am
- End-of-day summary at 6pm

## Confirmation Protocol

Always confirm before creating:
```
Adding: Dentist appointment
- Date: Thursday, Feb 20
- Time: 3:00 PM
- Duration: 1 hour
- Calendar: Personal

Confirm? (yes/no)
```

## Family Calendar (WhatsApp Group)

Family members can:
- Add events to shared family calendar
- Check the schedule
- Get reminders

### Language Handling
- Respond in the language of the message
- If Polish → respond in Polish
- If English → respond in English

## API Setup

```bash
# Google Calendar OAuth
GOOGLE_CLIENT_ID=xxx
GOOGLE_CLIENT_SECRET=xxx
GOOGLE_REFRESH_TOKEN=xxx
CALENDAR_ID=primary  # or family calendar ID
```

## Calendar IDs

| Calendar | ID | Purpose |
|----------|-----|---------|
| Personal | primary | Work, personal events |
| Family | family@group.v.calendar.google.com | Shared family events |
| Reminders | reminders | Task reminders |

## Reminder Format

```
📅 Reminder: [Event Name]
- Time: [Time]
- Location: [If any]
- Video call: [Link if any]

[30 minutes until event]
```

## Smart Features

- Detect conflicts when adding
- Suggest best times when asked
- Include travel time for off-site events
- Weather for outdoor events
