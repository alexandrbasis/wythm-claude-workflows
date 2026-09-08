# `/nf` — Deep-Dive Interview Guide

Question bank for **Step 3** of the `nf` skill. Drive the interview toward the sections of
`.claude/docs/templates/discovery-template.md`. Ask the **non-obvious** questions below until
each template section can be filled clearly and read as a standalone entry point. Use only the
subsets that add clarity — skip what doesn't apply.

## Feature Overview / Why This Exists
- What is the feature in plain language?
- What problem or opportunity does it address?
- Why does it matter now?
- What value should it create for the user or product?

## Usage Context (only if it adds clarity)
- Who is the primary user or actor?
- When does this feature matter?
- What surrounding context, prior state, or constraints affect usage?

## Chosen Direction (only if multiple viable approaches exist)
- What direction was selected?
- What alternatives were considered?
- Why is this direction preferred?

## How It Works
- Entry points
- Main happy path
- Key states (loading, empty, error, success, variants)
- Important edge cases that materially shape the feature

## Scope Boundaries
- What is explicitly in scope for this version?
- What is explicitly out of scope?
- Where could the scope accidentally expand?

## Key Requirements / Constraints
- Must-have behaviors
- Integration points and dependencies
- Security, accessibility, performance, privacy, or platform limitations that materially shape the feature
- Assumptions the downstream implementation must preserve

## Post-Action & Cross-Surface Behavior
Use the subset that applies.

**Any workflow with a submit / confirm action** (create, update, delete, toggle, selection-apply):
- After success, what exactly should the user see?
- Which screen is the canonical place to confirm the result?
- If the current screen doesn't show the result, what success feedback appears?

**Any feature that renders lists, search results, dashboards, or categorized views:**
- Where else does this entity appear? What metadata governs how it appears there?

**Any feature with user input or selection** (including read-only filters):
- For every validation rule, what's the UI affordance (error, disabled option, hint, highlighted field)?
- For invalid input, does feedback appear before or after submission?
- Are there options that should be hidden or visually distinguished based on context?
