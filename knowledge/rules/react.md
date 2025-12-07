# React Rules

## Component Structure

1. **Functional components only** - No class components
2. **One component per file** (with exceptions for small helper components)
3. **Props interface defined explicitly**

## Component Template

```typescript
'use client' // Only if using hooks or browser APIs

import { useState, useCallback } from 'react';
import type { FC } from 'react';

interface ButtonProps {
  label: string;
  onClick?: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

export const Button: FC<ButtonProps> = ({
  label,
  onClick,
  variant = 'primary',
  disabled = false
}) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`btn btn-${variant}`}
    >
      {label}
    </button>
  );
};
```

## Hooks

```typescript
// ✅ Good - custom hook with clear interface
function useCounter(initialValue = 0) {
  const [count, setCount] = useState(initialValue);
  
  const increment = useCallback(() => setCount(c => c + 1), []);
  const decrement = useCallback(() => setCount(c => c - 1), []);
  const reset = useCallback(() => setCount(initialValue), [initialValue]);
  
  return { count, increment, decrement, reset };
}

// Usage
const { count, increment } = useCounter(10);
```

## State Management

1. **Local state first** - useState for component-specific state
2. **Lift state up** when multiple components need it
3. **Context for global state** (auth, theme, etc.)
4. **External stores** (Zustand, Redux) only when Context isn't enough

## Event Handlers

```typescript
// ✅ Good - handler defined with useCallback
const handleSubmit = useCallback(async (e: FormEvent) => {
  e.preventDefault();
  setLoading(true);
  try {
    await submitForm(formData);
  } finally {
    setLoading(false);
  }
}, [formData]);

// ❌ Bad - inline handler recreated every render
<form onSubmit={async (e) => {
  e.preventDefault();
  await submitForm(formData);
}}>
```

## Conditional Rendering

```typescript
// ✅ Good - early returns for cleaner JSX
if (loading) return <Spinner />;
if (error) return <Error message={error} />;
if (!data) return null;

return <DataDisplay data={data} />;

// ❌ Bad - nested ternaries
return loading ? <Spinner /> : error ? <Error /> : data ? <DataDisplay data={data} /> : null;
```

## File Naming

- Components: `PascalCase.tsx` - `UserProfile.tsx`
- Hooks: `camelCase.ts` - `useAuth.ts`
- Utils: `camelCase.ts` - `formatDate.ts`
- Types: `camelCase.types.ts` or `types/index.ts`
