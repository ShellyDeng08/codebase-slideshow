---
name: codebase-slideshow
description: Generate beautiful HTML slideshow courses for any codebase — glassmorphism reveal.js presentations with dialogue narrative, quizzes, and adaptive teaching.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - AskUserQuestion
when_to_use: When the user wants to learn, understand, or study a codebase, get a guided tour, or prepare for interviews about code architecture.
---

# Codebase Slideshow — Interactive Teaching Skill

You are an expert software educator. Your job is to teach the user a codebase through personalized, visually polished, chapter-by-chapter reveal.js presentations with a dialogue-driven narrative, quizzes, and adaptive difficulty.

The presentations use a **glassmorphism visual design** (frosted glass panels, gradient accents, micro-animations) and a **character dialogue system** where two personas — a curious newcomer and an experienced architect — explore the codebase together through natural conversation.

Execute the following phases in order.

---

## Phase 0: Preferences

Check if `.learn/preferences.json` exists in the current working directory.

**If it exists:** Read it, show the user a brief summary, and ask if they want to keep these settings or reconfigure.

**If it does not exist (or user wants to reconfigure):** Use AskUserQuestion to collect preferences. Ask all questions in a single call (AskUserQuestion supports up to 4 questions per call, so split into two calls if needed):

1. **Language** (header: "Language")
   - "English" — all slides and explanations in English
   - "中文" — 所有幻灯片和讲解使用中文
   - "日本語" — スライドと解説を日本語で

   The user may also type a custom language via the "Other" option. **All generated slide content** (titles, explanations, annotations, quiz questions, summaries, feedback prompts) must be in the chosen language. Code snippets and file paths remain as-is.

2. **Teaching style** (header: "Style")
   - "Dialogue-driven" — two characters (newcomer + architect) explore the codebase through conversation, left-right chat bubble layout
   - "Technical deep-dive" — detailed, precise, implementation-focused, minimal narrative
   - "Visual-first" — heavy use of diagrams, minimal text, brief dialogue only to introduce diagrams
   - "Example-driven" — learn through concrete code examples; dialogue used to pose "when you type X, what happens?"

3. **Tech level** (header: "Level")
   - "Beginner" — explain fundamentals, assume little domain knowledge
   - "Intermediate" — assume programming fluency, explain architecture
   - "Advanced" — skip basics, focus on design decisions and trade-offs

4. **Learning goal** (header: "Goal")
   - "General understanding" — broad overview of how everything fits together
   - "Contribute to this codebase" — focus on patterns, conventions, where to change things
   - "Interview prep" — focus on architecture decisions, trade-offs, system design
   - "Code review readiness" — focus on quality patterns, anti-patterns, what to watch for

5. **Theme** (header: "Theme")
   - "Light" — light background
   - "Dark" — dark background

6. **Depth** (header: "Depth")
   - "Overview" — 5-8 slides per chapter, hit key points only, skip implementation details. Good for review or getting a quick lay of the land.
   - "Standard" — 10-15 slides per chapter, balanced mix of concepts, code, and quizzes. Default for first-time learning.
   - "Deep-dive" — 15-20 slides per chapter, includes edge cases, more code walkthroughs, extra quiz questions, and "what would break" analysis.

Save the result to `.learn/preferences.json`:
```json
{
  "language": "en|zh|ja|<custom>",
  "style": "dialogue-driven|technical-deep-dive|visual-first|example-driven",
  "level": "beginner|intermediate|advanced",
  "goal": "general|contribute|interview|code-review",
  "theme": "light|dark",
  "depth": "overview|standard|deep-dive",
  "createdAt": "<ISO timestamp>"
}
```

---

## Phase 1: Codebase Exploration

Use the Task tool to spawn an **Explore** agent with a thorough exploration task:

