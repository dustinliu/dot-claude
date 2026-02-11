# Requirement Completeness Checklist

Use this checklist to ensure your requirements are complete and ready for development.

## Problem & Context

- [ ] **Problem is clearly stated** - What problem are we solving?
- [ ] **Business impact is documented** - Why is this important? (revenue, retention, engagement, etc.)
- [ ] **User impact is clear** - How does this help users?
- [ ] **Target users are identified** - Who is this for? (specific personas or segments)

## User Stories & Acceptance Criteria

- [ ] **User stories follow the format** - "As a [user], I want [action], So that [benefit]"
- [ ] **User stories focus on outcomes** - Not implementation details
- [ ] **Each story has a clear user** - Not generic "user"
- [ ] **Acceptance criteria are specific** - Not "should work well" but "should load in <2s"
- [ ] **Acceptance criteria are testable** - Can QA verify these?
- [ ] **Acceptance criteria cover happy path** - The main success scenario
- [ ] **Acceptance criteria cover edge cases** - Unusual but valid scenarios
- [ ] **Acceptance criteria include error handling** - What happens when things go wrong?
- [ ] **Each story can be completed in 1-3 days** - Not too large to finish in a sprint

## User Journey

- [ ] **Feature workflow is described** - What are the steps a user goes through?
- [ ] **User interactions are documented** - What does the user see and do at each step?
- [ ] **Dependencies are identified** - Does this depend on other features?

## Edge Cases & Error Handling

- [ ] **Common edge cases are documented** - Empty data, large data, invalid input
- [ ] **Error scenarios are handled** - Network errors, timeouts, permission errors
- [ ] **User experience for errors is designed** - What should users see when something fails?
- [ ] **System behavior for errors is documented** - What should the system do?
- [ ] **Recovery scenarios are addressed** - How do users recover from errors?

## Scope Management

- [ ] **Scope is explicitly defined** - What IS included?
- [ ] **Out of scope items are listed** - What is NOT included?
- [ ] **Reasons for exclusions are documented** - Why are these not included?
- [ ] **Future enhancements are noted** - What might be added later?

## Risk & Dependency Management

- [ ] **Dependencies on other features are clear** - What must be built first?
- [ ] **Potential user experience issues are identified** - What could go wrong from user perspective?

## Approval & Alignment

- [ ] **Product owner has reviewed** - Does product agree this solves the problem?
- [ ] **No conflicting requirements exist** - Are there contradictions?
- [ ] **Team agrees on priority** - Is this prioritized relative to other work?

## Quality & Clarity

- [ ] **Requirements are clear** - Could someone understand this without asking questions?
- [ ] **No jargon without explanation** - Are all terms clearly defined?
- [ ] **Concise but complete** - 3-5 pages? (Not 50 pages, not 1 page)
- [ ] **Organized logically** - Is it easy to navigate?
- [ ] **Free of ambiguity** - No vague language like "should be fast" or "user-friendly"
- [ ] **No implementation details** - Requirements say "what", not "how"
- [ ] **Examples are provided** - Where clarity helps, examples are included
- [ ] **Links to related docs** - Design docs, research, specifications

## Before Handing Off to Development

**Final Review:**
- [ ] Requirements have been reviewed by product, engineering, and design
- [ ] All questions have been answered
- [ ] No ambiguities remain
- [ ] Team has capacity to start work
- [ ] All dependencies are available or scheduled
- [ ] Success metrics can be tracked
- [ ] Tests can be written based on acceptance criteria

**Sign-Off:**
- [ ] Product owner approves
- [ ] Engineering lead approves
- [ ] Ready to start development

---

## Common Gaps to Look For

❌ **Problem unclear** - "Make it faster" vs ✅ "Reduce load time from 5s to <2s"

❌ **Too large** - Can't complete in a sprint vs ✅ "Completable in 3 days"

❌ **Missing edge cases** - Only happy path documented vs ✅ "Includes error scenarios"

❌ **Vague criteria** - "Should work well" vs ✅ "Response time <500ms for 95% of requests"

❌ **Implementation focused** - "Add a dropdown" vs ✅ "Allow filtering by category"

❌ **No dependencies noted** - Risk of surprises vs ✅ "Depends on user auth service (Story #123)"

❌ **Unclear scope** - Team builds more than intended vs ✅ "Out of scope: mobile app, A/B testing"

---

## Scoring: Requirement Maturity

**Score each section:**
- 🟢 Complete (all checkboxes checked)
- 🟡 Mostly complete (80%+ checked, minor gaps)
- 🔴 Incomplete (significant gaps)

**Ready to develop when:**
- Problem & Context: 🟢
- User Stories & Acceptance Criteria: 🟢
- Edge Cases & Error Handling: 🟢
- Scope Management: 🟢
- All other sections: 🟢 or 🟡
