# Tailwind CSS Rules

## Class Organization

Order Tailwind classes consistently:

1. Layout (display, position, flex/grid)
2. Sizing (width, height, padding, margin)
3. Typography (font, text)
4. Visual (background, border, shadow)
5. Interactive (hover, focus, transition)

```tsx
// ✅ Good - organized classes
<div className="flex items-center justify-between p-4 mb-2 text-sm font-medium bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">

// ❌ Bad - random order
<div className="hover:shadow-md bg-white p-4 flex shadow-sm font-medium rounded-lg text-sm mb-2 items-center transition-shadow justify-between">
```

## Responsive Design

Use mobile-first approach:

```tsx
// ✅ Good - mobile first
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4">

// ❌ Bad - desktop first
<div className="grid grid-cols-4 md:grid-cols-2 sm:grid-cols-1">
```

## Component Patterns

```tsx
// Button variants
const buttonVariants = {
  primary: "bg-blue-600 hover:bg-blue-700 text-white",
  secondary: "bg-gray-200 hover:bg-gray-300 text-gray-800",
  danger: "bg-red-600 hover:bg-red-700 text-white",
};

// Card pattern
<div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">

// Input pattern
<input className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all" />
```

## Dark Mode

Use dark: prefix consistently:

```tsx
<div className="bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100">
```

## Avoid

1. Don't use `@apply` excessively - defeats the purpose of utility classes
2. Don't create too many custom colors - use the default palette
3. Don't use arbitrary values `w-[137px]` unless absolutely necessary
