#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def expected_decision(status: dict) -> dict:
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
        description="Verify Stage284 decision.json deterministically"
    )
    parser.add_argument(
        "--input",
        default="out/verification/verification_status.json",
        help="Path to verification input JSON",
    )
    parser.add_argument(
        "--decision",
        default="out/decision/decision.json",
        help="Path to decision JSON",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    decision_path = Path(args.decision)

    status = load_json(input_path)
    actual = load_json(decision_path)
    expected = expected_decision(status)

    if actual != expected:
        print("[ERROR] decision.json mismatch")
        print("expected:")
        print(json.dumps(expected, ensure_ascii=False, indent=2, sort_keys=True))
        print("actual:")
        print(json.dumps(actual, ensure_ascii=False, indent=2, sort_keys=True))
        raise SystemExit(1)

    print("[OK] decision.json verified")
    print(f"[OK] decision={actual['decision']}")


if __name__ == "__main__":
    main()
