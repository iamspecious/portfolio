"""
The person-mapping table. One row per human.

Identity resolution goes through this table only — never by matching email
inside a workflow. Emails change (personal → work, maiden → married, a typo
fixed six months in), and using them as a join key means a workflow that was
correct in March silently starts creating duplicate people in September.
The canonical_id is the one thing that's never supposed to change; every
platform-specific ID hangs off it.

`merged_into` exists for the case where two rows turn out to be the same
person — e.g. a candidate who was rejected, re-applied under a slightly
different name, and got hired the second time, producing two Ashby
candidate IDs for one eventual employee. Rather than delete a row (losing
the audit trail of "we once thought these were different people"), the
older row's status becomes 'merged' and merged_into points at the surviving
canonical_id. Every lookup function below follows a merge automatically so
callers never have to think about it.
"""

from receiver import db

LOOKUP_COLUMNS = {
    "hibob_employee_id": "hibob_employee_id",
    "ashby_candidate_id": "ashby_candidate_id",
    "ashby_application_id": "ashby_application_id",
    "remote_employment_id": "remote_employment_id",
}


def find_canonical_id(db_path: str, *, hibob_employee_id=None, ashby_candidate_id=None,
                       ashby_application_id=None, remote_employment_id=None) -> str | None:
    """
    Looks up a canonical_id by whichever platform ID is known, and follows
    merge chains to the current record. Returns None if no row matches —
    the caller then knows to create a new person rather than guessing.
    """
    lookups = {
        "hibob_employee_id": hibob_employee_id,
        "ashby_candidate_id": ashby_candidate_id,
        "ashby_application_id": ashby_application_id,
        "remote_employment_id": remote_employment_id,
    }
    with db.cursor(db_path) as cur:
        for column, value in lookups.items():
            if not value:
                continue
            cur.execute(
                f"SELECT canonical_id, merged_into FROM person_mapping WHERE {column} = ?",
                (value,),
            )
            row = cur.fetchone()
            if row:
                return _follow_merge(cur, row)
    return None


def _follow_merge(cur, row, _depth=0):
    if _depth > 10:
        raise RuntimeError("merged_into chain too deep — likely a cycle in person_mapping.")
    if row["merged_into"]:
        cur.execute(
            "SELECT canonical_id, merged_into FROM person_mapping WHERE canonical_id = ?",
            (row["merged_into"],),
        )
        next_row = cur.fetchone()
        if next_row:
            return _follow_merge(cur, next_row, _depth + 1)
    return row["canonical_id"]


def create_person(db_path: str, canonical_id: str, **fields) -> None:
    columns = ["canonical_id"] + list(fields.keys())
    placeholders = ", ".join("?" for _ in columns)
    values = [canonical_id] + list(fields.values())
    with db.cursor(db_path) as cur:
        cur.execute(
            f"INSERT INTO person_mapping ({', '.join(columns)}) VALUES ({placeholders})",
            values,
        )


def update_person(db_path: str, canonical_id: str, **fields) -> None:
    if not fields:
        return
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [canonical_id]
    with db.cursor(db_path) as cur:
        cur.execute(
            f"UPDATE person_mapping SET {set_clause}, updated_at = datetime('now') "
            f"WHERE canonical_id = ?",
            values,
        )


def merge(db_path: str, losing_canonical_id: str, winning_canonical_id: str, reason: str) -> None:
    """
    Marks losing_canonical_id as merged into winning_canonical_id. Does not
    delete or move data — the losing row's platform IDs stay in place so a
    future lookup by that old Ashby candidate ID still resolves (via the
    merge chain) to the current person.
    """
    if losing_canonical_id == winning_canonical_id:
        raise ValueError("Cannot merge a canonical_id into itself.")
    with db.cursor(db_path) as cur:
        cur.execute(
            "UPDATE person_mapping SET status = 'merged', merged_into = ?, "
            "updated_at = datetime('now') WHERE canonical_id = ?",
            (winning_canonical_id, losing_canonical_id),
        )
