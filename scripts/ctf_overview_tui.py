#!/usr/bin/env python3
"""Build the aligned 120x40 CTF Overview TUI from the profile layout spec."""

WIDTH = 120
MAIN = 88
RAIL = 29

SAMPLE = {
    "competition": "HackTheBox Cyber Apocalypse",
    "team": "red-asgard",
    "total_score": "8420",
    "our_rank": "17",
    "time_remain": "05:42:11",
    "phase_label": "endgame",
    "profile": "ctf",
    "queued": "6",
    "wu_ready": "3 ready",
    "focused_chal": "svc/auth-edge",
    "last_event": "approval req",
    "bridge": "healthy",
    "queue_press": "medium",
}


def row_top(main: str, rail: str) -> str:
    line = "┌" + main[:MAIN].ljust(MAIN) + "┬" + rail[:RAIL].ljust(RAIL) + "┐"
    return line[:WIDTH].ljust(WIDTH)


def row_mid(main: str, rail: str) -> str:
    line = "│" + main[:MAIN].ljust(MAIN) + "│" + rail[:RAIL].ljust(RAIL) + "│"
    return line[:WIDTH].ljust(WIDTH)


def row_sep(main: str, rail: str) -> str:
    line = "├" + main[:MAIN].ljust(MAIN) + "┤" + rail[:RAIL].ljust(RAIL) + "│"
    return line[:WIDTH].ljust(WIDTH)


def row_bot(main: str, rail: str) -> str:
    line = "└" + main[:MAIN].ljust(MAIN) + "┴" + rail[:RAIL].ljust(RAIL) + "┘"
    return line[:WIDTH].ljust(WIDTH)


def build() -> list[str]:
    s = SAMPLE
    lines = [
        row_top(
            "─ TAB 1/9 — [Overview] Challenges · Detail · Agents · Cntrs · Intel · WUps · Subs · Plan",
            "─ STATE RAIL ────────────────",
        ),
        row_mid(
            f" SKULD CTF  {s['competition']}  Team: {s['team']}  Score {s['total_score']}  Rank #{s['our_rank']}",
            "",
        ),
        row_mid(
            f"            Time {s['time_remain']}  Phase {s['phase_label']}",
            " COMPETITION                 ",
        ),
        row_mid("", f"  Profile     {s['profile']}      "),
        row_mid(
            " ┌─ CHALLENGES ───────────┬─ FOCUSED CHALLENGE ──────────┬─ URGENT / NEXT ────┐",
            f"  Phase       {s['phase_label']}  ",
        ),
        row_mid(
            " │ public.challenge_rows  │ public.focused_challenge_…   │ (alerts CRIT/URG)  │",
            f"  Score       {s['total_score']}  ",
        ),
        row_mid(
            " │  Name  Pts  Status  %  │ detail                       │                    │",
            f"  Rank        #{s['our_rank']}     ",
        ),
        row_mid(
            " │  filter: web|pwn|…     ├─ Last meaningful event ──────┼─ STRATEGIST ───────┤",
            f"  Time Left   {s['time_remain']}  ",
        ),
        row_mid(
            " │  sort: ROI|solves|pts  │ public.last_major_event      │ public.strategist… │",
            "",
        ),
        row_mid(
            " │                        ├─ Branches ───────────────────┼─ HEALTH ───────────┤",
            " CAPACITY                    ",
        ),
        row_mid(
            " │ ┌─ Mini stats ───────┐ │ public.branch_rows           │ public.system_…    │",
            f"  Queued      {s['queued']}       ",
        ),
        row_mid(
            " │ │ public.challenge_… │ │  Branch  Strategy  %  Status │ health             │",
            f"  Writeups    {s['wu_ready']}     ",
        ),
        row_mid(
            " │ │ summary            │ │                              │                    │",
            "",
        ),
        row_mid(
            " │ └────────────────────┘ │                              │                    │",
            " URGENT                      ",
        ),
        row_mid(
            " ├─ ACTIVE AGENTS ────────┼─ LIVE OUTPUT ────────────────┼─ SUBMISSIONS ──────┤",
            f"  Focus       {s['focused_chal']} ",
        ),
        row_mid(
            " │ * ctf-coordinator      │ agent_output stream          │ public.submission_ │",
            f"  Last Event  {s['last_event']}   ",
        ),
        row_mid(
            " │   ctf-broker           │  Ctrl+L: Chat / Log          │ rows               │",
            "",
        ),
        row_mid(
            " │   ctf-strategist       │                              ├─ CONTAINERS ───────┤",
            " HEALTH                      ",
        ),
        row_mid(
            " │   …                    │                              │ public.container_  │",
            f"  Bridge      {s['bridge']}       ",
        ),
        row_mid(
            " │                        │                              │ rows               │",
            f"  Queue       {s['queue_press']}  ",
        ),
        row_mid(
            " └────────────────────────┴──────────────────────────────┴────────────────────┘",
            "",
        ),
    ]

    # Blank body rows (21–35)
    for _ in range(15):
        lines.append(row_mid("", ""))

    lines.extend(
        [
            row_sep(
                "─ INPUT ────────────────────────────────────────────────────────────────────────────────",
                "",
            ),
            row_mid(" > _", ""),
            row_mid("", ""),
            row_bot(
                "────────────────────────────────────────────────────────────────────────────────────────",
                "─────────────────────────────",
            ),
        ]
    )

    if len(lines) != 40:
        raise ValueError(f"expected 40 lines, got {len(lines)}")

    for i, line in enumerate(lines, 1):
        if len(line) != WIDTH:
            raise ValueError(f"line {i}: len {len(line)} != {WIDTH}: {line!r}")

    return lines


if __name__ == "__main__":
    for line in build():
        print(line)
