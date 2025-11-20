---
allowed-tools: Bash(gh pr comment:*),Bash(gh pr diff:*),Bash(gh pr view:*)
description: Review a pull request using specialized agents and document findings
---

Perform a comprehensive code review using subagents for key areas:

- code-quality-reviewer
- performance-reviewer
- test-coverage-reviewer
- documentation-accuracy-reviewer
- security-code-reviewer

Instruct each to only provide noteworthy feedback. Once they finish, review the feedback and post only the feedback that you also deem noteworthy.

**After collecting all agent feedback**, create `Advanced Code Review - [Task Title].md` in task directory documenting findings from each agent:

```markdown
# Advanced Code Review - [Task Title]

**Date**: [Current Date] | **Review Type**: Multi-Agent Advanced Review
**Task**: `[path]` | **PR**: [URL] | **Status**: ✅ APPROVED / ❌ NEEDS FIXES / 🔄 NEEDS DISCUSSION

## Review Summary
[2-3 sentences synthesizing findings across all agents]

---

## Agent Findings

### 🏗️ Code Quality Review
**Agent**: code-quality-reviewer
**Status**: ✅ Excellent / 🔄 Good / ❌ Needs Improvement

#### Key Findings:
[Summary of code quality agent's findings]

#### Issues Identified:
- [ ] **[Issue]**: [Description] → [Impact] → [Solution]
- [ ] **[Issue]**: [Description] → [Impact] → [Solution]

---

### ⚡ Performance Review
**Agent**: performance-reviewer
**Status**: ✅ Excellent / 🔄 Good / ❌ Needs Improvement

#### Key Findings:
[Summary of performance agent's findings]

#### Issues Identified:
- [ ] **[Issue]**: [Description] → [Impact] → [Solution]
- [ ] **[Issue]**: [Description] → [Impact] → [Solution]

---

### ✅ Test Coverage Review
**Agent**: test-coverage-reviewer
**Status**: ✅ Excellent / 🔄 Good / ❌ Needs Improvement

#### Key Findings:
[Summary of test coverage agent's findings]

#### Issues Identified:
- [ ] **[Issue]**: [Description] → [Impact] → [Solution]
- [ ] **[Issue]**: [Description] → [Impact] → [Solution]

---

### 📚 Documentation Review
**Agent**: documentation-accuracy-reviewer
**Status**: ✅ Excellent / 🔄 Good / ❌ Needs Improvement

#### Key Findings:
[Summary of documentation agent's findings]

#### Issues Identified:
- [ ] **[Issue]**: [Description] → [Impact] → [Solution]
- [ ] **[Issue]**: [Description] → [Impact] → [Solution]

---

### 🔒 Security Review
**Agent**: security-code-reviewer
**Status**: ✅ Excellent / 🔄 Good / ❌ Needs Improvement

#### Key Findings:
[Summary of security agent's findings]

#### Issues Identified:
- [ ] **[Issue]**: [Description] → [Impact] → [Solution]
- [ ] **[Issue]**: [Description] → [Impact] → [Solution]

---

## Consolidated Issues Checklist

### 🚨 Critical (Must Fix Before Merge)
[All critical issues from all agents consolidated]
- [ ] **[Agent] - [Issue]**: [Description] → [Impact] → [Solution] → [Files] → [Verification]

### ⚠️ Major (Should Fix)
[All major issues from all agents consolidated]
- [ ] **[Agent] - [Issue]**: [Description] → [Impact] → [Solution] → [Files]

### 💡 Minor (Nice to Fix)
[All minor issues from all agents consolidated]
- [ ] **[Agent] - [Issue]**: [Description] → [Benefit] → [Solution]

---

## Requirements Compliance

### ✅ Completed
- [x] [Requirement] - [quality note from relevant agent]

### ❌ Missing/Incomplete
- [ ] [Missing requirement with explanation]

---

## Overall Quality Assessment

**Code Quality**: [Rating from code-quality-reviewer]
**Performance**: [Rating from performance-reviewer]
**Test Coverage**: [Rating from test-coverage-reviewer]
**Documentation**: [Rating from documentation-accuracy-reviewer]
**Security**: [Rating from security-code-reviewer]

**Overall Assessment**: ✅ Excellent / 🔄 Good / ❌ Needs Improvement

---

## Recommendations

### Immediate Actions (Before Merge)
1. [Critical/major fixes needed - prioritized]
2. [Critical/major fixes needed - prioritized]

### Future Improvements (Post-Merge)
1. [Architectural or optimization suggestions]
2. [Technical debt to address]

---

## Final Decision

**Status**: ✅ APPROVED FOR MERGE / ❌ NEEDS FIXES / 🔄 NEEDS DISCUSSION

**Criteria Met**:
- [ ] All critical issues resolved
- [ ] Code quality standards met across all dimensions
- [ ] Performance acceptable
- [ ] Test coverage adequate
- [ ] Documentation complete
- [ ] No security vulnerabilities

**Decision Rationale**: [Explain the decision based on aggregated agent feedback]

---

## Developer Instructions

### To Address Issues:
1. **Review findings by agent** above
2. **Prioritize critical issues** from consolidated checklist
3. **Mark fixed items** with `[x]` as you complete them
4. **Update task document** with fix details
5. **Test thoroughly** after each fix
6. **Request re-review** when all critical and major issues resolved

### Re-Review Process:
1. Complete all critical fixes, most major fixes
2. Update changelogs in task document
3. Ensure tests pass
4. Notify for re-review

```
---
