#!/usr/bin/env python3
"""Generate SVG project showcase cards for GitHub profile README.

Each card is a visual representation of the project architecture,
rendered as an SVG with a dark theme matching the profile aesthetic.
"""

import os

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "projects")

# Card dimensions
W = 580
H = 320
R = 16  # corner radius

# Color palette
BG = "#0D1117"
BG2 = "#161B22"
BG3 = "#1C2333"
BORDER = "#30363D"
ACCENT = "#58A6FF"
ACCENT2 = "#3FB950"
ACCENT3 = "#D2A8FF"
ACCENT4 = "#F78166"
ACCENT5 = "#FF7B72"
TEXT = "#E6EDF3"
TEXT_DIM = "#8B949E"
TEXT_MID = "#C9D1D9"


def card_shell(title, subtitle, tag, tag_color, inner, icon_svg):
    """Wrap inner content in a styled card shell."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{BG}"/>
      <stop offset="100%" stop-color="{BG2}"/>
    </linearGradient>
    <linearGradient id="accent-line" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{tag_color}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{tag_color}" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="{tag_color}" stop-opacity="0"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="card"><rect width="{W}" height="{H}" rx="{R}"/></clipPath>
  </defs>

  <g clip-path="url(#card)">
    <!-- Background -->
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <rect x="0" y="0" width="{W}" height="1" fill="url(#accent-line)"/>

    <!-- Header -->
    <g transform="translate(24, 28)">
      {icon_svg}
      <text x="32" y="4" font-family="'Segoe UI','Helvetica Neue',Arial,sans-serif" font-size="18" font-weight="700" fill="{TEXT}">{title}</text>
      <text x="32" y="22" font-family="'Segoe UI','Helvetica Neue',Arial,sans-serif" font-size="11" fill="{TEXT_DIM}">{subtitle}</text>
    </g>

    <!-- Tag -->
    <rect x="{W - 100}" y="18" width="80" height="22" rx="11" fill="{tag_color}" opacity="0.15"/>
    <text x="{W - 60}" y="33" text-anchor="middle" font-family="'Segoe UI','Helvetica Neue',Arial,sans-serif" font-size="10" font-weight="600" fill="{tag_color}">{tag}</text>

    <!-- Divider -->
    <line x1="24" y1="58" x2="{W - 24}" y2="58" stroke="{BORDER}" stroke-width="1"/>

    <!-- Content -->
    <g transform="translate(0, 68)">
{inner}
    </g>
  </g>

  <!-- Border -->
  <rect width="{W}" height="{H}" rx="{R}" fill="none" stroke="{BORDER}" stroke-width="1"/>
</svg>"""


def icon_bot():
    return f'<circle cx="10" cy="10" r="10" fill="{ACCENT}" opacity="0.15"/><circle cx="10" cy="10" r="5" fill="{ACCENT}"/>'


def icon_network():
    return (
        f'<circle cx="10" cy="10" r="10" fill="{ACCENT3}" opacity="0.15"/>'
        f'<circle cx="7" cy="7" r="2" fill="{ACCENT3}"/>'
        f'<circle cx="13" cy="13" r="2" fill="{ACCENT3}"/>'
        f'<circle cx="13" cy="7" r="2" fill="{ACCENT3}"/>'
        f'<line x1="7" y1="7" x2="13" y2="13" stroke="{ACCENT3}" stroke-width="1"/>'
        f'<line x1="7" y1="7" x2="13" y2="7" stroke="{ACCENT3}" stroke-width="1"/>'
    )


def icon_shield():
    return (
        f'<circle cx="10" cy="10" r="10" fill="{ACCENT2}" opacity="0.15"/>'
        f'<path d="M10 3 L16 6 L16 12 Q16 17 10 19 Q4 17 4 12 L4 6 Z" fill="none" stroke="{ACCENT2}" stroke-width="1.5"/>'
    )


