---
allowed-tools: Read, Write, Edit, Grep, Glob
argument-hint: [feature-name] | --template | --interactive
description: Create Jobs-to-be-Done (JTBD) analysis for product features
---

# Create Jobs-to-be-Done Document

You are an experienced Product Manager. Create a Jobs to be Done (JTBD) document for a feature: **$ARGUMENTS**

**IMPORTANT:**
- Focus on user needs and jobs, not technical implementation
- Do not include any time estimates
- JTBD analysis informs business requirements

## Required Context

**Read before starting:**
1. **Product Vision**: @docs/product-docs/PRD/PRD_Wythm.md
2. **Project Structure**: @CLAUDE.md

## Task

Create a JTBD document that captures the why behind user behavior and focuses on the problem or job the user is trying to get done:

1. **Create task directory** (if it doesn't exist):
   - Directory name: `tasks/task-YYYY-MM-DD-[feature-name]/`
   - Use current date in YYYY-MM-DD format
   - Use kebab-case for feature name
   - This directory will be used by subsequent commands (`/cprd`, `/ct`, `/si`)

2. **Use the JTBD template** from `@docs/product-docs/templates/JTBD-template.md`

3. **Create JTBD document** that includes:
   - Job statements following "When [situation], I want [motivation], so I can [expected outcome]"
   - User needs and pain points analysis
   - Desired outcomes from user perspective
   - Competitive analysis through JTBD lens
   - Market opportunity assessment

4. **Output location**: `tasks/task-YYYY-MM-DD-[feature-name]/JTBD-[feature-name].md`

Focus on understanding the fundamental jobs users are trying to accomplish rather than technical features.