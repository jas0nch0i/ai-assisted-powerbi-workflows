"""
Generate polished visual assets for the AI-Assisted PowerBI Workflows project.

Outputs (saved to ../images/):
  01-human-ai-workflow.png   — 9-stage workflow with human/AI ownership split
  02-prompt-categories.png   — prompt taxonomy (DAX / KPI / docs / dashboard / troubleshooting)
  03-human-vs-ai.png         — what AI does vs what the human owns
  04-impact-diagram.png      — speed + consistency + repeatability gains
"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
IMG_DIR = ROOT / "images"
IMG_DIR.mkdir(exist_ok=True, parents=True)

# Brand palette
PRIMARY  = "#1565C0"
TEAL     = "#2980B9"
GOOD     = "#3A9B7A"
ACCENT   = "#F2A93B"
PURPLE   = "#5C2D91"
BAD      = "#D13438"
NEUTRAL  = "#605E5C"
LIGHT    = "#F3F2F1"
TEXT     = "#252423"
TEXT2    = "#605E5C"

plt.rcParams.update({
    "figure.dpi": 110,
    "savefig.dpi": 140,
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def card(ax, x, y, w, h, fill="white", edge=LIGHT, lw=0.8, alpha=1.0):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.005,rounding_size=0.05",
                         linewidth=lw, facecolor=fill, edgecolor=edge, alpha=alpha)
    ax.add_patch(box)


def text(ax, x, y, s, **kw):
    defaults = dict(ha="left", va="center", color=TEXT, fontsize=10)
    defaults.update(kw)
    ax.text(x, y, s, **defaults)


# ---------------------------------------------------------------------------
# 1. 9-stage workflow with ownership lanes
# ---------------------------------------------------------------------------
def workflow_diagram():
    fig, ax = plt.subplots(figsize=(16, 7), facecolor="white")
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 7)
    ax.axis("off")

    fig.suptitle("AI-Assisted Power BI Development — 9 Stages, 2 Lanes",
                 fontsize=15, fontweight="bold", y=0.98)
    ax.text(8, 6.45,
            "Each stage shows what AI accelerates and what the human owns",
            ha="center", color=TEXT2, fontsize=11, style="italic")

    stages = [
        ("1. Define\nproblem",       "human-led",   "Audience\nKPI goals"),
        ("2. Gather\nrequirements",  "human-led",   "Questions\nVisuals + filters"),
        ("3. Structure\ndata model", "shared",      "Tables\nRelationships"),
        ("4. Draft KPI\ndefinitions","ai-assisted", "Naming\nBusiness wording"),
        ("5. Develop\nlayout",       "ai-assisted", "Page flow\nVisual hierarchy"),
        ("6. Build +\nrefine DAX",   "ai-assisted", "Patterns\nTroubleshooting"),
        ("7. Document\nthe report",  "ai-assisted", "Data dictionary\nKPI specs + handoff"),
        ("8. Validate\nwith users",  "human-led",   "Confirm accuracy\nUsability check"),
        ("9. Finalize +\nimprove",   "shared",      "Refine logic\nUpdate docs"),
    ]

    color_map = {
        "human-led":   PRIMARY,
        "ai-assisted": ACCENT,
        "shared":      PURPLE,
    }
    label_map = {
        "human-led":   "Human-led",
        "ai-assisted": "AI-assisted",
        "shared":      "Shared",
    }

    box_w, box_h = 1.55, 1.5
    gap = 0.20
    start_x = 0.4
    y = 3.4
    for i, (title, lane, sub) in enumerate(stages):
        x = start_x + i * (box_w + gap)
        c = color_map[lane]
        card(ax, x, y, box_w, box_h, fill=c, edge=c)
        text(ax, x + box_w / 2, y + box_h - 0.32, title,
             ha="center", color="white", fontsize=10, fontweight="bold")
        # ownership tag
        card(ax, x + 0.1, y + 0.18, box_w - 0.2, 0.32, fill="white", edge="white", alpha=0.85)
        text(ax, x + box_w / 2, y + 0.34, label_map[lane],
             ha="center", color=c, fontsize=8, fontweight="bold")

    # Subtitles below boxes (2-line wrap built into the strings)
    for i, (_, _, sub) in enumerate(stages):
        x = start_x + i * (box_w + gap) + box_w / 2
        ax.text(x, 2.65, sub, ha="center", va="top", color=TEXT2,
                fontsize=8.5, style="italic", linespacing=1.3)

    # Connecting line
    ax.plot([start_x + box_w / 2, start_x + box_w / 2 + 8 * (box_w + gap)],
            [y + box_h / 2, y + box_h / 2],
            color="white", linewidth=0, zorder=0)

    # Legend at top
    legend_y = 5.5
    legend_items = [("Human-led",   PRIMARY),
                    ("AI-assisted", ACCENT),
                    ("Shared",      PURPLE)]
    for i, (lbl, col) in enumerate(legend_items):
        x = 5 + i * 2.3
        card(ax, x, legend_y, 0.4, 0.4, fill=col, edge=col)
        text(ax, x + 0.55, legend_y + 0.2, lbl, color=TEXT, fontsize=10, fontweight="bold")

    # Bottom principle
    text(ax, 8, 1.1,
         "AI supports the work · the human owns the decision-making",
         ha="center", color=TEXT, fontsize=12, fontweight="bold")
    text(ax, 8, 0.7,
         "Business judgment, KPI definitions, validation, and stakeholder communication remain human responsibilities",
         ha="center", color=TEXT2, fontsize=10, style="italic")

    fig.savefig(IMG_DIR / "01-human-ai-workflow.png", facecolor="white", bbox_inches=None)
    plt.close(fig)
    print("  saved 01-human-ai-workflow.png")


# ---------------------------------------------------------------------------
# 2. Prompt categories taxonomy
# ---------------------------------------------------------------------------
def prompt_categories():
    fig, ax = plt.subplots(figsize=(15, 7), facecolor="white")
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 7)
    ax.axis("off")

    fig.suptitle("Prompt Pattern Taxonomy — Five Categories of BI Prompts",
                 fontsize=15, fontweight="bold", y=0.98)

    categories = [
        ("DAX Development", PRIMARY,
         ["Review measure logic\n+ explain wrong totals",
          "Rewrite for readability\n+ maintainability",
          "Suggest alternative patterns\n(rolling avg, YoY)",
          "Explain row vs filter\ncontext"]),
        ("KPI Definitions", TEAL,
         ["Draft business-friendly\ndefinition",
          "Rewrite for non-technical\naudience",
          "Standardize wording\nacross measure set",
          "Map measure to decision\nuse-case"]),
        ("Documentation", GOOD,
         ["Generate data dictionary",
          "Draft semantic model\ndocumentation",
          "Create report specification\noutline",
          "Auto-summarize Power\nQuery M steps"]),
        ("Dashboard Design", ACCENT,
         ["Suggest layout for\nexecutive audience",
          "Recommend KPI card\nhierarchy",
          "Propose cleaner structure",
          "Identify competing visual\npriorities"]),
        ("Troubleshooting", PURPLE,
         ["Identify root cause of\nincorrect totals",
          "Suggest validation steps",
          "Build a KPI verification\nchecklist",
          "Explain unexpected filter\nbehavior"]),
    ]

    box_w = 2.75
    box_h = 5.1
    gap = 0.20
    start_x = 0.5
    y = 0.8

    for i, (name, color, items) in enumerate(categories):
        x = start_x + i * (box_w + gap)
        # header
        card(ax, x, y + box_h - 0.65, box_w, 0.65, fill=color, edge=color)
        text(ax, x + box_w / 2, y + box_h - 0.32, name,
             ha="center", color="white", fontsize=11, fontweight="bold")
        # body
        card(ax, x, y, box_w, box_h - 0.65, fill=LIGHT, edge="#E1DFDD")
        for j, item in enumerate(items):
            iy = y + box_h - 1.20 - j * 1.00
            text(ax, x + 0.15, iy, "▸", color=color, fontsize=11,
                 fontweight="bold", va="top")
            text(ax, x + 0.40, iy, item, color=TEXT, fontsize=9,
                 va="top", linespacing=1.3)

    text(ax, 7.5, 0.5,
         "Use prompts as starting points · always validate output against business context and data",
         ha="center", color=TEXT2, fontsize=10, style="italic")

    fig.savefig(IMG_DIR / "02-prompt-categories.png", facecolor="white", bbox_inches=None)
    plt.close(fig)
    print("  saved 02-prompt-categories.png")


# ---------------------------------------------------------------------------
# 3. Human vs AI ownership split
# ---------------------------------------------------------------------------
def human_vs_ai():
    fig, ax = plt.subplots(figsize=(13, 6), facecolor="white")
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6)
    ax.axis("off")

    fig.suptitle("Ownership Split — AI Accelerates, Human Decides",
                 fontsize=15, fontweight="bold", y=0.97)

    # Left column — AI
    ai_items = [
        "Brainstorming approaches",
        "Generating first drafts",
        "Refining DAX logic",
        "Formatting documentation",
        "Suggesting troubleshooting paths",
        "Organizing requirements into templates",
    ]
    human_items = [
        "Business judgment",
        "KPI definitions",
        "Semantic model validation",
        "Final QA and testing",
        "Stakeholder communication",
        "Determining what is useful and accurate",
    ]

    # AI side
    card(ax, 0.4, 0.6, 5.8, 4.6, fill=ACCENT, edge=ACCENT)
    text(ax, 3.3, 4.85, "AI ASSISTS",
         ha="center", color="white", fontsize=15, fontweight="bold")
    for i, item in enumerate(ai_items):
        iy = 4.30 - i * 0.55
        text(ax, 0.7, iy, "•", color="white", fontsize=18, fontweight="bold")
        text(ax, 1.05, iy, item, color="white", fontsize=11)

    # Human side
    card(ax, 6.8, 0.6, 5.8, 4.6, fill=PRIMARY, edge=PRIMARY)
    text(ax, 9.7, 4.85, "HUMAN OWNS",
         ha="center", color="white", fontsize=15, fontweight="bold")
    for i, item in enumerate(human_items):
        iy = 4.30 - i * 0.55
        text(ax, 7.1, iy, "•", color="white", fontsize=18, fontweight="bold")
        text(ax, 7.45, iy, item, color="white", fontsize=11)

    # Center divider
    text(ax, 6.5, 0.25,
         "AI supports the work · the human owns the decision-making",
         ha="center", color=TEXT, fontsize=11, fontweight="bold", style="italic")

    fig.savefig(IMG_DIR / "03-human-vs-ai.png", facecolor="white", bbox_inches=None)
    plt.close(fig)
    print("  saved 03-human-vs-ai.png")


# ---------------------------------------------------------------------------
# 4. Impact diagram
# ---------------------------------------------------------------------------
def impact_diagram():
    fig, ax = plt.subplots(figsize=(14, 6.5), facecolor="white")
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6.5)
    ax.axis("off")

    fig.suptitle("Where AI-Assisted Workflow Creates Measurable Value",
                 fontsize=15, fontweight="bold", y=0.97)

    impacts = [
        ("SPEED", "Speed",
         "First drafts in minutes, not hours. KPI definitions, data dictionaries, and report specs land faster.",
         GOOD),
        ("CONSIST.", "Consistency",
         "Standardized templates reduce variation in measure naming, descriptions, and documentation.",
         PRIMARY),
        ("REPEAT", "Repeatability",
         "Reusable prompt patterns mean the same task takes less effort the second, third, and tenth time.",
         TEAL),
        ("DEBUG", "Troubleshooting",
         "Faster framing of measure issues. AI surfaces likely causes; human verifies.",
         ACCENT),
        ("DOCS", "Documentation",
         "Reports ship with documentation, not as an afterthought. Handoff and audit become routine.",
         PURPLE),
    ]

    box_w, box_h = 2.55, 4.4
    gap = 0.25
    start_x = 0.5
    y = 1.0
    for i, (tag, name, detail, color) in enumerate(impacts):
        x = start_x + i * (box_w + gap)
        card(ax, x, y, box_w, box_h, fill="white", edge=color, lw=2.5)
        # color header bar
        card(ax, x, y + box_h - 1.1, box_w, 1.1, fill=color, edge=color)
        text(ax, x + box_w / 2, y + box_h - 0.65, tag,
             ha="center", color="white", fontsize=12, fontweight="bold")
        text(ax, x + box_w / 2, y + box_h - 0.95, name.upper(),
             ha="center", color="white", fontsize=10, alpha=0.85)

    text(ax, 7, 0.4,
         "These gains compound when prompt patterns and templates become part of the team's standard practice.",
         ha="center", color=TEXT2, fontsize=10, style="italic")

    # Manual word-wrap into the body region (below the colored header)
    # Wrap to ~22 chars so text fits inside the card width with margin
    for i, (_, _, detail, _) in enumerate(impacts):
        x = start_x + i * (box_w + gap)
        words = detail.split(" ")
        lines, line = [], ""
        for w in words:
            if len(line) + len(w) + 1 < 22:
                line = (line + " " + w).strip()
            else:
                lines.append(line)
                line = w
        if line:
            lines.append(line)
        for j, ln in enumerate(lines):
            text(ax, x + 0.18, y + box_h - 1.50 - j * 0.30, ln,
                 color=TEXT, fontsize=8.5, va="top")

    fig.savefig(IMG_DIR / "04-impact-diagram.png", facecolor="white", bbox_inches=None)
    plt.close(fig)
    print("  saved 04-impact-diagram.png")


def main():
    print("Generating AI-Assisted PowerBI Workflows visuals...")
    workflow_diagram()
    prompt_categories()
    human_vs_ai()
    impact_diagram()
    print(f"\nAll visuals saved to {IMG_DIR}")


if __name__ == "__main__":
    main()
