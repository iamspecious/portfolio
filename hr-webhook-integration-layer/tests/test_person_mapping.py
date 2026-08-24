"""
Tests for identity resolution via the person-mapping table, including the
merge-chain lookup. Run: python -m unittest discover -s tests
"""

import os
import tempfile
import unittest

from receiver import db, person_mapping


class TestPersonMapping(unittest.TestCase):
    def setUp(self):
        fd, self.db_path = tempfile.mkstemp(suffix=".sqlite3")
        os.close(fd)
        db.init_db(self.db_path)

    def tearDown(self):
        os.remove(self.db_path)

    def test_create_and_find_by_each_platform_id(self):
        person_mapping.create_person(
            self.db_path, "person_001",
            ashby_candidate_id="cand_1", hibob_employee_id="emp_1",
            remote_employment_id="rem_1", work_email="jordan@example.test",
        )

        self.assertEqual(
            person_mapping.find_canonical_id(self.db_path, ashby_candidate_id="cand_1"),
            "person_001",
        )
        self.assertEqual(
            person_mapping.find_canonical_id(self.db_path, hibob_employee_id="emp_1"),
            "person_001",
        )
        self.assertEqual(
            person_mapping.find_canonical_id(self.db_path, remote_employment_id="rem_1"),
            "person_001",
        )

    def test_unknown_id_returns_none(self):
        self.assertIsNone(
            person_mapping.find_canonical_id(self.db_path, ashby_candidate_id="nope")
        )

    def test_merge_chain_resolves_to_surviving_record(self):
        person_mapping.create_person(self.db_path, "person_old", ashby_candidate_id="cand_old")
        person_mapping.create_person(self.db_path, "person_new", ashby_candidate_id="cand_new")
        person_mapping.merge(self.db_path, "person_old", "person_new", reason="duplicate application")

        # A lookup by the OLD candidate ID should still resolve — to the
        # surviving record, not the merged-away one.
        self.assertEqual(
            person_mapping.find_canonical_id(self.db_path, ashby_candidate_id="cand_old"),
            "person_new",
        )

    def test_cannot_merge_into_self(self):
        person_mapping.create_person(self.db_path, "person_x")
        with self.assertRaises(ValueError):
            person_mapping.merge(self.db_path, "person_x", "person_x", reason="bug")


if __name__ == "__main__":
    unittest.main()
