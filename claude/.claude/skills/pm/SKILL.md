---
name: pm
description: Help write and refine PRDs and user stories to communicate feature requirements to engineers. Use when Claude needs to: (1) Write or improve Product Requirements Documents (PRDs), (2) Analyze and clarify product requirements from engineers' perspective, (3) Generate user stories with clear acceptance criteria, (4) Translate feature concepts into structured requirements engineers can build from, or (5) Review requirement documents for clarity, specificity, and testability.
---

# Product Manager Skill

This skill helps you write clear, specific product requirements that engineers can understand and build from. It covers PRD writing, requirements analysis, and user story generation focused on what engineers need to know.

**Note:** This skill is for communicating product requirements to engineers. It does not cover project management, budgeting, timelines, or organizational/business planning—those are separate concerns.

## Core Workflows

### Writing or Improving a PRD

Use the PRD Template in `assets/prd-template.md` as a starting point:

1. **Gather context**: Understand the problem, user needs, and business goals
2. **Fill the template**: Complete each section of the PRD template
3. **Review for clarity**: Ensure acceptance criteria are specific and testable
4. **Iterate**: Refine based on feedback

**Key sections:**
- **Problem Statement** - What problem are you solving?
- **Target Users** - Who are the users and what are their needs?
- **User Stories** - Describe the user workflows and interactions
- **Requirements** - What the feature needs to do

### Analyzing and Clarifying Requirements

When a feature request is vague or incomplete:

1. **Ask clarifying questions** - Use the framework in `references/requirement-analysis.md`
2. **Identify gaps** - What's missing? What's ambiguous?
3. **Break down complexity** - Split complex features into smaller, implementable pieces
4. **Define scope** - What's in scope? What's out of scope?

### Generating User Stories

Transform requirements into actionable user stories:

1. **Identify user personas** - Who are the users?
2. **Use the user story format** - See `references/user-story-template.md` for structure
3. **Write acceptance criteria** - Make them SMART: Specific, Measurable, Achievable, Relevant, Testable
4. **Link to requirements** - Connect each story to the parent requirement

## Best Practices

For detailed guidance on requirement analysis, user story writing, and PRD best practices, see:
- `references/requirement-analysis.md` - Framework for analyzing incomplete or vague requirements
- `references/user-story-best-practices.md` - Principles for writing clear user stories
- `references/prd-best-practices.md` - Guidelines for well-structured PRDs

## Templates

The `assets/` directory contains ready-to-use templates:

- **PRD Template** (`assets/prd-template.md`) - Full PRD structure for new features
- **User Story Template** (`assets/user-story-template.md`) - Single user story format
- **Requirement Checklist** (`assets/requirement-checklist.md`) - Validation checklist for complete requirements

## Quick Tips

**Write clear user stories**: "As a [user type], I want to [action], so that [benefit]"

**Make acceptance criteria testable**: Avoid vague terms like "good" or "fast". Use specific, measurable criteria.

**Identify edge cases**: Ask "What could go wrong?" and document how the system should behave in error scenarios.

**Link requirements**: Every user story should trace back to a business goal or user need.

**Iterate based on feedback**: Requirements are living documents. Update them as understanding improves.
