"""
The one end-to-end flow: simulated hire -> fetch Remote's live country JSON
schema -> validate the payload against it -> create the employment in the
Remote sandbox.

Dry-run is on by default (see config.py — DRY_RUN unset or anything other
than the literal string "false" stays dry). In dry-run, every call that
would write to Remote is logged with exactly what it would have sent, and
nothing is sent. The schema fetch and validation still happen for real —
only the write is gated, because the point of dry-run is "prove the
payload is correct without touching anything," not "skip the interesting
part."

Idempotency: the key is derived from (event_id, target_system, operation)
via idempotency.py, and checked against the idempotent_calls table before
any write. A hire flow re-run for the same event — because a worker
crashed and restarted, or because Remote's replay endpoint redelivered an
event this integration already handled — does not create a second
employment for the same person.
"""

import json

from receiver import db
from receiver.idempotency import make_idempotency_key
from receiver.platforms.remote_client import RemoteClient


class SchemaValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors
        super().__init__(f"Payload failed schema validation: {errors}")


def _minimal_validate(payload: dict, schema: dict) -> list:
    """
    A deliberately small JSON Schema subset: checks `required` fields are
    present and, where `properties[<field>].type` is given, that the
    Python type roughly matches. This is NOT a full draft-07/2020-12
    validator — no $ref, no nested schema composition, no format
    validators. That's a real limitation, not an oversight: a full
    implementation is a solved problem (the `jsonschema` package), and
    reimplementing it badly would be worse than reimplementing it
    honestly-partially and saying so. See DEVLOG.md and README.md
    Constraints.
    """
    errors = []
    required = schema.get("required", [])
    for field in required:
        if field not in payload or payload[field] in (None, ""):
            errors.append(f"missing required field: {field}")

    type_map = {"string": str, "integer": int, "number": (int, float), "boolean": bool}
    properties = schema.get("properties", {})
    for field, spec in properties.items():
        if field not in payload:
            continue
        expected = type_map.get(spec.get("type"))
        if expected and not isinstance(payload[field], expected):
            errors.append(
                f"field {field!r} expected type {spec.get('type')}, "
                f"got {type(payload[field]).__name__}"
            )
    return errors


def run_hire_flow(config, event_id: str, hire_payload: dict) -> dict:
    """
    hire_payload is expected to look like a Remote employment-creation
    payload — country_code, full_name, personal_email, job_title, type,
    provisional_start_date — as assembled upstream from the person-mapping
    row plus whatever the triggering HR event supplied.

    Returns a result dict describing what happened, suitable for logging
    or for the failure-philosophy demo to print.
    """
    client = RemoteClient(config)
    country_code = hire_payload.get("country_code")
    if not country_code:
        raise ValueError("hire_payload is missing country_code — cannot fetch a schema for it.")

    print(f"[hire_flow] fetching live employment schema for country={country_code} "
          f"from {config.remote_base_url} ...")
    schema = client.get_country_schema(country_code)

    errors = _minimal_validate(hire_payload, schema)
    if errors:
        raise SchemaValidationError(errors)
    print(f"[hire_flow] payload validated against the live {country_code} schema — no errors.")

    idempotency_key = make_idempotency_key(event_id, "remote", "create_employment")

    with db.cursor(config.db_path) as cur:
        cur.execute(
            "SELECT result_json FROM idempotent_calls WHERE idempotency_key = ?",
            (idempotency_key,),
        )
        existing = cur.fetchone()
    if existing:
        print(f"[hire_flow] idempotency key {idempotency_key} already used — "
              f"skipping create, returning the original result.")
        return {"status": "already_done", "result": json.loads(existing["result_json"])}

    if config.dry_run:
        print(f"[hire_flow] DRY RUN — would POST /v1/employments to {config.remote_base_url} "
              f"with idempotency_key={idempotency_key}:")
        print(json.dumps(hire_payload, indent=2))
        return {"status": "dry_run", "would_send": hire_payload, "idempotency_key": idempotency_key}

    result = client.create_employment(hire_payload)
    with db.cursor(config.db_path) as cur:
        cur.execute(
            "INSERT INTO idempotent_calls (idempotency_key, target_system, operation, "
            "event_id, result_json) VALUES (?, ?, ?, ?, ?)",
            (idempotency_key, "remote", "create_employment", event_id, json.dumps(result)),
        )
    print(f"[hire_flow] employment created: {result.get('id', '(no id in response)')}")
    return {"status": "created", "result": result, "idempotency_key": idempotency_key}
