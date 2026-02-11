# User Story Template

## [Story ID]: [Story Title]

### Story

```
As a [user type],
I want to [action/capability],
So that [benefit/value].
```

**Example:**
```
As a customer who forgot my password,
I want to reset it via email,
So that I can regain access to my account.
```

---

### Acceptance Criteria

Define what success looks like. Make criteria specific and testable.

- [ ] Given [precondition], When [user action], Then [observable outcome]
- [ ] Given [precondition], When [user action], Then [observable outcome]
- [ ] Given [precondition], When [user action], Then [observable outcome]

**Example:**
```
- [ ] Given I'm on the login page, When I click "Forgot Password", Then I see a form asking for my email
- [ ] Given I enter my email and click submit, When my email is in the system, Then a password reset link is sent within 2 minutes
- [ ] Given the link is valid, When I click it, Then I can set a new password
- [ ] Given the email is not in the system, When the user submits, Then a confirmation message is shown
- [ ] Given the reset link expires, When the user clicks it, Then an error message is shown with option to request a new link
```

---

### Story Details

**Priority:** [High / Medium / Low]

**Depends On:** [Other stories or features this depends on]

---

## Story Review Checklist

Before finalizing a story, verify:

- [ ] Is the user need clear? Does it explain who the user is and what they need?
- [ ] Is the acceptance criteria testable? (Not subjective like "user-friendly")
- [ ] Do acceptance criteria cover the happy path?
- [ ] Do acceptance criteria cover edge cases (empty data, errors, etc.)?
- [ ] Can this be completed in 1-3 days?
- [ ] Are dependencies identified?
- [ ] Does this story provide user value?