def icon_graph():
    return (
        f'<circle cx="10" cy="10" r="10" fill="{ACCENT4}" opacity="0.15"/>'
        f'<polyline points="4,16 8,10 12,13 16,5" fill="none" stroke="{ACCENT4}" stroke-width="1.5"/>'
    )


def icon_scale():
    return (
        f'<circle cx="10" cy="10" r="10" fill="{ACCENT5}" opacity="0.15"/>'
        f'<line x1="10" y1="4" x2="10" y2="16" stroke="{ACCENT5}" stroke-width="1.5"/>'
        f'<line x1="4" y1="7" x2="16" y2="7" stroke="{ACCENT5}" stroke-width="1.5"/>'
        f'<circle cx="5" cy="10" r="2" fill="none" stroke="{ACCENT5}" stroke-width="1"/>'
        f'<circle cx="15" cy="10" r="2" fill="none" stroke="{ACCENT5}" stroke-width="1"/>'
    )


def icon_search():
    return (
        f'<circle cx="10" cy="10" r="10" fill="{ACCENT}" opacity="0.15"/>'
        f'<circle cx="9" cy="9" r="4" fill="none" stroke="{ACCENT}" stroke-width="1.5"/>'
        f'<line x1="12" y1="12" x2="16" y2="16" stroke="{ACCENT}" stroke-width="1.5"/>'
    )


def _box(x, y, w, h, label, color, sublabel=None):
    """Rounded box with label inside."""
    lines = [
        f'      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{color}" opacity="0.12" stroke="{color}" stroke-width="0.5" stroke-opacity="0.3"/>',
        f'      <text x="{x + w / 2}" y="{y + h / 2 + (0 if sublabel else 4)}" text-anchor="middle" font-family="\'Segoe UI\',sans-serif" font-size="10" font-weight="600" fill="{color}">{label}</text>',
    ]
    if sublabel:
        lines.append(
            f'      <text x="{x + w / 2}" y="{y + h / 2 + 14}" text-anchor="middle" font-family="\'Segoe UI\',sans-serif" font-size="8" fill="{TEXT_DIM}">{sublabel}</text>'
        )
    return "\n".join(lines)


def _arrow(x1, y1, x2, y2, color=TEXT_DIM):
    """Simple line arrow."""
    return f'      <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1" stroke-dasharray="3,2" opacity="0.4"/>'


def _label(x, y, text, size=9, color=TEXT_DIM):
    return f'      <text x="{x}" y="{y}" font-family="\'Segoe UI\',sans-serif" font-size="{size}" fill="{color}">{text}</text>'


def _metric(x, y, value, label, color=ACCENT):
    """A metric badge."""
    return (
        f'      <text x="{x}" y="{y}" font-family="\'Segoe UI\',sans-serif" font-size="20" font-weight="700" fill="{color}">{value}</text>\n'
        f'      <text x="{x}" y="{y + 14}" font-family="\'Segoe UI\',sans-serif" font-size="9" fill="{TEXT_DIM}">{label}</text>'
    )


# ══════════════════════════════════════════════
# PROJECT CARDS
# ══════════════════════════════════════════════

