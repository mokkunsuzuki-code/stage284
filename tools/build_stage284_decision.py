#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def build_decision(status: dict) -> dict:
    verified = status.get("verified")

    if not isinstance(verified, bool):
        raise ValueError("input JSON must contain boolean field: verified")

    decision = "accept" if verified else "reject"
    reason = "verified=true" if verified else "verified=false"

    result = {
        "decision": decision,
        "input": {
            "verified": verified
        },
        "policy": {
            "name": "boolean-verification-to-decision",
            "accept_if_verified": True,
            "reject_if_not_verified": True
        },
        "reason": reason
    }

    if "subject" in status:
        result["subject"] = status["subject"]

    if "verification_url" in status:
        result["verification_url"] = status["verification_url"]

    if "details" in status and isinstance(status["details"], dict):
        result["details"] = status["details"]

    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build Stage284 decision.json from verification_status.json"
    )
    parser.add_argument(
        "--input",
        default="out/verification/verification_status.json",
        help="Path to verification input JSON",
    )
    parser.add_argument(
        "--output",
        default="out/decision/decision.json",
        help="Path to output decision JSON",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    status = load_json(input_path)
    decision = build_decision(status)
    write_json(output_path, decision)

    print(f"[OK] wrote {output_path}")
    print(f"[OK] decision={decision['decision']}")


if __name__ == "__main__":
    main()