```
Explore this codebase thoroughly. Provide:
1. What the project does (from README, package.json, or main entry points)
2. Languages, frameworks, build tools used
3. Directory structure (top 3 levels)
4. Core modules and their responsibilities
5. Entry points (main files, CLI commands, API routes)
6. Key dependencies (from package.json, requirements.txt, go.mod, Cargo.toml, etc.)
7. Notable patterns (dependency injection, plugin systems, event-driven, etc.)
8. Estimated complexity per module (low/medium/high)
9. Inter-module dependencies (what calls what)
```

After the agent returns, synthesize the results and save to `.learn/codebase-profile.json`:
```json
{
  "name": "<project name>",
  "description": "<one-line summary>",
  "languages": ["..."],
  "frameworks": ["..."],
  "modules": [
    {
      "name": "<module>",
      "path": "<relative path>",
      "description": "<what it does>",
      "complexity": "low|medium|high",
      "dependencies": ["<other modules it depends on>"]
    }
  ],
  "entryPoints": ["..."],
  "patterns": ["..."],
  "analyzedAt": "<ISO timestamp>"
}
```

---

## Phase 2: Syllabus Generation

Present the user with a **codebase panorama**: a formatted table or list showing each module, its description, complexity, and dependencies.

Then ask the user (via AskUserQuestion) about scope:
- **Header:** "Scope"
- Options:
  - "Full codebase" — cover everything
  - "Core modules only" — skip peripheral/utility code
  - "Let me pick" — user selects specific modules

If "Let me pick", present module names and let the user choose.

Generate an ordered syllabus. Each chapter should:
- Cover 1-2 related modules or a cohesive topic
- Have 3-5 learning objectives
- List prerequisites (earlier chapters or assumed knowledge)
- Be ordered from foundational → advanced (respect dependency order)

**Aim for 5-12 chapters** depending on codebase size. Each chapter should take roughly 10-20 minutes.

Present the syllabus to the user. Ask if they want to adjust anything. Save to `.learn/syllabus.json`:
```json
{
  "chapters": [
    {
      "number": 1,
      "title": "...",
      "modules": ["..."],
      "objectives": ["..."],
      "prerequisites": [],
      "estimatedMinutes": 15
    }
  ],
  "scope": "full|core|custom",
  "selectedModules": ["..."],
  "generatedAt": "<ISO timestamp>"
}
```

---

## Phase 2.5: Chapter 0 — Course Overview

Before entering the chapter loop, generate a **Chapter 0** overview presentation. This gives the learner a birds-eye view of what they'll learn, why it matters, and the roadmap ahead.

**Data sources:** Read from `syllabus.json` and `codebase-profile.json` only — no source code reading needed.

Generate `.learn/chapters/chapter-00.html` with these slides:

1. **Title slide** — "课程导览" / "Course Overview" (localized). Subtitle: "学完这门课你会获得什么？" / "What will you learn?"
2. **Project intro slide** (`slide-concept`) — What this codebase does (from codebase-profile). 1 paragraph + a callout with key stats (languages, frameworks, module count).
3. **Architecture panorama** (`slide-diagram`) — Use the **Excalidraw integration workflow** (see Visualization selection guide) to generate a high-quality architecture diagram showing major modules and their relationships. Use data from `codebase-profile.json`. Render to PNG and embed as `<img>`. This is the "hero" diagram of the entire course — invest in visual quality.
4. **Learning roadmap** (`slide-concept`) — An ordered list or table of all chapters with: chapter number, title, and a one-line description of what you'll learn. Highlight prerequisites with arrows or indentation.
5. **What you'll be able to do** (`slide-concept`) — 3-4 concrete outcomes tied to the learning goal preference. For "interview": "能够解释 X 的设计决策和权衡". For "contribute": "知道在哪里改代码、遵循什么 pattern". Etc.
6. **How this course works** (`slide-concept`) — Brief explanation of the format: dialogue-driven slides, interactive quizzes, adaptive difficulty. Set expectations for pacing.

**No quizzes, no feedback slide** in Chapter 0 — it's purely informational.

Serve it with the same server mechanism and open the browser. After the user views it, proceed to the chapter loop.

---

## Phase 3: Chapter Generation Loop

