# Prisma Rules

## Schema Design

1. Use `snake_case` for database columns with `@map()`
2. Use `camelCase` in Prisma schema (TypeScript convention)
3. Always add `createdAt` and `updatedAt` timestamps
4. Use `@@index` for frequently queried fields
5. Use `@@map` for table names (snake_case)

## Example Schema

```prisma
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String?
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")
  
  posts     Post[]
  
  @@index([email])
  @@map("users")
}

model Post {
  id          Int      @id @default(autoincrement())
  title       String
  content     String?
  published   Boolean  @default(false)
  authorId    Int      @map("author_id")
  createdAt   DateTime @default(now()) @map("created_at")
  updatedAt   DateTime @updatedAt @map("updated_at")
  
  author      User     @relation(fields: [authorId], references: [id], onDelete: Cascade)
  
  @@index([authorId])
  @@index([published])
  @@map("posts")
}
```

## Queries

```typescript
// ✅ Good - select only needed fields, handle errors
async function getUser(id: number) {
  try {
    return await prisma.user.findUnique({
      where: { id },
      select: {
        id: true,
        email: true,
        name: true,
        posts: {
          where: { published: true },
          select: { id: true, title: true }
        }
      }
    });
  } catch (error) {
    console.error('Failed to fetch user:', error);
    return null;
  }
}

// ❌ Bad - fetching everything, no error handling
async function getUser(id: number) {
  return await prisma.user.findUnique({
    where: { id },
    include: { posts: true }
  });
}
```

## Migrations

1. Use `prisma migrate dev` during development
2. Use `prisma migrate deploy` in production
3. Review generated SQL before applying
4. Never modify migration files after they're committed

## Environment

```bash
# .env
DATABASE_URL="postgresql://user:password@localhost:5432/dbname?schema=public"

# For Supabase
DATABASE_URL="postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres"
```
