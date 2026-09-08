# LLM Mental Model: Where AI is Strong vs Brittle

> Reference for all agents and skills. Consult when designing verification gates or delegating work to AI agents.

## Where LLMs Excel (High Confidence Zones)

| Task | Why It Works | Example |
|------|-------------|---------|
| Pattern-based code generation | Matches training distribution | Generate a React component from a template |
| Boilerplate & scaffolding | Repetitive, well-defined | DTO, mapper, factory, test skeleton |
| Code review (pattern matching) | Spot known anti-patterns | Missing error handling, hardcoded values |
| Refactoring (local scope) | Clear input→output transformation | Extract function, rename, inline |
| Test generation from spec | Given/When/Then maps to code | Unit tests from acceptance criteria |
| Documentation from code | Summarization is a core strength | JSDoc, README, ADR drafts |
| Translation & i18n | Pattern substitution | key→translation mapping |

## Where LLMs Are Brittle (Guard Rail Zones)

| Task | Why It Fails | Mitigation |
|------|-------------|------------|
| **Counting & completeness** | Transformers don't count reliably; 11 fields become 4 | Use numbered VC-checklist; programmatic count verification |
| **Long enumerated lists** | Attention drift over long contexts | Break into batches of 5-7; explicit numbering |
| **Visual verification** | No actual visual processing of rendered UI | Require screenshot comparison or visual regression test |
| **Exact value reproduction** | Approximates instead of copying exactly | Always copy-paste from source; never "remember" hex values |
| **Spec adherence over long tasks** | Context window fills, early spec details get compressed | Re-read spec before each step; structured handoff artifacts |
| **Negation & constraint following** | "Don't use X" is weaker than "Use Y" | Frame rules positively: "Always use useThemeColors()" not "Don't hardcode colors" |
| **Multi-step reasoning chains** | Error compounds across steps | Break into atomic steps; verify after each |
| **State tracking across turns** | Loses track of what's done vs pending | Persist state to task document; re-read before continuing |

## Operational Rules (Derived from Incidents)

### Rule 1: Never Trust Agent Self-Report on Completeness
**Incident**: Employment Info — agent marked 4/11 fields as complete, checked all task doc boxes.
**Rule**: After implementation, run programmatic count: `grep -c 'VC-' task-doc | compare to implemented count`. Agent self-assessment is unreliable for "did I cover everything?"

### Rule 2: Re-Read Spec Before Every Implementation Step
**Incident**: Agent started with full context but by step 3, had "forgotten" half the requirements.
**Rule**: At the start of each step, explicitly re-read the relevant VC entries from the task document. Don't rely on context from 500+ lines ago.

### Rule 3: Don't Let Agent Choose "Simpler" Alternative
**Incident**: Agent deleted a failing feature path instead of fixing the underlying dependency/config that broke it.
**Rule**: When implementation fails, agent MUST diagnose root cause before changing approach. "Simplify by removing" is never acceptable without user approval.

### Rule 4: Visual Properties Must Come from Source, Not Memory
**Incident**: Agent guessed hex colors, layout direction, spacing instead of reading the design source.
**Rule**: Every visual property must be read from the design source (design-tool MCP or design tokens). Agent MUST NOT generate any visual value from "knowledge" — only from explicit source data.

### Rule 5: Test Assertions Must Be Exact
**Incident**: Tests asserted `options.length > 0` instead of `options.length === 28`.
**Rule**: Tests must assert exact expected values. `> 0` is never acceptable for enumerated data. The VC-checklist provides the exact counts.

### Rule 6: Don't Parallelize What Requires Sequential Verification
**Incident**: Multiple agents edited shared state, each claiming their version was correct.
**Rule**: If two tasks touch the same file or depend on each other's output, execute sequentially. Parallel-safe = different files, different modules, no shared state.

## How to Apply This Document

### In /ct (Create Task)
- Use relevant verification recipes when planning brittle requirements.
- Keep their checks in the task's existing plan; a separate VC checklist is optional.

### In /si (Start Implementation)
- Verify the current slice against its acceptance and record observed evidence in the task.
- Confirm every required outcome before completion; checkbox counts alone are not proof.

### In /sr (Start Review)
- spec-compliance-reviewer reads this doc to know WHERE to be extra skeptical
- Extra scrutiny on: field counts, option lists, visual properties, long enumerations

### For All Agents
- If you're about to do something in a "brittle zone", add a verification step
- If you catch yourself approximating instead of reading source, STOP and read
- When in doubt, ask the user rather than guess