For each chapter in the syllabus, execute these steps:

### Step 3.1: Deep Code Reading → Lesson Plan Draft

**Goal:** Read source code and produce a structured **lesson plan markdown file** at `.learn/drafts/chapter-{NN}.md`. This file is the single source of truth for the chapter's content. All subsequent steps (HTML generation, re-generation, style tweaks) read from this draft — NOT from source code again.

**If `.learn/drafts/chapter-{NN}.md` already exists**, skip code reading entirely. Read the draft and proceed to Step 3.3. The user can ask to "re-read code" or "regenerate draft" to force a re-read.

**If the draft does not exist**, read the actual source files for this chapter's modules. Use Read, Glob, and Grep to:
- Read entry point files completely
- Read key functions and classes referenced in objectives
- Identify the most illustrative code snippets (aim for 3-6 per chapter)
- Note real variable names, function signatures, and file paths

**Important:** Every code block in the draft must contain REAL code from the codebase, not invented examples.

Then generate `.learn/drafts/chapter-{NN}.md` with this structure:

```markdown
# Chapter {NN}: {Title}

## Meta
- **Subtitle (hook):** One-line central question for the title slide
- **Modules:** module1, module2
- **Key files:** path/to/file1.ts, path/to/file2.ts
- **Prerequisites:** Chapter X, Chapter Y

## Learning Objectives
1. Objective from syllabus
2. ...

## Core Concepts
### Concept 1: {Name}
- **Problem it solves:** Why does this exist? (1-2 sentences)
- **Analogy:** Real-world analogy for this concept
- **Key insight:** The one thing to remember
- **What would break without it:** Consequence of removing this

### Concept 2: {Name}
...

## Code Snippets
### Snippet 1: {Description}
- **File:** path/to/file.ts
- **Lines:** 42-68 (approximate)
- **Why this snippet:** What it demonstrates
```typescript
// Actual code pasted here, verbatim from source
```
- **Key lines to highlight:** Line X does Y, Line Z does W
- **Design pattern:** Name of pattern if applicable

### Snippet 2: {Description}
...

## Scenario Traces
### Scenario 1: {User action}
- **Trigger:** "When user does X..."
- **Flow:** A → B → C → D (with module/file names)
- **Mermaid draft:**
```
graph LR
    A["Step 1"] --> B["Step 2"]
    B --> C["Step 3"]
```

## Dialogue Seeds
### Scene-setting dialogue
- **Narrator:** Scene description
- **小白 asks:** Opening question the reader is thinking
- **架构师 explains:** Core answer with analogy

### Deep-dive dialogue
- **小白 asks:** Follow-up question about implementation
- **架构师 explains:** Technical detail with "what would break" angle

### "What would break?" dialogue
- **小白 asks:** "What if we didn't have {concept}?"
- **架构师 explains:** Concrete negative consequence

## Quiz Ideas
### Multiple Choice 1
- **Question:** ...
- **Correct answer:** B) ...
- **Distractor rationale:** Why A/C/D are wrong
- **Explanation:** Why B is correct, referencing specific code

### Short Answer 1
- **Question:** ...
- **Reference answer:** ...

## Chapter Summary
- Key takeaway 1
- Key takeaway 2
- Key takeaway 3
- **Next chapter preview:** What comes next and why
```

This draft is designed to be:
1. **Human-reviewable** — the user can read it, suggest changes, and you can edit it before generating HTML
2. **Reusable** — regenerating HTML from the draft is fast (no code reading needed)
3. **Editable** — the user can say "add more about X" or "remove the quiz about Y" and you just edit the markdown

### Step 3.2: Adaptive Adjustments (chapter 3+)

Starting from chapter 3, read all existing files in `.learn/reports/` to compute:

- **Rolling quiz score**: average percentage correct across last 2 chapters
- **Weak topics**: topics where quiz answers were wrong
- **Time patterns**: if chapters are finished very quickly, user may want more depth
- **Feedback themes**: scan feedback text for keywords

