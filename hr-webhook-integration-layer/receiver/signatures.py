"""
Three webhook signature schemes, verified three different ways, on purpose.

The point of this module is that these functions are NOT interchangeable.
A shared verify_signature(algorithm, ...) helper was the obvious first
instinct and was deliberately not built — see DEVLOG.md. Each platform
signs a different thing, over a different encoding, with a different
header shape. Collapsing that into one function hides exactly the detail
that matters.

All three comparisons use hmac.compare_digest — never `==` on a signature.
"""

import hashlib
import hmac


class SignatureError(Exception):
    pass


def verify_remote(raw_body: bytes, timestamp: str, signature: str, secret: str) -> bool:
    """
    Remote: HMAC-SHA256, base16 (hex), computed over `raw_body + ":" + timestamp`.
    Header: X-Remote-Signature (signature), X-Remote-Timestamp (timestamp).

    Per Remote's docs (developer.remote.com/docs/verifying-webhooks), the
    timestamp is the time of the FIRST delivery attempt — a retried webhook
    for the same event keeps its original timestamp, which is what lets a
    receiver tell "old retry" from "genuinely new event" apart. Freshness
    checking (rejecting a timestamp older than some window) is the caller's
    job, not this function's — this function only proves the payload wasn't
    tampered with and did come from Remote.
    """
    if not signature or not timestamp:
        raise SignatureError("Missing X-Remote-Signature or X-Remote-Timestamp header.")

    signed_payload = raw_body + b":" + timestamp.encode("utf-8")
    expected = hmac.new(secret.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def verify_ashby(raw_body: bytes, header_value: str, secret: str) -> bool:
    """
    Ashby: HMAC-SHA256, hex, sent as "sha256=<hex>" in the Ashby-Signature header.
    Computed over the exact raw request bytes — not the parsed/re-serialised JSON,
    which can differ in whitespace and key order from what was actually signed.

    Per developers.ashbyhq.com/docs/authenticating-webhooks.
    """
    if not header_value:
        raise SignatureError("Missing Ashby-Signature header.")
    if not header_value.startswith("sha256="):
        raise SignatureError(f"Unexpected Ashby-Signature format: {header_value!r}")

    provided_hex = header_value[len("sha256="):]
    expected_hex = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected_hex, provided_hex)


def verify_hibob(raw_body: bytes, header_value: str, secret: str) -> bool:
    """
    HiBob: HMAC-SHA512, base64, in the Bob-Signature header. No algorithm
    prefix to strip — the header is the raw base64 digest, computed over
    the raw request body.

    Per apidocs.hibob.com/reference/getting-started-webhooks.
    """
    if not header_value:
        raise SignatureError("Missing Bob-Signature header.")

    import base64

    expected = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha512).digest()
    expected_b64 = base64.b64encode(expected).decode("ascii")
    # compare_digest works fine on equal-length strings; base64 digests of a
    # fixed-length HMAC are always the same length, so this is safe.
    return hmac.compare_digest(expected_b64, header_value)
