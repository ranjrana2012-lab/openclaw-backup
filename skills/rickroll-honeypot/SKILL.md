---
name: rickroll-honeypot
description: "WordPress login honeypot that rickrolls bots - catches automated scanners with style"
metadata:
  openclaw:
    emoji: "🎭"
    requires:
      config: []
---

# WordPress Rickroll Honeypot

Catch bots scanning for WordPress admin pages with a rickroll.

## What It Does

1. Creates fake `/wp-login` route
2. Shows convincing WordPress login page
3. When form submitted → redirect to Rick Astley
4. Logs attempts for entertainment

## Implementation (Next.js)

### pages/wp-login.js (or app/wp-login/route.tsx)

```tsx
export default function WpLogin() {
  return (
    <div style={{
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      background: '#f0f0f1',
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    }}>
      <form action="/api/wp-login-submit" method="POST" style={{
        background: 'white',
        padding: '30px',
        borderRadius: '5px',
        boxShadow: '0 1px 3px rgba(0,0,0,0.13)'
      }}>
        <h1 style={{ fontSize: '14px', marginBottom: '20px' }}>Powered by WordPress</h1>
        <label style={{ display: 'block', marginBottom: '5px', fontSize: '14px' }}>
          Username or Email Address
        </label>
        <input type="text" name="log" style={{
          width: '100%',
          padding: '6px 10px',
          marginBottom: '15px',
          fontSize: '24px',
          border: '1px solid #8c8f94'
        }} />
        <label style={{ display: 'block', marginBottom: '5px', fontSize: '14px' }}>
          Password
        </label>
        <input type="password" name="pwd" style={{
          width: '100%',
          padding: '6px 10px',
          marginBottom: '15px',
          fontSize: '24px',
          border: '1px solid #8c8f94'
        }} />
        <button type="submit" style={{
          background: '#2271b1',
          color: 'white',
          border: 'none',
          padding: '10px 20px',
          borderRadius: '3px',
          cursor: 'pointer'
        }}>
          Log In
        </button>
      </form>
    </div>
  );
}
```

### API Route

```typescript
// app/api/wp-login-submit/route.ts
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  const formData = await request.formData();
  const ip = request.headers.get('x-forwarded-for') || 'unknown';
  const userAgent = request.headers.get('user-agent') || 'unknown';
  
  // Log the attempt
  console.log(`🤖 BOT CAUGHT: ${new Date().toISOString()}`);
  console.log(`   IP: ${ip}`);
  console.log(`   UA: ${userAgent}`);
  console.log(`   User: ${formData.get('log')}`);
  console.log(`   Pass: ${formData.get('pwd')}`);
  
  // Rickroll them
  return NextResponse.redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ');
}
```

## Logging Output

```
🤖 BOT CAUGHT: 2024-02-21T10:30:45.123Z
   IP: 192.168.1.100
   UA: Mozilla/5.0 (compatible; Googlebot/2.1)
   User: admin
   Pass: password123
```

## Deployment

Works with:
- Vercel (recommended)
- Netlify
- Any Next.js host

## Stats

Track how many bots you've caught:
- Add a simple counter to the API route
- Display in a private admin page

## Disclaimer

For YOUR domain only. Don't deploy this to catch legitimate users.