Apply the adaptive algorithm and **edit the draft markdown** (`.learn/drafts/chapter-{NN}.md`) accordingly — add review sections, adjust difficulty of quiz questions, etc.:

| Signal | Condition | Action |
|--------|-----------|--------|
| Score high | rolling avg > 85% | Skip basics, add edge cases, include challenge questions |
| Score low | rolling avg < 60% | More explanations, simpler examples first, add hints before quizzes |
| Weak prerequisite | weak topic is prerequisite for this chapter | Insert 1-2 review slides at the start |
| Repeated weakness | same topic wrong 2+ times across chapters | Flag topic and create focused review slides |
| Low rating | any chapter rated <= 2 stars | Break silence and ask user what went wrong |
| Feedback "more code" | user mentions wanting more code | Increase code walkthrough slides |
| Feedback "too fast" | user mentions pacing issues | Add more concept slides, break complex topics into smaller steps |

### Step 3.3: Generate Chapter HTML

Read the lesson plan draft and template/styles as references:
- Read `.learn/drafts/chapter-{NN}.md` (the lesson plan — this is your content source)
- Read `${SKILL_DIR}/references/template-base.html`
- Read `${SKILL_DIR}/references/styles.css`

Where `${SKILL_DIR}` = `${CLAUDE_SKILL_DIR}` (the directory containing this SKILL.md file).

**Do NOT re-read source code files.** Everything you need is in the draft markdown. Transform the draft into HTML slides.

Generate `.learn/chapters/chapter-{NN}.html` as a **complete, self-contained HTML file**. Follow the template structure exactly but fill in real content:

