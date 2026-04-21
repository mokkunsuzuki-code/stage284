# QSP / VEP / Stage284

## Decision System (ACCEPT / REJECT)

Stage284 converts a verification result into a protocol decision.

Before this stage, the system could say:

- verified

Stage284 makes that machine-readable as:

```json
{
  "decision": "accept"
}

This is important because a protocol should not stop at human-readable status.
It should return an explicit decision that software, policy, and downstream systems can consume.

Core Idea

Input:

{
  "verified": true
}

Output:

{
  "decision": "accept"
}

If verification is false, the result becomes:

{
  "decision": "reject"
}
What This Stage Proves
Verification status can be converted into a deterministic protocol decision
The decision is machine-readable
The decision can be reproduced locally and in CI
The system now behaves more like a protocol than a display layer
Decision Policy

Stage284 uses a simple deterministic policy:

verified = true → accept
verified = false → reject

This is intentionally minimal.

The value of this stage is not policy complexity.
The value is that the system now returns a formal decision object.

Files
out/verification/verification_status.json
input status
tools/build_stage284_decision.py
builds decision.json
tools/verify_stage284_decision.py
verifies deterministic correctness
out/decision/decision.json
final protocol decision
.github/workflows/stage284-decision.yml
CI reproduction and verification
Local Run
python3 tools/build_stage284_decision.py
python3 tools/verify_stage284_decision.py
cat out/decision/decision.json
Example Output
{
  "decision": "accept",
  "input": {
    "verified": true
  },
  "policy": {
    "accept_if_verified": true,
    "name": "boolean-verification-to-decision",
    "reject_if_not_verified": true
  },
  "reason": "verified=true"
}
Why This Matters

A "verified" badge is a display result.

A protocol decision such as accept or reject is an actionable result.

That makes Stage284 closer to a real decision protocol.

Limitations

This stage does not yet implement:

weighted trust scoring
pending / indeterminate states
multi-condition policy composition
threshold governance

It is a minimal protocol decision layer.

License

MIT License

Copyright (c) 2025
