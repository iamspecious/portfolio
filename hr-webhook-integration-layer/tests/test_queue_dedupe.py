"""
Tests for the durable queue's two-level dedup: exact event-ID redelivery,
and Ashby's three-events-one-hire fan-out. Run:
  python -m unittest discover -s tests
"""

import os
import tempfile
import unittest

from receiver import db, queue
from receiver.simulators import ashby_payloads


class TestQueueDedupe(unittest.TestCase):
    def setUp(self):
        fd, self.db_path = tempfile.mkstemp(suffix=".sqlite3")
        os.close(fd)
        db.init_db(self.db_path)

    def tearDown(self):
        os.remove(self.db_path)

    def test_exact_redelivery_is_a_duplicate(self):
        result_1 = queue.enqueue(self.db_path, "evt_1", "hibob", "employee.hired", "{}")
        result_2 = queue.enqueue(self.db_path, "evt_1", "hibob", "employee.hired", "{}")

        self.assertEqual(result_1, "queued")
        self.assertEqual(result_2, "duplicate")

    def test_ashby_fan_out_collapses_to_one_run(self):
        """
        The case this project exists to handle: candidateHire also fires
        applicationUpdate and candidateStageChange. Three distinct event
        IDs, one applicationId. Only the first should come out 'queued';
        the other two should be recorded (for audit) but marked as skips.
        """
        events = ashby_payloads.candidate_hire_fan_out()
        results = []
        for event in events:
            event_id = ashby_payloads.extract_event_id(event)
            fan_out_key = ashby_payloads.extract_fan_out_key(event)
            result = queue.enqueue(
                self.db_path, event_id, "ashby", event["action"], "{}", fan_out_key=fan_out_key
            )
            results.append(result)

        self.assertEqual(results[0], "queued")
        self.assertEqual(results[1], "fan_out_skip")
        self.assertEqual(results[2], "fan_out_skip")

        # All three should still be recorded — this is dedup, not data loss.
        with db.cursor(self.db_path) as cur:
            cur.execute("SELECT COUNT(*) as n FROM webhook_events")
            self.assertEqual(cur.fetchone()["n"], 3)

        # Exactly one row should be ready for a worker to pick up.
        with db.cursor(self.db_path) as cur:
            cur.execute("SELECT COUNT(*) as n FROM webhook_events WHERE status = 'queued'")
            self.assertEqual(cur.fetchone()["n"], 1)

    def test_different_fan_out_keys_both_queue(self):
        r1 = queue.enqueue(self.db_path, "evt_a", "ashby", "candidateHire", "{}", fan_out_key="app_1")
        r2 = queue.enqueue(self.db_path, "evt_b", "ashby", "candidateHire", "{}", fan_out_key="app_2")
        self.assertEqual(r1, "queued")
        self.assertEqual(r2, "queued")


if __name__ == "__main__":
    unittest.main()
