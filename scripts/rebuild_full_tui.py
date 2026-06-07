#!/usr/bin/env python3
"""Rebuild 121-column full TUI on a fixed 90-column zone grid."""

from __future__ import annotations

import html
import re
from pathlib import Path

WIDTH = 121
MAIN = 90


def zones(m: str) -> dict[str, str]:
    assert len(m) == MAIN, len(m)
    return {
        "o": m[0],
        "L": m[1:27],
        "d1": m[27],
        "M": m[28:58],
        "d2": m[58],
        "R": m[59:80],
        "d3": m[80],
        "P": m[81:90],
    }


def build_main(z: dict[str, str]) -> str:
    line = (
        z["o"]
        + z["L"].ljust(26)[:26]
        + z["d1"]
        + z["M"].ljust(30)[:30]
        + z["d2"]
        + z["R"].ljust(21)[:21]
        + z["d3"]
        + z["P"].ljust(9)[:9]
    )
    assert len(line) == MAIN, len(line)
    return line


def fix_mini_stats_rows(z: dict[str, str]) -> dict[str, str]:
  z = dict(z)
  z["L"] = z["L"].rstrip("│ ").ljust(26)[:26]
  text_m = z["M"].strip("│ ")
  if text_m and not text_m.startswith(" "):
      text_m = " " + text_m
  z["M"] = text_m[:30].ljust(30)
  text_r = z["R"].strip("│ ")
  if text_r and not text_r.startswith(" "):
      text_r = " " + text_r
  z["R"] = text_r[:21].ljust(21)
  z["d1"] = "│"
  z["d2"] = "│"
  z["d3"] = "│"
  return z


def fix_agents_rows(z: dict[str, str]) -> dict[str, str]:
    z = dict(z)
    if z["R"].startswith("│"):
        z["R"] = z["R"][1:]
    text_m = z["M"].strip("│ ")
    if text_m and not text_m.startswith(" "):
        text_m = " " + text_m
    z["M"] = text_m[:30].ljust(30)
    text_r = z["R"].strip("│ ")
    if text_r and not text_r.startswith(" "):
        text_r = " " + text_r
    z["R"] = text_r[:21].ljust(21)
    z["d1"] = "│"
    z["d2"] = "│" if z["R"].strip() else " "
    z["d3"] = "│"
    return z


def fix_branch_rows(z: dict[str, str]) -> dict[str, str]:
    z = dict(z)
    text_m = z["M"].strip("│ ")
    z["M"] = text_m[:30].ljust(30)
    z["d1"] = "│"
    z["d2"] = " "
    z["d3"] = "│"
    return z


def rebuild_main(main: str, row: int) -> str:
    z = zones(main)
    if row in (14, 15):
        return build_main(fix_mini_stats_rows(z))
    if 22 <= row <= 29 and row != 25:
        return build_main(fix_agents_rows(z))
    if row in (18, 19, 20):
        return build_main(fix_branch_rows(z))
    return build_main(z)


def build_full_line(main: str, rail: str, row: int, total: int) -> str:
    if row == 1:
        line = main + rail + "┐"
    elif row == total:
        line = main + "│" + rail + "┘"
    else:
        line = main + "│" + rail + "│"
    if len(line) != WIDTH:
        raise ValueError(f"row {row}: expected {WIDTH}, got {len(line)}")
    return line


def extract_flex(path: Path) -> tuple[list[str], list[str]]:
    text = path.read_text()
    mains = [html.unescape(m) for m in re.findall(r'<span class="full-tui-main">(.*?)</span>', text)]
    rails = [html.unescape(m) for m in re.findall(r'<span class="full-tui-rail[^"]*">(.*?)</span>', text)]
    if mains:
        return mains, rails
    m = re.search(r'<pre class="term-pre full-tui-pre">(.*?)</pre>', text, re.S)
    if not m:
        raise SystemExit("No full TUI content found")
    lines = m.group(1).split("\n")
    return [ln[:90] for ln in lines], [ln[91:120] for ln in lines]


def rebuild_from_flex(flex_path: Path) -> list[str]:
    mains, rails = extract_flex(flex_path)
    lines: list[str] = []
    for idx, (main, rail) in enumerate(zip(mains, rails)):
        row = idx + 1
        main = rebuild_main(main, row)
        if row == 1:
            rail_full = rail if len(rail) == 30 else ("┬" + rail.ljust(29)[:29])
        else:
            rail_full = rail.ljust(29)[:29]
        lines.append(build_full_line(main, rail_full, row, len(mains)))
    return lines


def patch_index(path: Path, lines: list[str]) -> None:
    text = path.read_text()
    pre_body = "\n".join(lines)
    block = (
        '      <div class="full-tui-terminal">\n'
        '        <div class="term-shell full-tui-shell">\n'
        f'          <pre class="term-pre full-tui-pre">{pre_body}</pre>\n'
        "        </div>\n"
        "      </div>"
    )
    pattern = r'      <div class="full-tui-terminal">.*?</div>\n      </div>'
    new_text, n = re.subn(pattern, block, text, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f"Could not patch index.html (matches={n})")
    path.write_text(new_text)


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    flex = root / "scripts" / "full_tui_source.html"
    if not flex.exists():
        flex = Path("/tmp/before_rebuild.html")
    lines = rebuild_from_flex(flex)
    for idx in range(5, 30):
        line = lines[idx]
        print(
            f"{idx+1:2}",
            {c: line[c - 1] for c in (28, 59, 81)},
            [i + 1 for i, ch in enumerate(line[:90]) if ch == "│"],
        )
    patch_index(root / "index.html", lines)
    print(f"\nPatched index.html ({len(lines)} lines)")
