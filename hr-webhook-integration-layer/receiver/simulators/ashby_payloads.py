"""
Documented-payload simulator for Ashby.

Ashby has no public sandbox — there is no hosted environment a project like
this one can register against and receive real webhook traffic from. These
functions build payloads shaped the way Ashby's own webhook documentation
(developers.ashbyhq.com) describes them: the envelope fields (action,
webhookId, createdAt, data), the event type names (candidateHire,
applicationUpdate, candidateStageChange), and the nested candidate/
application object shapes.

Every value inside is synthetic. No real candidate, company, or job posting
exists anywhere in this data. Static copies of what these functions produce
live in fixtures/ for anyone who wants to look without running Python.

This module exists to produce REALISTIC INPUT for the receiver and the
dedup/fan-out logic to be tested against — it is not, and does not claim to
be, a live Ashby integration. See README.md's honesty note.
"""

import uuid
from datetime import datetime, timezone


def _now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def ping_event() -> dict:
    """
    The validation event Ashby sends when a webhook is first registered, to
    confirm the endpoint is reachable before enabling delivery for real.
    """
    return {
        "action": "ping",
        "webhookId": "wh_" + uuid.uuid4().hex[:12],
        "createdAt": _now_iso(),
        "data": {"message": "Ashby webhook ping"},
    }


def candidate_hire_fan_out(application_id: str = "app_9f2a1c7e4b3d",
                            candidate_id: str = "cand_5b7e21a0f114") -> list[dict]:
    """
    The case this project is built to survive: one real-world hiring
    decision, three separate webhook deliveries. All three carry the same
    applicationId — that's the fan_out_key the queue dedupes on (see
    receiver/queue.py). A naive integration that dedupes by event ID alone
    runs its downstream "new hire" workflow three times.

    Returns the three events in the order Ashby actually sends them:
    stage change first (moving to Hired), then the application update, then
    the dedicated hire event.
    """
    candidate = {
        "id": candidate_id,
        "name": "Jordan Ellery",
        "email": "jordan.ellery@example-candidate.test",
        "createdAt": "2026-06-02T09:14:00.000000Z",
    }
    application = {
        "id": application_id,
        "candidate": {"id": candidate_id},
        "job": {"id": "job_2c14e8a9", "title": "Senior Backend Engineer"},
        "status": "Hired",
    }

    stage_change = {
        "action": "candidateStageChange",
        "webhookId": "wh_" + uuid.uuid4().hex[:12],
        "createdAt": _now_iso(),
        "data": {
            "application": application,
            "candidate": candidate,
            "previousStage": {"title": "Offer"},
            "newStage": {"title": "Hired"},
        },
    }
    application_update = {
        "action": "applicationUpdate",
        "webhookId": "wh_" + uuid.uuid4().hex[:12],
        "createdAt": _now_iso(),
        "data": {
            "application": application,
            "candidate": candidate,
        },
    }
    candidate_hire = {
        "action": "candidateHire",
        "webhookId": "wh_" + uuid.uuid4().hex[:12],
        "createdAt": _now_iso(),
        "data": {
            "application": application,
            "candidate": candidate,
            "hiredAt": _now_iso(),
        },
    }
    return [stage_change, application_update, candidate_hire]


def extract_fan_out_key(event: dict) -> str | None:
    """
    Every Ashby event carries data.application.id. Using it as the
    fan_out_key is what lets three different event types for the same hire
    collapse into one downstream run.
    """
    return event.get("data", {}).get("application", {}).get("id")


def extract_event_id(event: dict) -> str:
    return event.get("webhookId")