def card_aegis():
    inner = "\n".join([
        # Architecture diagram
        _label(30, 12, "ARCHITECTURE", 9, TEXT_DIM),

        # Data sources column
        _box(30, 22, 85, 28, "Banking", ACCENT2, "Plaid"),
        _box(30, 56, 85, 28, "Calendar", ACCENT, "Google + Outlook"),
        _box(30, 90, 85, 28, "Health", ACCENT4, "Garmin"),
        _box(30, 124, 85, 28, "LMS", ACCENT3, "Canvas"),
        _box(30, 158, 85, 28, "Social", ACCENT5, "LinkedIn + X"),

        # Arrows to center
        _arrow(115, 36, 155, 80, ACCENT2),
        _arrow(115, 70, 155, 95, ACCENT),
        _arrow(115, 104, 155, 110, ACCENT4),
        _arrow(115, 138, 155, 125, ACCENT3),
        _arrow(115, 172, 155, 140, ACCENT5),

        # Core engine
        _box(155, 60, 120, 100, "AI Agent Core", ACCENT, "RAG + Cron + Skills"),

        # Arrow to output
        _arrow(275, 110, 315, 65, ACCENT),
        _arrow(275, 110, 315, 115, ACCENT),
        _arrow(275, 110, 315, 165, ACCENT),

        # Output column
        _box(315, 44, 100, 36, "WhatsApp", ACCENT2, "Daily Briefings"),
        _box(315, 96, 100, 36, "Insights", ACCENT3, "Financial + Health"),
        _box(315, 148, 100, 36, "Content", ACCENT4, "Auto-publish"),

        # Infra badges
        _label(435, 30, "INFRA", 9, TEXT_DIM),
        _box(435, 40, 110, 22, "Docker Compose", TEXT_DIM),
        _box(435, 68, 110, 22, "Cloudflare Tunnel", TEXT_DIM),
        _box(435, 96, 110, 22, "PostgreSQL + pgvec", TEXT_DIM),
        _box(435, 124, 110, 22, "AES-256-GCM", TEXT_DIM),
        _box(435, 152, 110, 22, "Zero Public Ports", TEXT_DIM),

        # Metrics row
        _metric(50, 218, "15+", "Data Sources", ACCENT),
        _metric(150, 218, "8", "AI Skills", ACCENT3),
        _metric(240, 218, "4", "Agents", ACCENT2),
        _metric(330, 218, "0", "Public Ports", ACCENT4),
        _metric(430, 218, "24/7", "Autonomous", ACCENT5),
    ])
    return card_shell(
        "Aegis", "Personal Intelligence Platform", "AI SYSTEM", ACCENT,
        inner, icon_bot()
    )


def card_partnerships_os():
    inner = "\n".join([
        _label(30, 12, "KNOWLEDGE GRAPH ARCHITECTURE", 9, TEXT_DIM),

        # Graph visualization (simplified)
        # Central node
        f'      <circle cx="160" cy="100" r="20" fill="{ACCENT3}" opacity="0.2" stroke="{ACCENT3}" stroke-width="1"/>',
        f'      <text x="160" y="104" text-anchor="middle" font-family="\'Segoe UI\',sans-serif" font-size="8" font-weight="600" fill="{ACCENT3}">Partner</text>',

        # Connected nodes
        f'      <circle cx="80" cy="60" r="16" fill="{ACCENT}" opacity="0.15" stroke="{ACCENT}" stroke-width="0.8"/>',
        f'      <text x="80" y="64" text-anchor="middle" font-family="\'Segoe UI\',sans-serif" font-size="7" fill="{ACCENT}">Contact</text>',

        f'      <circle cx="80" cy="140" r="16" fill="{ACCENT2}" opacity="0.15" stroke="{ACCENT2}" stroke-width="0.8"/>',
        f'      <text x="80" y="144" text-anchor="middle" font-family="\'Segoe UI\',sans-serif" font-size="7" fill="{ACCENT2}">Deal</text>',

        f'      <circle cx="240" cy="60" r="16" fill="{ACCENT4}" opacity="0.15" stroke="{ACCENT4}" stroke-width="0.8"/>',
        f'      <text x="240" y="64" text-anchor="middle" font-family="\'Segoe UI\',sans-serif" font-size="7" fill="{ACCENT4}">Event</text>',

        f'      <circle cx="240" cy="140" r="16" fill="{ACCENT5}" opacity="0.15" stroke="{ACCENT5}" stroke-width="0.8"/>',
        f'      <text x="240" y="144" text-anchor="middle" font-family="\'Segoe UI\',sans-serif" font-size="7" fill="{ACCENT5}">Outcome</text>',

        # Edges
        f'      <line x1="96" y1="60" x2="140" y2="90" stroke="{ACCENT}" stroke-width="0.8" opacity="0.4"/>',
        f'      <line x1="96" y1="140" x2="140" y2="110" stroke="{ACCENT2}" stroke-width="0.8" opacity="0.4"/>',
        f'      <line x1="224" y1="60" x2="180" y2="90" stroke="{ACCENT4}" stroke-width="0.8" opacity="0.4"/>',
        f'      <line x1="224" y1="140" x2="180" y2="110" stroke="{ACCENT5}" stroke-width="0.8" opacity="0.4"/>',
        f'      <line x1="80" y1="76" x2="80" y2="124" stroke="{TEXT_DIM}" stroke-width="0.5" opacity="0.3" stroke-dasharray="2,2"/>',
        f'      <line x1="240" y1="76" x2="240" y2="124" stroke="{TEXT_DIM}" stroke-width="0.5" opacity="0.3" stroke-dasharray="2,2"/>',

        # Right panel - features
        _label(330, 20, "FEATURES", 9, TEXT_DIM),
        _box(330, 30, 215, 26, "Neo4j Knowledge Graph", ACCENT3),
        _box(330, 62, 215, 26, "Voice-First AI Agent", ACCENT),
        _box(330, 94, 215, 26, "Notion-Synced CRM", ACCENT2),
        _box(330, 126, 215, 26, "AI Relationship Scoring", ACCENT4),
        _box(330, 158, 215, 26, "Pipeline Analytics", ACCENT5),

        # Metrics
        _metric(50, 218, "Neo4j", "Graph Database", ACCENT3),
        _metric(170, 218, "GPT-4", "Voice Agent", ACCENT),
        _metric(310, 218, "Notion", "CRM Sync", ACCENT2),
        _metric(430, 218, "Real-time", "Scoring", ACCENT4),
    ])
    return card_shell(
        "Partnerships OS", "Enterprise Partnership Intelligence", "PLATFORM", ACCENT3,
        inner, icon_network()
    )


