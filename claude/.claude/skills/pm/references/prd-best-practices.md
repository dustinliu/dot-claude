# PRD Best Practices

## What Makes a Good PRD

A good PRD is:
- **Clear** - Anyone reading it can understand the feature without asking questions
- **Complete** - Nothing important is left out or assumed
- **Specific** - Uses concrete examples and measurable criteria
- **Actionable** - Developers can start building without extensive clarification
- **Concise** - Focuses on what matters, avoids unnecessary detail

## Section-by-Section Guidance

### Overview / Problem Statement

**Purpose**: Set the context and explain why this feature matters.

**Include:**
- One-sentence summary of the feature
- Problem it solves
- Why this is important (business impact, user impact)
- Target user or use case

**Avoid:**
- Implementation details
- Solution assumptions
- Lengthy background (focus on what matters)

**Example:**
```
## Problem Statement

Many customers abandon their cart because they can't see product recommendations
during checkout. Our data shows 15% of users leave without completing purchase when
they don't see complementary products.

This feature recommends products based on the user's cart to increase average order
value and reduce checkout abandonment.
```

### Target Users

**Purpose**: Describe who this feature is for and their needs.

**Include:**
- User personas or segments
- Their current pain points
- How they'll use this feature
- User journey or context

**Example:**
```
## Target Users

Primary: Active shoppers with cart values >$50
- Currently abandon carts when unsure about product fit
- Spend 3-5 minutes browsing before checkout
- Respond positively to personalized suggestions

Secondary: Price-conscious shoppers
- Looking for value alternatives or complementary items
- May add items if they see good recommendations
```

### User Stories & Requirements

**Purpose**: Break down the feature into implementable pieces.

**Include:**
- 3-8 user stories that collectively describe the feature
- Each story has clear acceptance criteria
- Requirements are specific and testable

**Format**: Use the user story format from the User Story skill:
```
As a [user type],
I want to [action],
So that [benefit].

Acceptance Criteria:
Given [context]
When [action]
Then [outcome]
```

### User Journey

**Purpose**: Describe how users will interact with this feature from start to finish.

**Include:**
- Step-by-step flow of how users will use the feature
- What users see and do at each stage
- When and where the feature fits into their workflow

**Avoid:**
- Implementation or technical details
- How the system works internally
- Database or system architecture

**Example:**
```
## User Journey

1. User browses products while building their cart
2. As user adds items to cart, they see personalized product recommendations
3. User can view recommended items by clicking "View details"
4. User can add recommended items directly to cart from recommendation card
5. At checkout, user reviews all items including recommended ones before purchasing
```

### Edge Cases & Error Handling

**Purpose**: Describe what happens when things don't go perfectly.

**Include:**
- Error scenarios (no recommendations available, system errors)
- How the UI should handle errors
- Performance degradation scenarios
- Data edge cases

**Example:**
```
## Edge Cases & Error Handling

1. No recommendations available
   - Display: "Based on your choices, here are similar products"
   - Show seasonal or trending products instead

2. Recommendation service is slow/down
   - Timeout after 1 second
   - Display "See similar products" link (to search page)
   - Log error for monitoring

3. User has empty or very new cart
   - Show popular/trending products
   - Personalize as cart accumulates items

4. Inventory changes during checkout
   - If recommended item goes out of stock:
     - Remove from recommendations
     - Show next best alternative
```

### Out of Scope

**Purpose**: Be explicit about what's NOT included. This prevents scope creep and manages expectations.

**Include:**
- Features that were considered but excluded
- Why they're out of scope
- Potential future enhancements

**Example:**
```
## Out of Scope

- A/B testing different recommendation algorithms (Phase 2)
- Personalization based on user preferences (Phase 2)
- Mobile app recommendations (Phase 2)
- Admin dashboard for recommendation management (Phase 3)
```

### Risks & Dependencies

**Purpose**: Flag technical risks and dependencies engineers need to know about.

**Include:**
- Technical risks that could affect implementation
- Dependencies on other systems/features
- Data quality risks
- Performance or scalability concerns

**Example:**
```
## Risks & Dependencies

Dependencies:
- Depends on User Recommendation Service API
- Requires user browsing history data availability

Risks:
- Recommendation service latency could impact checkout performance
  Mitigation: Implement 1-second timeout, cache fallback
- Limited historical data for new users
  Mitigation: Default to popular products for new users
```

## Common PRD Pitfalls

**1. Mixing "why" with "how"**
- PRD explains what and why
- Engineers decide how to build it
- Avoid: "Add a dropdown menu" (this is how)
- Better: "Allow filtering by brand" (this is what)

**2. Missing user perspective**
- Every feature should map to a user need
- Include user journey, not just requirements list

**3. Too much detail in wrong places**
- Avoid 50-page PRDs with excessive background
- Focus on what's needed for decision-making
- Keep it readable (3-5 pages is typical)

**4. Undefined scope**
- Be explicit about what's in scope
- Be explicit about what's out of scope
- This prevents misalignment later

## PRD Review Checklist

Before finalizing your PRD, verify:

- [ ] Is the problem statement clear? Would anyone understand why this matters?
- [ ] Does every requirement map back to a user need?
- [ ] Are acceptance criteria testable (not subjective)?
- [ ] Are edge cases documented?
- [ ] Are dependencies identified?
- [ ] Is out-of-scope clearly documented?
- [ ] Could an engineer start building based on this PRD?
- [ ] Is it concise? (Ideally 3-5 pages)
- [ ] Are there no contradictions or ambiguities?
