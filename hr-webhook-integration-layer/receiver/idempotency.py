"""
Idempotency keys for outbound calls.

Key = sha256(event_id + ":" + target_system + ":" + operation), truncated to
32 hex chars for readability in logs. Deterministic on purpose: the same
event replayed against the same target for the same operation always
produces the same key, so a crashed-and-retried flow can check "have I
already done this" before making the call again, and a genuine Remote
replay (see RESEARCH.md — replay is Remote's only recovery path for a
silently-dropped event) doesn't double-create an employment.

This key is NOT the same thing as the queue's dedup-by-event-id (queue.py).
That dedupes inbound deliveries — three Ashby events for one hire collapsing
to one queued job. This key guards outbound calls — the one queued job
possibly being processed more than once (worker crash, at-least-once retry)
without hitting Remote twice.
"""

import hashlib


def make_idempotency_key(event_id: str, target_system: str, operation: str) -> str:
    if not event_id or not target_system or not operation:
        raise ValueError("event_id, target_system, and operation are all required.")
    raw = f"{event_id}:{target_system}:{operation}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]
