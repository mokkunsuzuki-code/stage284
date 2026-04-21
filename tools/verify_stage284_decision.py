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
    verification_url = status.get("verification_url")

    if not isinstance(verified, bool):
        return {
            "decision": "reject",
            "reason": "invalid or missing 'verified'"
        }

    if not verification_url:
        return {
            "decision": "reject",
            "reason": "missing verification_url"
        }

    decision = "accept" if verified else "reject"
    reason = "verified=true" if verified else "verified=false"

    result = {
        "decision": decision,
        "input": {
            "verified": verified
        },
        "policy": {
            "name": "verified+url-required",
            "require_verification_url": True,
            "accept_if_verified": True
        },
        "reason": reason,
        "verification": {
            "url": verification_url
        }
    }

    if "subject" in status:
        result["subject"] = status["subject"]

    if "details" in status and isinstance(status["details"], dict):
        result["details"] = status["details"]

    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="out/verification/verification_status.json")
    parser.add_argument("--decision", default="out/decision/decision.json")
    args = parser.parse_args()

    status = load_json(Path(args.input))
    actual = load_json(Path(args.decision))
    expected = expected_decision(status)

    if actual != expected:
        print("[ERROR] mismatch")
        print("expected:", json.dumps(expected, indent=2, ensure_ascii=False))
        print("actual:", json.dumps(actual, indent=2, ensure_ascii=False))
        raise SystemExit(1)

    print("[OK] verified")
    print(f"[OK] decision={actual['decision']}")


if __name__ == "__main__":
    main()
