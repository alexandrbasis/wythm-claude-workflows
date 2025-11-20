---
allowed-tools: Read, Write, Edit, Grep, Glob
argument-hint: [feature-name] | --template | --interactive
description: Create Product Requirements Document (PRD) for new features
---

# Create Product Requirements Document

You are an experienced Product Manager. Create a Product Requirements Document (PRD) for a feature: **$ARGUMENTS**

**IMPORTANT:**
- Focus on feature and user needs, not technical implementation
- Do not include any time estimates
- PRD informs business requirements creation for future tasks

## Required Context

**Read before starting:**
1. **Product Vision**: @product-docs/PRD/PRD_Wythm.md
2. **Project Structure**: @CLAUDE.md
3. **Existing PRDs**: Check `product-docs/PRD/` for related documents

## Task

Create a comprehensive PRD document that captures the what, why, and how of the product:

1. **Check existing PRDs**: Review `product-docs/PRD/` to ensure consistency and avoid duplication

2. **Use the PRD template** from `@product-docs/templates/PRD-template.md`

3. **Create PRD document** that defines:
   - Problem statement and user needs
   - Feature specifications and scope
   - Success metrics and acceptance criteria
   - User experience requirements
   - Technical considerations (high-level only)

4. **Output location**: `product-docs/PRD/PRD-[feature-name].md`
   - Use kebab-case for feature name
   - Name should be descriptive and reflect the feature domain
   - Example: `PRD-vocabulary-learning.md`, `PRD-user-onboarding.md`

Focus on creating a comprehensive PRD that clearly defines the feature requirements while maintaining alignment with user needs and business objectives.