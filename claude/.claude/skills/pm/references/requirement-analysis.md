# Requirement Analysis Framework

When faced with vague or incomplete requirements, use this framework to clarify and structure them.

## Key Questions for Analysis

### Understanding the Problem

- **What problem are we solving?** - What is the current pain point?
- **Who has this problem?** - Which user persona or user segment?
- **How big is this problem?** - How many users? How often? Impact on business?
- **Why now?** - What triggered this request? What's changed?

### Defining the Solution

- **What is the proposed solution?** - How would you describe it?
- **Why this solution?** - Why not alternatives? Were other approaches considered?
- **What are the scope constraints?** - What's the minimum viable scope? Are there technical limitations?
- **What does success look like?** - How will we measure if this solves the problem?

### Identifying Scope

- **What's included?** - Specific features, workflows, user journeys
- **What's excluded?** - What are we not doing? Why?
- **What are the dependencies?** - Does this depend on other features or services?
- **What are the edge cases?** - Error scenarios, unusual user flows, unusual data patterns?

## Process: Breaking Down Complex Requirements

When a feature is complex:

1. **Break into smaller parts** - Can you split it into separate, deliverable user stories?
2. **Identify the MVP** - What's the minimum viable set of features?
3. **Sequence the work** - What should be built first? What depends on what?
4. **Define clear interfaces** - How do these parts interact?

Example:
- Feature: "Build a recommendation engine"
- Sub-features:
  1. Collect user behavior data
  2. Build recommendation algorithm
  3. Serve recommendations to users
  4. A/B test recommendations
  5. Monitor recommendation quality

## Red Flags for Incomplete Requirements

- No clear success metric - "It should be fast" vs "Load in <2s for 95% of users"
- Ambiguous scope - "Make it better" without defining what or how to measure
- Missing user perspective - No mention of user needs or user journey
- No edge case handling - What happens when things go wrong?
- Misaligned priorities - Unclear why this is important relative to other work

## Requirements Maturity Checklist

A requirement is ready for development when:

- [ ] Clear problem statement with business impact
- [ ] Identified user personas and their needs
- [ ] Well-defined acceptance criteria (testable, specific)
- [ ] User journey is documented
- [ ] Dependencies are identified
- [ ] Out-of-scope items are explicitly documented
