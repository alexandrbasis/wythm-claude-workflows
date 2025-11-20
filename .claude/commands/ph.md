# Prepare Handover Command

## PRIMARY OBJECTIVE
You need to **STOP** current implementation and prepare task-document for next developer to continue implementation from you've stopped. IMPORTANT: Think hard

## PURPOSE
Ensure task document is updated with all progress, then add minimal handover context.

## WORKFLOW

### **STEP 1: Stop and Update**

1. **STOP work**: "Which task? What completed since last update?"

2. **Update task document**:
   - Mark completed steps with [x] and timestamps
   - Add changelog entries for recent work
   - Update status and progress
   - Commit working code, stash partial work

### **STEP 2: Add Handover**

Add handover section (only if needed):

```markdown
## 🔄 Implementation Handover
**Date**: [Current Date]  
**Stopping Point**: [Where work stopped]  
**Next Step**: [What next developer should do]
**Context**: [Any blockers or critical info not in task]
```

### **STEP 3: Update Linear**

Post handover comment using linear-task-manager agent:
```
Add handover comment to Linear issue

Task directory: [absolute path to task folder]
Issue ID: [Linear issue ID from task document]

Comment content:
🔄 Implementation handover prepared

**Date**: [timestamp]
**Progress**: [summary]
**Stopping Point**: [where stopped]
**Next Step**: [what to do next]

Task ready for continuation.
```

**Integration**: Use `Task` tool with `linear-task-manager` agent type

## Workflow Feedback Collection

### Step 4: Collect Workflow Feedback
```
After completing handover preparation, engage the workflow-feedback-collector agent to gather improvement insights about instruction clarity, process efficiency, and missing guidance that could benefit future developers.
```

**Agent Trigger**: Use workflow-feedback-collector agent
**Focus Areas**:
- Completeness of handover documentation templates
- Effectiveness of context preservation instructions
- Clarity of continuation guidelines for next developer
- Missing information that would improve handover quality
- Process efficiency for context switching scenarios
**Documentation**: All feedback automatically logged to docs/development/dev-wf-feedback.md