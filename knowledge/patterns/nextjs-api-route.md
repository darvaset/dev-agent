# Next.js API Route Pattern

Use this pattern for creating API routes in Next.js 15 App Router.

## Basic Template

```typescript
import { NextRequest, NextResponse } from 'next/server';

// Type definitions for request/response
interface RequestBody {
  // Define expected request body
}

interface ResponseData {
  // Define response structure
}

interface ErrorResponse {
  error: string;
  details?: string;
}

export async function GET(request: NextRequest): Promise<NextResponse<ResponseData | ErrorResponse>> {
  try {
    // Get query parameters
    const searchParams = request.nextUrl.searchParams;
    const id = searchParams.get('id');
    
    if (!id) {
      return NextResponse.json(
        { error: 'Missing required parameter: id' },
        { status: 400 }
      );
    }
    
    // Fetch data
    const data = await fetchData(id);
    
    if (!data) {
      return NextResponse.json(
        { error: 'Resource not found' },
        { status: 404 }
      );
    }
    
    return NextResponse.json(data);
    
  } catch (error) {
    console.error('GET /api/route error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest): Promise<NextResponse<ResponseData | ErrorResponse>> {
  try {
    // Parse and validate body
    const body: RequestBody = await request.json();
    
    // Validate required fields
    if (!body.requiredField) {
      return NextResponse.json(
        { error: 'Missing required field: requiredField' },
        { status: 400 }
      );
    }
    
    // Process request
    const result = await processData(body);
    
    return NextResponse.json(result, { status: 201 });
    
  } catch (error) {
    if (error instanceof SyntaxError) {
      return NextResponse.json(
        { error: 'Invalid JSON in request body' },
        { status: 400 }
      );
    }
    
    console.error('POST /api/route error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

## With Database (Prisma)

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function GET(request: NextRequest) {
  try {
    const items = await prisma.item.findMany({
      take: 20,
      orderBy: { createdAt: 'desc' },
      select: {
        id: true,
        name: true,
        // Only select needed fields
      }
    });
    
    return NextResponse.json({ items });
  } catch (error) {
    console.error('Database error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch items' },
      { status: 500 }
    );
  }
}
```

## With Dynamic Route

```typescript
// app/api/users/[id]/route.ts

import { NextRequest, NextResponse } from 'next/server';

interface RouteParams {
  params: {
    id: string;
  };
}

export async function GET(
  request: NextRequest,
  { params }: RouteParams
) {
  const { id } = params;
  
  // ... handle request
}
```