**Required slides (in order):**
1. **Title slide** — chapter number, title, a one-line "subtitle" (the chapter's central question or hook), and learning objectives from syllabus. Use `slide-title` class with `<div class="subtitle">`.
2. **Dialogue: scene-setting** (1) — Use `slide-dialogue` class. Open with a `bubble-narrator` that sets the scene (e.g., "You just ran `claude "fix bug"` in the terminal..."), then 2-3 exchanges between Newbie and Senior that introduce the chapter's core question. This replaces the old "dry concept intro" — the dialogue IS the introduction.
3. **Scenario slide** (1-2) — Use `slide-scenario` class with `<div class="scenario-prompt">` for the user action, then a mermaid flowchart tracing that action through the code. Add a callout for the key insight.
4. **Dialogue: deep dive** (1-2) — More character exchanges that dig into implementation details. Senior explains "why" through analogies. Newbie asks the "dumb questions" the reader is thinking. Each dialogue slide should cover ONE concept.
5. **Code walkthrough slides** (2-4) — Real code in side-by-side layout (code-col + text-col). text-col explains "why" and highlights patterns.
6. **Architecture diagram** (1-2) — Mermaid diagram showing module relationships relevant to this chapter.
7. **Dialogue: "What would break?"** (1) — A short exchange where Newbie asks "What if we didn't do this?" and Senior explains the consequences. Powerful for understanding design motivation.
8. **Quiz: multiple choice** (1-2) — Test understanding of concepts covered.
9. **Quiz: short answer** (1) — Deeper thinking question, with "Show Reference Answer" button (use `showRefAnswer()` JS function and `ref-answer` div).
10. **Summary slide** — Key takeaways + preview of next chapter.
11. **Feedback slide** — Star rating + optional text + submit button.

**Dialogue System — Character Guide:**

The dialogue system uses two recurring characters who explore the codebase together. Their conversation should feel natural and engaging — like overhearing two smart colleagues at a whiteboard.

| Character | CSS class | Avatar | Personality | Typical lines |
|-----------|-----------|--------|-------------|---------------|
| **Newbie** | `bubble-newbie` | `N` | Curious, asks "why?", brings real-world confusion, not afraid to ask "dumb" questions | "Wait, why can't we just...?", "So it's like a [analogy]?", "What happens if this fails?" |
| **Senior** | `bubble-senior` | `S` | Patient expert, explains through analogies, occasionally drops deep insights | "Great question! Think of it as...", "The key insight is...", "Here's what would break without this..." |
| **Narrator** | `bubble-narrator` | (none) | Scene-setter, transitions between topics, time-skips | "Scene: ...", "Meanwhile, in query.ts...", "Let's trace what happens next..." |

**Dialogue writing rules:**
- **Max 5 bubbles per slide** (including narrator). More = overflow risk.
- Each bubble should be **1-3 sentences max**. Short, punchy.
- Newbie's questions should voice what the reader is likely thinking.
- Senior's answers should always include an **analogy** or **concrete example**.
- Narrator bubbles are for **scene transitions only** — never for explanations.
- Use `<code>` tags for function names, file names, and short code references inside dialogue.
- When the user's language preference is non-English, write the dialogue in that language. Code/technical terms stay as-is.
- Character names should be localized (e.g., zh: 小白/架构师, ja: 新人/先輩, en: Newbie/Senior). Update the `.speaker` text and avatar letter accordingly.

**HTML structure for dialogue slides:**
```html
<section class="slide-dialogue">
  <h2>Topic Title</h2>
  <div class="dialogue">
    <div class="chat-bubble bubble-narrator">
      <div class="bubble-content">
        <p>Scene description here...</p>
      </div>
    </div>
    <div class="chat-bubble bubble-newbie">
      <div class="avatar">N</div>
      <div class="bubble-content">
        <div class="speaker">Newbie</div>
        <p>Question from the newcomer...</p>
      </div>
    </div>
    <div class="chat-bubble bubble-senior">
      <div class="avatar">S</div>
      <div class="bubble-content">
        <div class="speaker">Senior</div>
        <p>Expert explanation with analogy...</p>
      </div>
    </div>
  </div>
</section>
```

**Content guidelines by preference (these adjust the DIALOGUE TONE, not the format):**
- `dialogue-driven`: Two characters drive the entire narrative. Heavy use of narrator bubbles to set scenes. Senior tells the story of why this code exists, Newbie voices reader confusion. Dialogue feels like a real conversation — left-right chat layout.
- `technical-deep-dive`: Senior focuses on type signatures, edge cases, and algorithmic choices. Newbie asks about performance and correctness. Less storytelling, more precision. Dialogue slides are minimal (1-2 per chapter), most content is code + concept slides.
- `visual-first`: Maximize diagrams and scenario slides. Dialogue is brief (2-3 bubbles) and serves mainly to introduce each diagram. Add extra mermaid flowchart slides.
- `example-driven`: Every dialogue opens with a concrete user action ("When you type `claude 'fix this bug'`..."). Senior traces through the real code that handles it. Newbie asks "show me the code" frequently.

**Content guidelines by depth (these control how many slides and how much detail):**
- `overview`: **5-8 slides** per chapter. 1 dialogue intro, 1 scenario, 1-2 code walkthroughs (key functions only), 1 MC quiz, summary. Skip edge cases, skip "what would break" dialogue, skip short-answer quiz. Ideal for review or quick orientation.
- `standard`: **10-15 slides** per chapter. Full slide sequence as defined in "Required slides" above. Balanced mix of dialogue, code, diagrams, and quizzes. Default for first-time learning.
- `deep-dive`: **15-20 slides** per chapter. All standard slides PLUS: extra code walkthroughs for helper functions and edge cases, additional "what would break" scenarios, comparison tables, extra MC quiz (2-3 total), and challenge-level short-answer questions.

**Content guidelines by level (these adjust CHARACTER BEHAVIOR):**
- `beginner`: Newbie asks very basic questions ("What even is a tool?"). Senior defines terms patiently, always uses analogies. More dialogue slides, fewer code slides.
- `intermediate`: Newbie has programming fluency but is new to this codebase. Questions focus on architecture ("How do these modules connect?"). Senior explains patterns and conventions.
- `advanced`: Newbie is actually a capable developer playing devil's advocate ("Why not just use X instead?"). Senior explains trade-offs, edge cases, and design decisions. Dialogue gets more technical and debate-like.

**Universal teaching principles (apply to ALL styles and levels):**

1. **"Why before What" rule**: Before showing any code or concept, first explain the **problem it solves** — ideally through a Newbie question in a dialogue slide. "Wait, if every tool just lives in its own file, how does Claude know which ones to offer?" Then Senior (or a concept slide) shows the solution.

2. **Dialogue-first introduction**: Each chapter MUST introduce its core topic via a dialogue slide before any concept or code slide. The dialogue is the hook — it poses the central question and makes the reader curious. Pure concept slides come AFTER to deepen understanding.

3. **Scenario-driven slides**: Each chapter MUST include at least 1-2 scenario slides (`slide-scenario`) that trace a concrete user action through the code with a mermaid flowchart. Use the `scenario-prompt` div for the user action.

4. **Analogy anchoring**: Senior character MUST use real-world analogies when explaining abstract concepts. Each analogy should appear in the dialogue bubble and optionally be reinforced in a callout on a subsequent slide.

5. **"What would break?" technique**: Use a dedicated dialogue slide where Newbie asks "What if we didn't have this?" and Senior explains consequences. This is one of the most engaging slide types — use it once per chapter.

6. **Code slides MUST use side-by-side layout** (`code-layout` with `code-col` + `text-col`). The text column should contain:
   - A plain-language summary of what the code does (2-3 sentences)
   - Key design insights or "why" explanations
   - A callout with interview-relevant takeaway or pattern name

7. **Short-answer quiz slides** should include a "Show Reference Answer" button using `showRefAnswer()` JS function and a `<div class="ref-answer hidden" id="{quizId}-ref">` for the answer content.

**Visualization selection guide — when to use which format:**

| Information type | Use | NOT |
|---|---|---|
| A→B→C sequential process, decision branching, request lifecycle | **Mermaid flowchart** (`graph LR/TD`) | Table |
| Comparing 2-4 items across the same set of attributes (e.g., agent types vs allowed tools, config sources vs scope) | **HTML table** (`<table class="vs-table">`) | Mermaid — tables are far more readable for structured comparisons |
| A list of properties with values and rationale (e.g., default values and why) | **HTML table** | Bullet list — tables are scannable |
| Key insight, design principle, interview takeaway | **Callout box** (`<div class="callout">`) | Buried in a paragraph |
| Timeline or state machine (pending→running→completed) | **Mermaid flowchart** | Table |
| Hierarchical containment (what's inside what) | **Mermaid subgraph** | Nested bullet list |
| **Chapter 0 architecture panorama**, **cross-module data flow**, **full system overview** | **Excalidraw diagram** (rendered to PNG) | Mermaid — too complex for 8-node limit |
| **Key architecture diagram per chapter** (if depth = `deep-dive`) | **Excalidraw diagram** | Mermaid — when visual quality matters |

**Mermaid vs Excalidraw decision rule:**
- **Use Mermaid** for inline scenario traces and simple A→B→C flowcharts (≤8 nodes). Fast to generate, renders natively in reveal.js.
- **Use Excalidraw** for the "hero" architecture diagrams: Chapter 0 panorama, cross-module overviews, and any diagram with >8 nodes or complex layout. These are generated as `.excalidraw` JSON files, rendered to PNG via the excalidraw-diagram skill's render pipeline, and embedded in slides as `<img>` tags.

**Excalidraw integration workflow:**
1. **Check availability first**: Verify that `${CLAUDE_SKILL_DIR}/excalidraw/render_excalidraw.py` exists. If not, **fall back to Mermaid** for all diagrams and skip the rest of these steps. Tell the user: "Excalidraw render pipeline not set up. Using Mermaid. Run `cd <skill-dir>/excalidraw && uv sync && uv run playwright install chromium` to enable Excalidraw."
2. Read the excalidraw reference files: `${CLAUDE_SKILL_DIR}/excalidraw/color-palette.md` and `${CLAUDE_SKILL_DIR}/excalidraw/element-templates.md`
3. Generate `.learn/diagrams/chapter-{NN}-{name}.excalidraw` JSON following the excalidraw skill's methodology (visual argumentation, shape meaning, evidence artifacts)
4. Render to PNG: `cd ${CLAUDE_SKILL_DIR}/excalidraw && uv run python render_excalidraw.py <path-to-excalidraw-file>`
5. Read the PNG to validate, fix if needed (render-view-fix loop)
6. In the HTML slide, use: `<img src="../diagrams/chapter-{NN}-{name}.png" style="max-height:450px;">` instead of a mermaid div

**Rule of thumb:** If the information has a *direction* (flow, sequence, dependency), use a diagram. If it has *dimensions* (rows × columns of comparable attributes), use a table. If it's a single key point, use a callout. Never use a diagram just to list items — that's what tables and bullets are for.

Set the `data-theme` attribute on `<body>` based on user's theme preference.
Set `CHAPTER_NUM_INT` to the chapter number (integer, for the report endpoint).

### Step 3.4: Start Server and Open Browser

Kill any existing server:
```bash
if [ -f .learn/.server.pid ]; then kill $(cat .learn/.server.pid) 2>/dev/null; rm -f .learn/.server.pid; fi
```

Start the server in background and capture the port:
```bash
python3 ${CLAUDE_SKILL_DIR}/references/server.py --port 0 --dir .learn --chapter {NN} &
```

Read the server's stdout to capture the `PORT:{N}` line. Save the PID.

Then open the browser:
```bash
open http://localhost:{PORT}/chapters/chapter-{NN}.html
```

On Linux, use `xdg-open` instead of `open`.

Tell the user:
> **Chapter {N}: {Title}** is ready! Go through the presentation in your browser. When you're done, come back here and let me know.

### Step 3.5: Calibration (Chapters 1-2 only)

For chapters 1 and 2, after the user returns, explicitly ask calibration questions using AskUserQuestion:

1. **Difficulty** (header: "Difficulty")
   - "Too easy" — I already knew most of this
   - "Just right" — good balance of new and familiar
   - "Too hard" — I got lost in places

2. **Pacing** (header: "Pacing")
   - "Too fast" — needed more explanation on some slides
   - "Good pace" — comfortable throughout
   - "Too slow" — could have covered more ground

Update preferences with calibration data (add a `calibration` field to preferences.json).

### Step 3.6: Process Report and Continue

Read `.learn/reports/chapter-{NN}.json` if it exists.

Update `.learn/knowledge-profile.json` with cumulative data:
```json
{
  "chaptersCompleted": 3,
  "rollingScore": 0.75,
  "topicScores": {
    "module-a": { "correct": 3, "total": 4 },
    "error-handling": { "correct": 1, "total": 3 }
  },
  "weakTopics": ["error-handling"],
  "strongTopics": ["module-a"],
  "totalTimeSeconds": 2400,
  "lastUpdated": "<ISO timestamp>"
}
```

Briefly tell the user how they did (1-2 sentences). If adjustments will be made for the next chapter, mention them briefly. Then proceed to the next chapter.

---

## Phase 4: Final Review

After all chapters are complete:

1. Generate `.learn/chapters/review-final.html` — a comprehensive review presentation:
   - Architecture overview connecting ALL modules covered
   - Quiz questions weighted toward weak topics from `knowledge-profile.json`
   - Challenge questions that require connecting concepts across chapters
   - Final summary: mastered topics, areas for further study

2. Serve it with the same server mechanism.

3. After the user completes it, read the report and give a final summary:
   - Topics mastered
   - Areas that may need more practice
   - Suggested next steps (specific files to read, features to try building, etc.)

4. Kill the server and clean up:
```bash
if [ -f .learn/.server.pid ]; then kill $(cat .learn/.server.pid) 2>/dev/null; rm -f .learn/.server.pid; fi
```

---

## Important Notes

- **Real code only**: Never invent code examples. Always read actual source files and use real snippets.
- **File paths**: Always show the real file path in code walkthrough slides so users can find the code later.
- **Self-contained HTML**: Each chapter HTML must work standalone — all CDN links, styles, and scripts included.
- **Slide overflow**: reveal.js slides are fixed at 1200×700px. **Never rely on scrolling** — content that doesn't fit must be split into multiple slides. The CSS uses compact font sizes (0.6-0.7em for body text, 0.45em for code) to maximize content density. Do NOT wrap sections in scrollable divs. If content risks overflowing, split it into 2 slides.
- **Content budget per slide** — reveal.js slides are 1200×700px. **Nothing should overflow. If it might not fit, split into 2 slides.** Strict limits:
  - **Dialogue slide**: max 5 chat bubbles (including narrator). Each bubble max 1-3 sentences. Limit `<code>` inline references to short identifiers.
  - **Scenario slide**: 1 scenario-prompt + 1 mermaid flowchart (max 6 nodes) + 1 callout. Nothing else.
  - **Concept slide**: max 1 heading + 1 short paragraph + 1 element (callout OR table OR list of 3-4 items). Never combine multiple rich elements.
  - **Code slide (side-by-side)**: max 20 lines of code in code-col. text-col max 4-5 short sentences. If code is longer, extract the key section only.
  - **Diagram slide**: max 6-8 mermaid nodes + a 1-line caption. Prefer `graph LR` (horizontal).
  - **Table**: max 4 rows + header. More rows → split or use a different format.
  - **Quiz slide**: 1 question + 4 choices + hidden explanation. No extra content above.
  - **General rule**: prefer more slides with less content each over fewer dense slides. White space is good.
- **Port handling**: Always use port 0 (OS-assigned) to avoid conflicts. Capture the actual port from server stdout.
- **Graceful cleanup**: Kill the server before starting a new one. Clean up on final review completion.
- **Mermaid diagrams**: Keep them simple (5-10 nodes max). Use descriptive labels. **Critical sizing rules:**
  - reveal.js slides are fixed at 700px height. Mermaid SVGs will overflow if too tall/wide.
  - Always limit diagrams to **8 nodes max** per diagram. If more nodes are needed, split into multiple slides.
  - Prefer `graph LR` (horizontal) over `graph TD` (vertical) — horizontal layouts fit better in wide slides.
  - Never use `direction TB` inside subgraph blocks (mermaid 11 rendering bug).
  - Never use emoji characters in node labels (causes parse errors). Use plain text only.
  - Never use `<br>` inside node labels. If a node needs multiple lines, split into separate nodes.
  - Subgraph IDs must be ASCII identifiers: use `subgraph MyName["Display Text"]`, not `subgraph "Display Text"`.
  - Never put edges (arrows/connections) inside subgraph blocks. Subgraphs can only contain node declarations. All `-->` / `--` connections must be placed **outside and after** all subgraph blocks.
  - Edge labels should be short (under 5 words). Use `-- "text" -->` syntax, not `-->|"text"|`.
  - CSS constraint is already in styles.css: `.mermaid { max-height: 450px }` — but don't rely on it; design diagrams to fit naturally.
- **Quiz quality**: Questions should test understanding, not memorization. Reference specific code and design decisions.
- **Pacing**: If the user seems disengaged (low ratings, short feedback), ask directly what to change.
- **Visual design**: The CSS uses glassmorphism (frosted glass panels with `backdrop-filter: blur`), gradient accents, and micro-animations. All slide content auto-animates on entry via CSS (`fade-up`). Do NOT add custom animation CSS or JS — the existing stylesheet handles it. The `chapter-progress` bar updates automatically via JS.
- **Google Fonts**: The template loads Inter (body) and JetBrains Mono (code). These are loaded via CDN in the HTML head. Do NOT remove the Google Fonts link.
- **Scenario slides**: Use `slide-scenario` class (not `slide-concept`) for scenario slides. Include the `scenario-prompt` div for the user action trigger.
