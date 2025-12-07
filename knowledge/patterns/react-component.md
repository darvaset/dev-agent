# React Component Pattern

Use this pattern for creating React components in TypeScript.

## Basic Component

```typescript
'use client'; // Only if using hooks or browser APIs

import { useState, useCallback } from 'react';
import type { FC, ReactNode } from 'react';

// Props interface - always explicit
interface ComponentNameProps {
  /** Required prop with description */
  title: string;
  /** Optional prop with default */
  variant?: 'primary' | 'secondary';
  /** Children if needed */
  children?: ReactNode;
  /** Event handler */
  onClick?: () => void;
}

/**
 * ComponentName - Brief description of what it does
 * 
 * @example
 * <ComponentName title="Hello" variant="primary" />
 */
export const ComponentName: FC<ComponentNameProps> = ({
  title,
  variant = 'primary',
  children,
  onClick,
}) => {
  // State hooks at the top
  const [isActive, setIsActive] = useState(false);
  
  // Callbacks
  const handleClick = useCallback(() => {
    setIsActive(prev => !prev);
    onClick?.();
  }, [onClick]);
  
  // Render
  return (
    <div 
      className={`component-name ${variant} ${isActive ? 'active' : ''}`}
      onClick={handleClick}
    >
      <h2>{title}</h2>
      {children}
    </div>
  );
};
```

## Component with Loading/Error States

```typescript
'use client';

import { useState, useEffect } from 'react';

interface DataDisplayProps {
  dataId: string;
}

interface Data {
  id: string;
  name: string;
}

export const DataDisplay: FC<DataDisplayProps> = ({ dataId }) => {
  const [data, setData] = useState<Data | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        const response = await fetch(`/api/data/${dataId}`);
        if (!response.ok) throw new Error('Failed to fetch');
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchData();
  }, [dataId]);
  
  // Early returns for states
  if (isLoading) {
    return <div className="animate-pulse">Loading...</div>;
  }
  
  if (error) {
    return <div className="text-red-500">Error: {error}</div>;
  }
  
  if (!data) {
    return <div>No data found</div>;
  }
  
  return (
    <div>
      <h1>{data.name}</h1>
    </div>
  );
};
```

## Form Component

```typescript
'use client';

import { useState, FormEvent } from 'react';

interface FormData {
  email: string;
  message: string;
}

interface ContactFormProps {
  onSubmit: (data: FormData) => Promise<void>;
}

export const ContactForm: FC<ContactFormProps> = ({ onSubmit }) => {
  const [formData, setFormData] = useState<FormData>({
    email: '',
    message: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      await onSubmit(formData);
      setFormData({ email: '', message: '' }); // Reset on success
    } finally {
      setIsSubmitting(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input
        type="email"
        value={formData.email}
        onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
        placeholder="Email"
        required
        className="w-full px-4 py-2 border rounded-lg"
      />
      <textarea
        value={formData.message}
        onChange={(e) => setFormData(prev => ({ ...prev, message: e.target.value }))}
        placeholder="Message"
        required
        className="w-full px-4 py-2 border rounded-lg"
      />
      <button
        type="submit"
        disabled={isSubmitting}
        className="px-6 py-2 bg-blue-600 text-white rounded-lg disabled:opacity-50"
      >
        {isSubmitting ? 'Sending...' : 'Send'}
      </button>
    </form>
  );
};
```
