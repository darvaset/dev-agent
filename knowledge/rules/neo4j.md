# Neo4j Rules

## Cypher Query Best Practices

### Node Labels
- Use PascalCase: `Person`, `Club`, `NationalTeam`
- Be specific: prefer `Person` over `Entity`

### Relationship Types
- Use SCREAMING_SNAKE_CASE: `PLAYED_FOR`, `MANAGED`, `REPRESENTED`
- Use verbs: `FOLLOWS`, `CREATED`, `BELONGS_TO`

### Properties
- Use snake_case: `start_date`, `end_date`, `first_cap`
- Be consistent with naming across node types

## Query Patterns

### Basic Match
```cypher
// ✅ Good - specific labels, parameterized
MATCH (p:Person {id: $personId})-[:PLAYED_FOR]->(c:Club)
RETURN p.name, c.name

// ❌ Bad - no labels, hardcoded values
MATCH (p)-[r]->(c)
WHERE p.id = 123
RETURN p, c
```

### Shortest Path
```cypher
// Find shortest path between two people
MATCH (p1:Person {id: $startId}), (p2:Person {id: $endId})
MATCH path = shortestPath((p1)-[*..6]-(p2))
RETURN path
```

### Date Overlap Query
```cypher
// Find teammates (overlapping stints at same club)
MATCH (p1:Person)-[r1:PLAYED_FOR]->(c:Club)<-[r2:PLAYED_FOR]-(p2:Person)
WHERE p1.id = $personId
  AND p1 <> p2
  AND r1.start_date <= coalesce(r2.end_date, date())
  AND coalesce(r1.end_date, date()) >= r2.start_date
RETURN DISTINCT p2, c, r1, r2
```

## Indexing

Always create indexes for frequently queried properties:

```cypher
CREATE INDEX person_id FOR (p:Person) ON (p.id);
CREATE INDEX person_name FOR (p:Person) ON (p.name);
CREATE INDEX club_id FOR (c:Club) ON (c.id);
```

## Node.js Driver

```typescript
import neo4j from 'neo4j-driver';

// ✅ Good - use driver instance, close sessions
const driver = neo4j.driver(uri, neo4j.auth.basic(user, password));
const session = driver.session();

try {
  const result = await session.run(
    'MATCH (p:Person {id: $id}) RETURN p',
    { id: personId }
  );
  return result.records.map(r => r.get('p').properties);
} finally {
  await session.close();
}

// ❌ Bad - not closing session, string concatenation
const result = await session.run(`MATCH (p:Person {id: ${id}}) RETURN p`);
```

## Data Modeling

1. **Nodes** for entities (Person, Club, NationalTeam)
2. **Relationships** for connections with properties for temporal data
3. **Properties** on relationships for context (dates, roles)
4. Keep nodes lightweight - only essential properties
