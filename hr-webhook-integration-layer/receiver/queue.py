"""
Durable queue with dedup by event ID.

The case this exists to handle: Ashby fires candidateHire, applicationUpdate,
and candidateStageChange for a single hire action — three deliveries, three
distinct event IDs, one real-world event. Dedup by event ID alone doesn't
collapse that; each of the three has a unique ID and would sail through.

So dedup here works at two levels:
  1. event_id is the primary key — a literal redelivery of the exact same
     event (Ashby's own retry, or Remote replaying an event you already
     processed) is a no-op insert, caught by SQLite's PK constraint.
  2. fan_out_key groups distinct-but-related events that should collapse to
     one downstream run. For Ashby's three-event hire fan-out, the fan_out
     key is the applicationId — all three events carry it, so all three
     enqueue as separate rows (for audit — you can see all three arrived)
     but only the FIRST one to arrive for a given fan_out_key is marked
     ready for processing; the other two are recorded and skipped.
"""

from receiver import db


def enqueue(db_path: str, event_id: str, platform: str, event_type: str,
            payload_json: str, fan_out_key: str | None = None) -> str:
    """
    Returns one of: 'queued' (new event, ready to process),
                     'duplicate' (exact event_id already seen),
                     'fan_out_skip' (new event_id, but its fan_out_key
                                     already has a queued/processed sibling).
    """
    with db.cursor(db_path) as cur:
        cur.execute("SELECT 1 FROM webhook_events WHERE event_id = ?", (event_id,))
        if cur.fetchone():
            return "duplicate"

        status = "queued"
        if fan_out_key:
            cur.execute(
                "SELECT 1 FROM webhook_events WHERE fan_out_key = ? LIMIT 1",
                (fan_out_key,),
            )
            if cur.fetchone():
                status = "fan_out_skip"

        cur.execute(
            """INSERT INTO webhook_events
               (event_id, platform, event_type, payload_json, fan_out_key, status)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (event_id, platform, event_type, payload_json, fan_out_key, status),
        )
        return status


def next_queued(db_path: str) -> "sqlite3.Row | None":
    with db.cursor(db_path) as cur:
        cur.execute(
            "SELECT * FROM webhook_events WHERE status = 'queued' "
            "ORDER BY received_at ASC LIMIT 1"
        )
        return cur.fetchone()


def mark_processed(db_path: str, event_id: str) -> None:
    with db.cursor(db_path) as cur:
        cur.execute(
            "UPDATE webhook_events SET status = 'processed', "
            "processed_at = datetime('now') WHERE event_id = ?",
            (event_id,),
        )


def mark_failed(db_path: str, event_id: str, reason: str = "") -> None:
    with db.cursor(db_path) as cur:
        cur.execute(
            "UPDATE webhook_events SET status = 'failed', "
            "processed_at = datetime('now') WHERE event_id = ?",
            (event_id,),
        )
