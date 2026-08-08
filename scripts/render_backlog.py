#!/usr/bin/env python3
"""Render the detailed P2-P4 backlog from the machine roadmap."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Any


SECTIONS = {
    "P2": "Next",
    "P3": "Later",
    "P4": "Someday",
}


def clean_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"invalid {field}")
    return " ".join(value.split())


def project_name(payload: dict[str, Any]) -> str:
    """The project this roadmap describes.

    Taken from the payload rather than hardcoded. The monorepo copy of this
    file carried "sylveste" in three places, which is the single reason it
    could not move into interpath, where the same generator has to serve any
    project. sync-roadmap-json.sh always writes `project`, so this is a read,
    not a guess.
    """
    value = payload.get("project")
    if isinstance(value, str) and value.strip():
        return " ".join(value.split())
    return "project"


def collect_items(payload: dict[str, Any], default_module: str) -> list[dict[str, str]]:
    roadmap = payload.get("roadmap")
    if not isinstance(roadmap, dict):
        raise ValueError("missing roadmap object")

    items: list[dict[str, str]] = []
    seen: set[str] = set()
    for phase in ("now", "next", "later"):
        phase_items = roadmap.get(phase, [])
        if not isinstance(phase_items, list):
            raise ValueError(f"roadmap.{phase} must be an array")
        for raw in phase_items:
            if not isinstance(raw, dict):
                raise ValueError(f"roadmap.{phase} contains a non-object item")
            issue_id = clean_text(raw.get("id"), "issue id")
            normalized_id = issue_id.casefold()
            if normalized_id in seen:
                raise ValueError(f"duplicate issue id: {issue_id}")
            seen.add(normalized_id)

            priority = clean_text(raw.get("priority"), f"priority for {issue_id}")
            status = clean_text(raw.get("status", "open"), f"status for {issue_id}")
            if priority not in SECTIONS or status == "closed":
                continue
            items.append(
                {
                    "id": issue_id,
                    "title": clean_text(raw.get("title"), f"title for {issue_id}"),
                    "module": clean_text(raw.get("module", default_module), f"module for {issue_id}"),
                    "priority": priority,
                    "status": status,
                }
            )
    return items


def render(payload: dict[str, Any]) -> str:
    generated_at = clean_text(payload.get("generated_at"), "generated_at")
    synced_date = generated_at[:10]
    if len(synced_date) != 10:
        raise ValueError("invalid generated_at")

    project = project_name(payload)
    project_title = project[:1].upper() + project[1:]

    grouped: dict[str, dict[str, list[dict[str, str]]]] = {
        priority: defaultdict(list) for priority in SECTIONS
    }
    for item in collect_items(payload, project):
        grouped[item["priority"]][item["module"]].append(item)

    lines = [
        f"# {project_title} Backlog - Detailed Inventory",
        "",
        f"**Companion to:** [{project}-roadmap.md]({project}-roadmap.md) (strategic roadmap)",
        f"**Last synced:** {synced_date}",
        "",
        "This file contains every live P2-P4 item in the canonical Beads tracker.",
        "It is generated from [roadmap.json](roadmap.json); do not hand-edit it.",
    ]

    for priority, label in SECTIONS.items():
        lines.extend(["", "---", "", f"## {priority} - {label}"])
        modules = grouped[priority]
        if not modules:
            lines.extend(["", "No live items."])
            continue
        for module in sorted(modules, key=str.casefold):
            lines.extend(["", f"### {module}"])
            for item in sorted(modules[module], key=lambda value: value["id"].casefold()):
                status = item["status"]
                suffix = "" if status == "open" else f" _({status.replace('_', ' ')})_"
                lines.append(f"- **{item['id']}** {item['title']}{suffix}")

    return "\n".join(lines) + "\n"


def write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        delete=False,
    ) as handle:
        handle.write(content)
        temp_path = Path(handle.name)
    os.replace(temp_path, path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roadmap_json", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args(argv)

    try:
        payload = json.loads(args.roadmap_json.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("roadmap root must be an object")
        write_atomic(args.output, render(payload))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"render-backlog: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
