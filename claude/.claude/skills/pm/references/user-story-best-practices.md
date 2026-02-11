# User Story Best Practices

## Structure

### Format
```
As a [user type],
I want to [action/capability],
So that [benefit/value].
```

**Example:**
```
As a customer,
I want to save my payment information,
So that I can check out faster on my next purchase.
```

### Writing Guidelines

**Be specific about the user type**
- Good: "As a product admin"
- Bad: "As a user"
- Better: "As a product admin with editor permissions"

**Describe the action, not the implementation**
- Good: "I want to filter orders by status"
- Bad: "I want a dropdown menu for order status"
- This keeps the solution open to different implementations

**Focus on the benefit**
- Good: "So that I can prioritize high-value customers"
- Bad: "So that I can see customers" (too generic)

## Acceptance Criteria

Acceptance criteria define when a user story is complete and ready for production.

### SMART Criteria

Make criteria **Specific, Measurable, Achievable, Relevant, Testable**:

**Example - Bad:**
```
- The search should be fast
- Results should be relevant
```

**Example - Good:**
```
- Search returns results in <500ms for 95% of queries
- When searching for "blue shirt", blue shirts appear in top 5 results
- Search is case-insensitive
- Empty search field returns all products
```

### Format

```
Given [context/precondition]
When [user action]
Then [observable outcome]
```

**Example:**
```
Given I'm logged in with a saved payment method
When I proceed to checkout
Then my saved payment method is pre-selected as the default
```

### Common Acceptance Criteria Categories

**Functional Requirements**
- What should the system do?
- What data should be displayed?
- What validations should occur?

**Non-Functional Requirements**
- Performance (response time, throughput)
- Security (authentication, authorization)
- Reliability (error handling, retries)
- Usability (accessibility, mobile support)

**Edge Cases**
- What happens with empty data?
- What happens with invalid input?
- What happens with very large datasets?
- What happens when external services fail?

**Error Scenarios**
- Network timeout behavior
- Invalid input handling
- Permission denied scenarios
- Resource not found responses

## Story Size

### User Stories Should Be Small

A good user story is:
- **Completable in 1-3 days** - If it's bigger, break it down
- **Independently implementable** - Doesn't require waiting for another story
- **Independently valuable** - Provides user value without other stories

### Breaking Down Large Stories

If a story is too big:
1. **Split by workflow** - Different steps in a user journey
2. **Split by role** - Admin view vs Customer view
3. **Split by complexity** - Happy path vs error handling
4. **Split by data volume** - Handling 10 items vs 1000 items

**Example breakdown:**
- Story: "Users can manage their profile"
  1. Users can view their profile
  2. Users can edit their basic info (name, email)
  3. Users can upload a profile picture
  4. Users can change their password

## Dependencies and Blockers

Document dependencies clearly:

```
This story depends on:
- User authentication feature (Story #123)
- Payment processing feature (Story #124)

This story blocks:
- Refund processing workflow (Story #200)
```

## Examples of Well-Written User Stories

**Story 1: Password Reset**
```
As a user who forgot my password,
I want to reset it via email,
So that I can regain access to my account.

Acceptance Criteria:
Given I'm on the login page
When I click "Forgot Password"
Then I see a form asking for my email

Given I enter my email and click submit
When my email is in the system
Then a password reset link is sent within 2 minutes
And I see a confirmation message

Given I click the reset link in the email
When the link is valid (not expired, not used)
Then I can set a new password
And the link becomes invalid after use or 24 hours

Edge Cases:
- Email not in system → Show generic message (don't reveal if email exists)
- Link expires → Show clear error message with "request new link" option
- User tries to use old link → Show they already reset, offer password reset again
```

**Story 2: Search Filtering**
```
As a customer shopping for electronics,
I want to filter products by brand and price range,
So that I can find products that match my budget and preferences.

Acceptance Criteria:
Given I'm on the electronics category page
When I select a brand from the Brand filter
Then only products from that brand are displayed
And the page updates without full reload

Given I set a price range (min-max)
When I submit the price filter
Then only products within that range display
And prices are in my selected currency

Given I apply multiple filters
When I change one filter
Then other active filters remain applied

Performance:
- Filter changes update results in <500ms

Edge Cases:
- No products match filters → Show "No results" message with suggestion to adjust filters
- Multiple filters with conflicting results → Still show relevant message
```