def card_sentinel():
    inner = "\n".join([
        _label(30, 12, "SLACK BOT PIPELINE", 9, TEXT_DIM),

        # Pipeline flow
        _box(30, 28, 95, 40, "Slack Events", ACCENT, "Messages + Joins"),
        _arrow(125, 48, 155, 48, ACCENT),

        _box(155, 28, 95, 40, "GPT-4 Engine", ACCENT3, "Intent + Research"),
        _arrow(250, 48, 280, 48, ACCENT3),

        _box(280, 28, 95, 40, "Action Router", ACCENT4, "Classify + Route"),
        _arrow(375, 48, 405, 48, ACCENT4),

        _box(405, 28, 140, 40, "Human-in-the-Loop", ACCENT2, "Approve / Override"),

        # Second row - capabilities
        _label(30, 92, "CAPABILITIES", 9, TEXT_DIM),

        _box(30, 102, 125, 34, "Auto-Onboarding", ACCENT2, "New member welcome"),
        _box(165, 102, 125, 34, "Research Pipeline", ACCENT, "Deep-dive any topic"),
        _box(300, 102, 125, 34, "Smart Outreach", ACCENT3, "Personalized DMs"),
        _box(435, 102, 110, 34, "Moderation", ACCENT5, "Content filtering"),

        # Third row - data flow
        _label(30, 158, "DATA FLOW", 9, TEXT_DIM),
        _box(30, 168, 160, 28, "Community Knowledge Base", ACCENT),
        _arrow(190, 182, 220, 182, ACCENT),
        _box(220, 168, 140, 28, "Vector Search (RAG)", ACCENT3),
        _arrow(360, 182, 390, 182, ACCENT3),
        _box(390, 168, 155, 28, "Contextual Responses", ACCENT2),

        # Metrics
        _metric(50, 222, "GPT-4", "Research Engine", ACCENT),
        _metric(170, 222, "RAG", "Knowledge Base", ACCENT3),
        _metric(310, 222, "HITL", "Human Review", ACCENT2),
        _metric(430, 222, "24/7", "Community Bot", ACCENT4),
    ])
    return card_shell(
        "Sentinel", "AI Community Management Bot", "SLACK BOT", ACCENT2,
        inner, icon_shield()
    )


