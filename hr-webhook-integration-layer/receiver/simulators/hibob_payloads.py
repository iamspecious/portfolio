"""
Documented-payload simulator for HiBob.

HiBob has no public sandbox either. These functions build payloads shaped
the way HiBob's Webhooks v2 documentation (apidocs.hibob.com) describes
them: the envelope (type, uuid, companyId, timestamp), and a payload object
carrying the changed entity.

Every value is synthetic. Static copies live in fixtures/. This module
produces realistic input for the receiver to be tested against — it does
not claim to be a live HiBob tenant. See README.md's honesty note.
"""

import uuid
from datetime import datetime, timezone


def _now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def ping_event() -> dict:
    """The test delivery HiBob sends when a webhook is first configured."""
    return {
        "type": "webhook.ping",
        "uuid": str(uuid.uuid4()),
        "companyId": "demo-co",
        "timestamp": _now_iso(),
        "payload": {"message": "HiBob webhook test delivery"},
    }


def employee_hired_event(employee_id: str = "hibob_emp_00417") -> dict:
    """
    Fires when the HR admin marks a new employee's start in Bob — the
    HiBob-side event this project's identity resolution has to tie back to
    the same person Ashby already knows as a candidate/application, and
    that Remote will eventually know as an employment. See
    receiver/person_mapping.py.
    """
    return {
        "type": "employee.hired",
        "uuid": str(uuid.uuid4()),
        "companyId": "demo-co",
        "timestamp": _now_iso(),
        "payload": {
            "employee": {
                "id": employee_id,
                "displayName": "Jordan Ellery",
                "email": "jordan.ellery@examplecorp.test",
                "startDate": "2026-07-01",
                "employmentType": "Full-time",
                "site": "Remote - Germany",
            }
        },
    }


def extract_event_id(event: dict) -> str:
    return event.get("uuid")
