# [Feature/Project Name]

## Metadata

- **Author(s)**: [Your name]
- **Status**: Draft | In Review | Approved | Implemented
- **Created**: [YYYY-MM-DD]
- **Last Updated**: [YYYY-MM-DD]
- **Reviewers**: [Key stakeholders]

## Summary

[2-3 sentences describing what this EDD covers and what problem it solves]

---

## 1. Problem Statement

### Background
[Describe the current situation and context]

### Problem
[What specific problem are we solving? Why is it important?]

### Goals
- Goal 1
- Goal 2
- Goal 3

### Non-Goals
[What are we explicitly NOT doing in this iteration?]

### Success Metrics
- Metric 1: [e.g., Response time < 200ms for 95th percentile]
- Metric 2: [e.g., Support 1000 concurrent users]

---

## 2. Proposed Solution

### High-Level Architecture

[Provide a system diagram showing major components and data flow]

```
[Diagram - use Mermaid, PlantUML, or ASCII art]
```

**Key Components**:
- **Component A**: [Brief description]
- **Component B**: [Brief description]

**Data Flow**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

### API Design

[Choose REST, GraphQL, or gRPC based on your needs]

**For REST APIs**:
```
GET    /api/v1/resources/{id}
POST   /api/v1/resources
PUT    /api/v1/resources/{id}
DELETE /api/v1/resources/{id}

Request/Response schemas: [Brief description or link to OpenAPI spec]
```

**For GraphQL**:
```graphql
type Resource {
  id: ID!
  name: String!
  # Key fields only
}

type Query {
  resource(id: ID!): Resource
}

type Mutation {
  createResource(input: CreateResourceInput!): Resource!
}
```

**For gRPC**:
```protobuf
service ResourceService {
  rpc GetResource(GetResourceRequest) returns (Resource) {}
  rpc CreateResource(CreateResourceRequest) returns (Resource) {}
}
```

### Data Model

**Database Schema**:
```sql
-- Main table(s) with key columns, indexes, and constraints
CREATE TABLE resources (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_resources_name ON resources(name);
```

**Entity Relationships**: [Brief description or ER diagram]

### Security & Authentication

- **Authentication**: [JWT / OAuth / API Keys]
- **Authorization**: [RBAC / Permissions model]
- **Data Encryption**: [At rest / In transit]
- **Input Validation**: [Key validation rules]
- **Rate Limiting**: [Limits per user/IP]

### Performance Considerations

- **Expected Load**: [RPS, concurrent users, data volume]
- **Caching Strategy**: [Redis/CDN/Application cache with TTLs]
- **Database Optimization**: [Indexes, connection pooling, read replicas]
- **Async Processing**: [Background jobs, queues]
- **Scalability**: [Horizontal/vertical scaling approach]

---

## 3. Implementation Plan

### Phase 1: Foundation
- [ ] Database schema setup
- [ ] Basic API endpoints
- [ ] Authentication scaffolding

**Timeline**: [Estimate]

### Phase 2: Core Features
- [ ] Business logic implementation
- [ ] Validation and error handling
- [ ] Unit and integration tests

**Timeline**: [Estimate]

### Phase 3: Polish & Launch
- [ ] Performance optimization
- [ ] Documentation
- [ ] Monitoring and alerts
- [ ] Load testing

**Timeline**: [Estimate]

---

## 4. Testing Strategy

### Unit Tests
- Coverage goal: [e.g., 80% for business logic]
- Focus: Model validation, business logic, utilities

### Integration Tests
- Coverage: All API endpoints
- Scenarios: Happy path, error cases, edge cases

### Performance Tests
- Load testing: [Target load]
- Stress testing: [Find breaking point]
- Tools: [JMeter, k6, Locust]

### Security Tests
- Penetration testing
- Dependency vulnerability scanning

---

## 5. Alternatives Considered

### Alternative 1: [Name]
**Pros**:
- [Pro 1]
- [Pro 2]

**Cons**:
- [Con 1]
- [Con 2]

**Decision**: [Why was this not chosen?]

---

## 6. Open Questions

- [ ] **Q1**: [Question that needs discussion]
- [ ] **Q2**: [Another unresolved issue]

---

## 7. References

- [Related EDD: Link]
- [External documentation: Link]
- [Research or blog post: Link]

---

## 8. Review History

| Date       | Reviewer | Status   | Comments           |
| ---------- | -------- | -------- | ------------------ |
| YYYY-MM-DD | [Name]   | Reviewed | [Feedback summary] |
| YYYY-MM-DD | [Name]   | Approved | Ready for impl     |