def card_lattice():
    inner = "\n".join([
        _label(30, 12, "MULTI-AGENT ORCHESTRATION", 9, TEXT_DIM),

        # Agent hierarchy visualization
        # Supervisor
        _box(200, 22, 160, 32, "Supervisor Agent", ACCENT3, "Planning + Routing"),

        # Arrows down
        _arrow(240, 54, 100, 80, ACCENT3),
        _arrow(280, 54, 280, 80, ACCENT3),
        _arrow(320, 54, 460, 80, ACCENT3),

        # Worker agents
        _box(40, 80, 120, 32, "Research Agent", ACCENT, "Web + RAG search"),
        _box(220, 80, 120, 32, "Analysis Agent", ACCENT4, "Data processing"),
        _box(400, 80, 120, 32, "Execution Agent", ACCENT2, "Tool calling"),

        # Arrows to verification
        _arrow(100, 112, 280, 138, ACCENT),
        _arrow(280, 112, 280, 138, ACCENT4),
        _arrow(460, 112, 280, 138, ACCENT2),

        # Verification layer
        _box(200, 138, 160, 32, "Formal Verifier", ACCENT5, "Workflow validation"),

        # Right panel - key features
        _label(30, 195, "KEY INNOVATIONS", 9, TEXT_DIM),
        _box(30, 205, 125, 24, "Learned Routing", ACCENT3),
        _box(165, 205, 125, 24, "Adaptive Planning", ACCENT),
        _box(300, 205, 135, 24, "Formal Verification", ACCENT5),
        _box(445, 205, 100, 24, "Self-Healing", ACCENT2),
    ])
    return card_shell(
        "Lattice", "Hierarchical Agent Orchestration", "RESEARCH", ACCENT3,
        inner, icon_network()
    )


def card_evictionchatbot():
    inner = "\n".join([
        _label(30, 12, "AI LEGAL ASSISTANT FLOW", 9, TEXT_DIM),

        # User flow
        _box(30, 28, 110, 38, "Tenant", ACCENT, "Facing eviction"),
        _arrow(140, 47, 170, 47, ACCENT),

        _box(170, 28, 120, 38, "EVITA Chat", ACCENT2, "Natural language Q&A"),
        _arrow(290, 47, 320, 47, ACCENT2),

        _box(320, 28, 110, 38, "Legal Analysis", ACCENT3, "PA tenant law"),
        _arrow(430, 47, 460, 47, ACCENT3),

        _box(460, 28, 90, 38, "Action Plan", ACCENT4, "Next steps"),

        # Knowledge base
        _label(30, 90, "LEGAL KNOWLEDGE BASE", 9, TEXT_DIM),
        _box(30, 100, 165, 30, "PA Landlord-Tenant Act", ACCENT2),
        _box(205, 100, 165, 30, "Municipal Housing Codes", ACCENT),
        _box(380, 100, 170, 30, "Court Procedures + Forms", ACCENT3),

        # Impact section
        _label(30, 152, "BUILT WITH", 9, TEXT_DIM),
        _box(30, 162, 200, 30, "Philadelphia Legal Assistance", ACCENT2),
        _box(240, 162, 150, 30, "RAG Pipeline", ACCENT),
        _box(400, 162, 150, 30, "Next.js + Vercel", ACCENT4),

        # Metrics
        _metric(50, 222, "Free", "Legal Help", ACCENT2),
        _metric(170, 222, "RAG", "Legal Search", ACCENT),
        _metric(310, 222, "PA Law", "Specialized", ACCENT3),
        _metric(430, 222, "Live", "evita.vercel.app", ACCENT4),
    ])
    return card_shell(
        "EVITA", "AI Legal Assistant for Tenants", "SOCIAL GOOD", ACCENT2,
        inner, icon_scale()
    )


