"""
Unit tests for the three signature schemes. Run: python -m unittest discover -s tests
"""

import base64
import hashlib
import hmac
import unittest

from receiver import signatures


class TestRemoteSignature(unittest.TestCase):
    def test_valid_signature_accepted(self):
        secret = "remote_test_secret"
        body = b'{"id":"evt_1","type":"employment.created"}'
        timestamp = "1719900000"
        signed = body + b":" + timestamp.encode("utf-8")
        sig = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()

        self.assertTrue(signatures.verify_remote(body, timestamp, sig, secret))

    def test_tampered_body_rejected(self):
        secret = "remote_test_secret"
        body = b'{"id":"evt_1"}'
        timestamp = "1719900000"
        signed = body + b":" + timestamp.encode("utf-8")
        sig = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()

        tampered_body = b'{"id":"evt_2"}'
        self.assertFalse(signatures.verify_remote(tampered_body, timestamp, sig, secret))

    def test_missing_headers_raise(self):
        with self.assertRaises(signatures.SignatureError):
            signatures.verify_remote(b"{}", None, "abc", "secret")
        with self.assertRaises(signatures.SignatureError):
            signatures.verify_remote(b"{}", "123", None, "secret")


class TestAshbySignature(unittest.TestCase):
    def test_valid_signature_accepted(self):
        secret = "ashby_test_secret"
        body = b'{"action":"candidateHire"}'
        digest = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
        header = f"sha256={digest}"

        self.assertTrue(signatures.verify_ashby(body, header, secret))

    def test_wrong_prefix_raises(self):
        with self.assertRaises(signatures.SignatureError):
            signatures.verify_ashby(b"{}", "sha1=deadbeef", "secret")

    def test_tampered_body_rejected(self):
        secret = "ashby_test_secret"
        body = b'{"action":"candidateHire"}'
        digest = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
        header = f"sha256={digest}"

        self.assertFalse(signatures.verify_ashby(b'{"action":"tampered"}', header, secret))


class TestHiBobSignature(unittest.TestCase):
    def test_valid_signature_accepted(self):
        secret = "hibob_test_secret"
        body = b'{"type":"employee.hired"}'
        digest = hmac.new(secret.encode(), body, hashlib.sha512).digest()
        header = base64.b64encode(digest).decode("ascii")

        self.assertTrue(signatures.verify_hibob(body, header, secret))

    def test_tampered_body_rejected(self):
        secret = "hibob_test_secret"
        body = b'{"type":"employee.hired"}'
        digest = hmac.new(secret.encode(), body, hashlib.sha512).digest()
        header = base64.b64encode(digest).decode("ascii")

        self.assertFalse(signatures.verify_hibob(b'{"type":"tampered"}', header, secret))

    def test_missing_header_raises(self):
        with self.assertRaises(signatures.SignatureError):
            signatures.verify_hibob(b"{}", "", "secret")


if __name__ == "__main__":
    unittest.main()
