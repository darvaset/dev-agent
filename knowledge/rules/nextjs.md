# Next.js Rules

## App Router (Next.js 13+)

1. **Use App Router** - All new code should use the app/ directory structure
2. **Server Components by default** - Only use `'use client'` when necessary
3. **Prefer Server Actions** for mutations over API routes when possible

## File Conventions

```
src/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Home page
│   ├── loading.tsx         # Loading UI
│   ├── error.tsx           # Error UI
│   ├── not-found.tsx       # 404 page
│   ├── api/
│   │   └── [route]/
│   │       └── route.ts    # API route handler
│   └── [feature]/
│       ├── page.tsx
│       └── components/     # Feature-specific components
├── components/
│   ├── ui/                 # Reusable UI components
│   └── [feature]/          # Feature components
├── lib/                    # Utilities, helpers
├── hooks/                  # Custom React hooks
└── types/                  # TypeScript types
```

## API Routes

```typescript
// ✅ Good - proper Next.js 15 API route
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    const data = await fetchData();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch data' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    // validate body
    const result = await createData(body);
    return NextResponse.json(result, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create' },
      { status: 500 }
    );
  }
}
```

## Client vs Server Components

```typescript
// Server Component (default) - can use async/await directly
async function ServerComponent() {
  const data = await fetchData(); // Direct DB/API call
  return <div>{data.title}</div>;
}

// Client Component - needs 'use client' directive
'use client'
import { useState } from 'react';

function ClientComponent() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

## Environment Variables

- `NEXT_PUBLIC_*` - Exposed to browser
- All others - Server-only
- Use `.env.local` for local development
- Never commit `.env.local`

## Performance

1. Use `next/image` for images
2. Use `next/link` for navigation
3. Use `next/font` for fonts
4. Implement loading states with `loading.tsx`
5. Use Suspense boundaries for streaming
