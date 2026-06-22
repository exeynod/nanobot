You have TWO equally important tasks:
1. Extract new facts from conversation history
2. Deduplicate existing memory files — find and flag redundant, overlapping, or stale content even if NOT mentioned in history

For EACH candidate fact, classify it against the existing memory files, then output the matching line:
- ADD → [FILE] atomic fact (genuinely new, not already present)
- UPDATE → [FILE-UPDATE] old: <existing text being superseded> | new: <corrected/updated fact>
- DELETE → [FILE-REMOVE] reason for removal (stale, resolved, contradicted by newer info)
- NOOP → emit nothing (already captured accurately — do not restate it)

[SKILL] kebab-case-name: one-line description of the reusable pattern

Prefer UPDATE over REMOVE+ADD when a fact supersedes an existing one — it keeps memory coherent instead of churning near-duplicates. A changed value (weight, status, preference, resolved issue) is an UPDATE of the old line, not a second ADD.

Timestamps: when adding or updating a MEMORY.md fact, prefix it with the current date in brackets, e.g. "[2026-01-15] ...", using the "Current Date" given in the context below — never invent a date. SOUL.md and USER.md are NOT timestamped.

Files: USER (identity, preferences), SOUL (bot behavior, tone), MEMORY (knowledge, project context)

Rules:
- Atomic facts: "has a cat named Luna" not "discussed pet care"
- Corrections: [USER] location is Tokyo, not Osaka
- Capture confirmed approaches the user validated

Deduplication — scan ALL memory files for these redundancy patterns:
- Same fact stated in multiple places (e.g., "communicates in Chinese" in both USER.md and multiple MEMORY.md entries)
- Overlapping or nested sections covering the same topic
- Information in MEMORY.md that is already captured in USER.md or SOUL.md (MEMORY.md should not duplicate permanent-file content)
- Verbose entries that can be condensed without losing information
For each duplicate found, output [FILE-REMOVE] for the less authoritative copy (prefer keeping facts in their canonical location)

Staleness — MEMORY.md lines may have a ``← Nd`` suffix showing days since last modification:
- SOUL.md and USER.md have no age annotations — they are permanent, only update with corrections
- Age only indicates when content was last touched, not whether it should be removed
- Use content judgment: user habits/preferences/personality traits are permanent regardless of age
- Only prune content that is objectively outdated: passed events, resolved tracking, superseded approaches
- Lines with ``← Nd`` (N>{{ stale_threshold_days }}) deserve closer review but are NOT automatically removable
- When removing: prefer deleting individual items over entire sections

Skill discovery — flag [SKILL] when ALL of these are true:
- A specific, repeatable workflow appeared 2+ times in the conversation history
- It involves clear steps (not vague preferences like "likes concise answers")
- It is substantial enough to warrant its own instruction set (not trivial like "read a file")
- Do not worry about duplicates — the next phase will check against existing skills

Do not add: current weather, transient status, temporary errors, conversational filler.

[SKIP] if nothing needs updating.
