"""Summarize recorded Codex CLI runs without executing models or grading output."""

# cspell:ignore collab

import argparse
import json
import math
from pathlib import Path
import sys

TOOL_TYPES = {
    "command_execution", "file_change", "mcp_tool_call", "web_search", "collab_tool_call"
}
USAGE_FIELDS = ("input_tokens", "cached_input_tokens", "output_tokens")


def nonnegative(value, field, integer=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be a nonnegative number")
    if not math.isfinite(value) or value < 0 or (integer and not isinstance(value, int)):
        raise ValueError(f"Invalid {field}: {value}")
    return value


def summarize(run, base, rates):
    directory = base / run["path"]
    result = json.loads((directory / "result.json").read_text())
    usage = dict.fromkeys(USAGE_FIELDS, 0)
    tools = set()
    completed = 0
    started = 0
    failed = False
    missing_usage = False
    cache_writes = 0

    for line_number, line in enumerate((directory / "events.jsonl").read_text().splitlines(), 1):
        if not line.strip():
            continue
        event = json.loads(line)
        if not isinstance(event, dict):
            raise ValueError(f"Event {line_number} must be an object")
        kind = event.get("type")
        if kind == "turn.started":
            started += 1
        elif kind == "turn.failed":
            failed = True
        elif kind == "turn.completed":
            completed += 1
            current = event.get("usage") or {}
            if not all(field in current for field in USAGE_FIELDS):
                missing_usage = True
                continue
            for field in USAGE_FIELDS:
                usage[field] += nonnegative(current[field], field, integer=True)
            if current["cached_input_tokens"] > current["input_tokens"]:
                raise ValueError("cached_input_tokens exceeds input_tokens")
            cache_writes += nonnegative(current.get("cache_write_input_tokens", 0), "cache_write_input_tokens", integer=True)
        elif kind == "item.completed":
            item = event.get("item", {})
            if item.get("type") in TOOL_TYPES:
                tools.add((started, item.get("id", line_number), item["type"]))

    elapsed = nonnegative(result["elapsed_seconds"], "elapsed_seconds")
    if result["exit_code"] is not None and type(result["exit_code"]) is not int:
        raise ValueError("exit_code must be an integer or null")
    if type(result["timeout"]) is not bool:
        raise ValueError("timeout must be a boolean")
    complete = (
        result["exit_code"] == 0 and not result["timeout"] and not failed
        and completed > 0 and started <= completed and not missing_usage
    )
    cost = None
    if complete and rates is not None and cache_writes == 0:
        cost = (
            (usage["input_tokens"] - usage["cached_input_tokens"]) * rates["input"]
            + usage["cached_input_tokens"] * rates["cached_input"]
            + usage["output_tokens"] * rates["output"]
        ) / 1_000_000

    return {
        "id": run["id"], "variant": run["variant"], "case": run["case"],
        "measurement_complete": complete, "exit_code": result["exit_code"],
        "timeout": result["timeout"], "elapsed_seconds": elapsed,
        "tool_calls": len(tools), "observed_usage": usage,
        "cache_write_input_tokens": cache_writes,
        "total_tokens": usage["input_tokens"] + usage["output_tokens"] if complete else None,
        "api_equivalent_usd": cost,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text())
        rates = manifest.get("rates_per_million")
        if rates is not None:
            for field in ("input", "cached_input", "output"):
                nonnegative(rates[field], field)
        rows = []
        ids = set()
        for run in manifest["runs"]:
            if run["id"] in ids:
                raise ValueError(f"Duplicate run id: {run['id']}")
            ids.add(run["id"])
            rows.append(summarize(run, args.manifest.parent, rates))
        print(json.dumps({"rates_per_million": rates, "runs": rows}, ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Evaluation summary failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
