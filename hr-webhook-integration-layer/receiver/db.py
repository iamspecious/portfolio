"""
SQLite schema and connection helper.

One file, three tables:
  - webhook_events   — durable queue + dedup ledger (queue.py)
  - person_mapping    — one row per human (person_mapping.py)
  - idempotent_calls    — outbound-call ledger keyed by idempotency key (flows/)

SQLite is enough here. This is a portfolio-scale demo, not a production
queue — the point being demonstrated is the dedup/idempotency logic itself,
not the storage engine. Swapping in Postgres later changes nothing above
this file.
"""

import sqlite3
from contextlib import contextmanager

SCHEMA = """
CREATE TABLE IF NOT EXISTS webhook_events (
    event_id        TEXT PRIMARY KEY,
    platform        TEXT NOT NULL,
    event_type      TEXT NOT NULL,
    received_at     TEXT NOT NULL DEFAULT (datetime('now')),
    payload_json     TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'queued',
    -- ties multiple raw deliveries to the same downstream unit of work,
    -- e.g. Ashby's candidateHire + applicationUpdate + candidateStageChange
    -- fan-out for one hire all resolve to the same fan_out_key.
    fan_out_key     TEXT,
    processed_at    TEXT
);

CREATE INDEX IF NOT EXISTS idx_webhook_events_fan_out
    ON webhook_events(fan_out_key);

CREATE TABLE IF NOT EXISTS person_mapping (
    canonical_id          TEXT PRIMARY KEY,
    hibob_employee_id      TEXT,
    ashby_candidate_id      TEXT,
    ashby_application_id     TEXT,
    remote_employment_id      TEXT,
    work_email               TEXT,
    personal_email             TEXT,
    employment_type              TEXT,
    country                        TEXT,
    start_date                       TEXT,
    status                             TEXT NOT NULL DEFAULT 'active',
    merged_into                          TEXT,
    created_at    TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_person_mapping_hibob   ON person_mapping(hibob_employee_id);
CREATE INDEX IF NOT EXISTS idx_person_mapping_ashby_c ON person_mapping(ashby_candidate_id);
CREATE INDEX IF NOT EXISTS idx_person_mapping_ashby_a ON person_mapping(ashby_application_id);
CREATE INDEX IF NOT EXISTS idx_person_mapping_remote  ON person_mapping(remote_employment_id);

CREATE TABLE IF NOT EXISTS idempotent_calls (
    idempotency_key   TEXT PRIMARY KEY,
    target_system     TEXT NOT NULL,
    operation         TEXT NOT NULL,
    event_id          TEXT NOT NULL,
    result_json       TEXT,
    made_at           TEXT NOT NULL DEFAULT (datetime('now'))
);
"""


def connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: str) -> None:
    conn = connect(db_path)
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()


@contextmanager
def cursor(db_path: str):
    conn = connect(db_path)
    try:
        cur = conn.cursor()
        yield cur
        conn.commit()
    finally:
        conn.close()
