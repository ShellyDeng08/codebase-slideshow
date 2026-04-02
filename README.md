# codebase-slideshow

A Claude Code skill that generates beautiful HTML slideshow courses for any codebase — glassmorphism reveal.js presentations with dialogue narrative, interactive quizzes, and adaptive teaching.

## What it does

Point it at a codebase, and it will:

1. **Explore** the codebase structure, modules, and patterns
2. **Generate a syllabus** tailored to your learning goal (interview prep, contributing, general understanding)
3. **Build chapter-by-chapter presentations** with:
   - Dialogue-driven narrative (two characters explore the code together)
   - Real code walkthroughs (never invented examples)
   - Mermaid and Excalidraw architecture diagrams
   - Interactive quizzes with explanations
   - Adaptive difficulty based on your quiz scores
4. **Serve locally** and open in your browser

The presentations use a glassmorphism visual design with frosted glass panels, gradient accents, and micro-animations.

## Installation

Copy this skill into your project's `.claude/skills/` directory:

```bash
# From your project root
mkdir -p .claude/skills
cp -r /path/to/codebase-slideshow .claude/skills/codebase-slideshow
```

Or clone directly:

```bash
cd your-project/.claude/skills
git clone https://github.com/YOUR_USER/codebase-slideshow.git codebase-slideshow
```

## Prerequisites

- **Claude Code** (the CLI) — this is a skill, not a standalone tool
- **Python 3** — for the local presentation server (no pip dependencies needed)

### Optional: Excalidraw diagrams

For high-quality architecture diagrams (rendered as PNG), you need:

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Set up the Excalidraw renderer
cd .claude/skills/codebase-slideshow/excalidraw
uv sync
uv run playwright install chromium
```

Without this, the skill falls back to Mermaid diagrams (which still look good, just less polished for complex architectures).

## Usage

In Claude Code, just say:

```
Teach me this codebase
```

or invoke the skill explicitly:

```
/codebase-slideshow
```

The skill will ask you about:
- **Language** (English, 中文, 日本語, or custom)
- **Teaching style** (dialogue-driven, technical deep-dive, visual-first, example-driven)
- **Tech level** (beginner, intermediate, advanced)
- **Learning goal** (general understanding, contribute, interview prep, code review)
- **Theme** (light or dark)
- **Depth** (overview, standard, deep-dive)

Then it generates and serves chapters one by one.

## How it works

```
.learn/                     ← Generated in your project root
├── preferences.json        ← Your settings
├── codebase-profile.json   ← Analysis results
├── syllabus.json           ← Chapter plan
├── styles.css              ← Presentation styles
├── chapters/
│   ├── chapter-00.html     ← Course overview
│   ├── chapter-01.html     ← First chapter
│   └── ...
├── diagrams/
│   ├── chapter-00-panorama.png
│   └── ...
├── drafts/
│   ├── chapter-01.md       ← Lesson plan (editable!)
│   └── ...
└── reports/
    ├── chapter-01.json     ← Quiz results & feedback
    └── ...
```

The **drafts** are editable markdown files. You can ask Claude to adjust a draft before regenerating the HTML — no need to re-read source code.

## Customization

- Edit `references/styles.css` to change the visual theme
- Edit `references/template-base.html` to modify the slide template
- Edit `excalidraw/color-palette.md` to change diagram colors

## License

MIT