def card_spectra():
    inner = "\n".join([
        _label(30, 12, "RAG EVALUATION FRAMEWORK", 9, TEXT_DIM),

        # Pipeline visualization
        # Strategy column
        _label(30, 32, "12 RETRIEVAL STRATEGIES", 8, TEXT_DIM),
        _box(30, 40, 120, 20, "Naive RAG", ACCENT),
        _box(30, 64, 120, 20, "HyDE", ACCENT),
        _box(30, 88, 120, 20, "Self-RAG", ACCENT3),
        _box(30, 112, 120, 20, "Fusion", ACCENT4),
        _box(30, 136, 120, 20, "ColBERT", ACCENT5),
        f'      <text x="90" y="170" text-anchor="middle" font-family="\'Segoe UI\',sans-serif" font-size="9" fill="{TEXT_DIM}">+ 7 more...</text>',

        # Arrow to evaluation
        _arrow(150, 100, 190, 100, ACCENT),

        # Evaluation engine
        _box(190, 38, 140, 50, "A/B Test Engine", ACCENT3, "Automated comparison"),
        _arrow(190, 100, 330, 60, ACCENT3),

        # Quality metrics
        _box(190, 100, 140, 50, "Quality Metrics", ACCENT, "Precision + Recall"),
        _arrow(330, 125, 360, 75, ACCENT),

        # Pareto output
        _box(360, 38, 185, 50, "Pareto-Optimal", ACCENT2, "Best accuracy vs. latency"),

        # Pareto chart (simplified)
        _label(370, 108, "PARETO FRONTIER", 8, TEXT_DIM),
        # Axes
        f'      <line x1="370" y1="190" x2="535" y2="190" stroke="{TEXT_DIM}" stroke-width="0.5"/>',
        f'      <line x1="370" y1="120" x2="370" y2="190" stroke="{TEXT_DIM}" stroke-width="0.5"/>',
        f'      <text x="450" y="205" text-anchor="middle" font-family="\'Segoe UI\',sans-serif" font-size="7" fill="{TEXT_DIM}">Latency</text>',
        f'      <text x="360" y="155" text-anchor="middle" font-family="\'Segoe UI\',sans-serif" font-size="7" fill="{TEXT_DIM}" transform="rotate(-90, 360, 155)">Quality</text>',
        # Pareto points
        f'      <circle cx="390" cy="175" r="3" fill="{ACCENT5}" opacity="0.5"/>',
        f'      <circle cx="410" cy="160" r="3" fill="{ACCENT4}" opacity="0.5"/>',
        f'      <circle cx="435" cy="145" r="4" fill="{ACCENT2}"/>',
        f'      <circle cx="470" cy="135" r="4" fill="{ACCENT3}"/>',
        f'      <circle cx="510" cy="130" r="3" fill="{ACCENT}" opacity="0.5"/>',
        # Pareto curve
        f'      <path d="M390 175 Q420 150 435 145 Q460 135 510 130" fill="none" stroke="{ACCENT2}" stroke-width="1" stroke-dasharray="3,2" opacity="0.5"/>',

        # Metrics
        _metric(50, 218, "12", "Strategies", ACCENT),
        _metric(170, 218, "A/B", "Auto-Testing", ACCENT3),
        _metric(310, 218, "Pareto", "Optimization", ACCENT2),
        _metric(430, 218, "MkDocs", "Documentation", ACCENT4),
    ])
    return card_shell(
        "Spectra", "Systematic RAG Evaluation", "FRAMEWORK", ACCENT,
        inner, icon_search()
    )


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    cards = {
        "aegis": card_aegis,
        "partnerships-os": card_partnerships_os,
        "sentinel": card_sentinel,
        "lattice": card_lattice,
        "evita": card_evictionchatbot,
        "spectra": card_spectra,
    }

    for name, fn in cards.items():
        svg = fn()
        path = os.path.join(OUT_DIR, f"{name}.svg")
        with open(path, "w") as f:
            f.write(svg)
        print(f"Generated {path}")


if __name__ == "__main__":
    main()
