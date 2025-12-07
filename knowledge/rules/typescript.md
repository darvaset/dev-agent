# TypeScript Rules

## Type Definitions

1. **Use `interface` over `type`** for object shapes (interfaces are more extensible)
2. **Explicit return types** on all exported functions
3. **Avoid `any`** - use `unknown` if type is truly unknown, then narrow
4. **Use strict mode** - ensure `strict: true` in tsconfig.json

## Code Style

```typescript
// ✅ Good - explicit types, interface for objects
interface User {
  id: number;
  name: string;
  email: string;
}

function getUser(id: number): Promise<User | null> {
  // implementation
}

// ❌ Bad - implicit any, type instead of interface
type User = { id; name; email }
function getUser(id) {
  // implementation
}
```

## Error Handling

```typescript
// ✅ Good - typed error handling
interface Result<T> {
  success: boolean;
  data?: T;
  error?: string;
}

async function fetchData(): Promise<Result<Data>> {
  try {
    const data = await api.get();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error instanceof Error ? error.message : 'Unknown error' };
  }
}

// ❌ Bad - throwing errors without types
async function fetchData() {
  const data = await api.get(); // throws on error
  return data;
}
```

## Imports

1. Group imports: external libraries, internal modules, types
2. Use absolute imports with path aliases (`@/`)
3. Import types separately when possible (`import type { X }`)

```typescript
// External
import { useState, useEffect } from 'react';
import { z } from 'zod';

// Internal
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/hooks/useAuth';

// Types
import type { User, Post } from '@/types';
```

## Naming Conventions

- `PascalCase` for types, interfaces, classes, components
- `camelCase` for variables, functions, methods
- `SCREAMING_SNAKE_CASE` for constants
- Prefix interfaces with `I` only if there's a corresponding class
- Boolean variables: `is`, `has`, `should`, `can` prefixes
