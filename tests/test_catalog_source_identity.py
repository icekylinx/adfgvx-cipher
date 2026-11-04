"""Canonical source identity rejects duplicate rows and unsafe evidence aliases."""
from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from adfgvx import catalog


class CanonicalSourceIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(catalog.DATA.read_text())
        cls.aliases = json.loads(catalog.SOURCE_ALIASES.read_text())

    def load(self, data=None, aliases=None):
        with TemporaryDirectory(prefix="adfgvx-canonical-test-") as directory:
            root = Path(directory)
            source = root / "catalogue.json"
            register = root / "aliases.json"
            source.write_text(json.dumps(self.data if data is None else data))
            register.write_text(json.dumps(self.aliases if aliases is None else aliases))
            with patch.object(catalog, "DATA", source), patch.object(catalog, "SOURCE_ALIASES", register):
                return catalog.load_catalog()

    def test_every_reviewed_body_has_one_canonical_entry(self):
        data = self.load()
        account = catalog.physical_source_accounting(data)
        self.assertEqual(account["catalogue_entries"], 679)
        self.assertEqual(account["unique_physical_sources"], 679)
        self.assertEqual(account["challenge_entries"], 22)
        self.assertEqual(account["additional_physical_sources"], 657)
        rows = {r["id"]: r for group in ("challenge", "other") for r in data[group]}
        self.assertEqual({r["id"] for r in rows.values() if r["state"] == "OPEN"},
                         {"p73", "p170", "p198", "p70_B1", "p127_B2", "p145_A", "p194_D1"})
        self.assertNotIn("p132_B", rows)
        for ident in ("p137_A6", "p163_A16", "p84_C"):
            self.assertEqual(rows[ident]["state"], "CONDITIONAL")
        self.assertEqual(rows["p153a"]["state"], "PARTIAL")

    def test_even_a_registered_evidence_alias_cannot_be_a_second_row(self):
        for original, alias in (("p132", "p132_B"), ("p153a", "p153_C5")):
            with self.subTest(alias=alias):
                data = deepcopy(self.data)
                row = deepcopy(next(r for r in data["challenge"] if r["id"] == original))
                source = catalog.source_messages()[original]["source"]
                row.update(id=alias, printed_page=source["printed_page"],
                           source_section=source["section"], source_reviewed=True)
                row.pop("evidence_record_ids", None)
                data["other"].append(row)
                with self.assertRaisesRegex(AssertionError, "Duplicate physical source"):
                    self.load(data)

    def test_an_open_source_cannot_disappear_from_accounting(self):
        data = deepcopy(self.data)
        data["other"] = [r for r in data["other"] if r["id"] != "p70_B1"]
        with self.assertRaisesRegex(AssertionError, "every reviewed physical source"):
            self.load(data)

    def test_unknown_source_location_is_not_an_extra_body(self):
        data = deepcopy(self.data)
        row = next(r for r in data["other"] if r["id"] == "p194_D1")
        row["source_section"] = "D2"
        with self.assertRaisesRegex(AssertionError, "every reviewed physical source"):
            self.load(data)

    def test_alias_requires_exact_registered_literal_digest(self):
        aliases = deepcopy(self.aliases)
        aliases["records"][0]["literal_source_sha256"] = "0" * 64
        with self.assertRaisesRegex(AssertionError, "p132_B"):
            self.load(aliases=aliases)

    def test_alias_lookup_is_restricted_to_canonical_case_and_exact_path(self):
        canonical = next(r for r in self.data["challenge"] if r["id"] == "p132")
        path = "experiments/november_radio_service/certificates.json"
        self.assertEqual(catalog.evidence_record_id(canonical, path), "p132_B")
        self.assertEqual(catalog.evidence_record_id(canonical, "data/messages.json"), "p132")
        for wrong_case in (False, True):
            with self.subTest(wrong_case=wrong_case):
                data = deepcopy(self.data)
                row = next(r for r in data["challenge"] if r["id"] == ("p100" if wrong_case else "p132"))
                if wrong_case:
                    row["evidence"] = [path]
                    row["evidence_record_ids"] = {path: "p132_B"}
                else:
                    row["evidence_record_ids"]["data/messages.json"] = "p132_B"
                with self.assertRaisesRegex(AssertionError, "Unregistered evidence alias"):
                    self.load(data)

    def test_missing_alias_registration_is_not_silently_ignored(self):
        aliases = deepcopy(self.aliases)
        aliases["records"] = []
        with self.assertRaisesRegex(AssertionError, "Unregistered evidence alias"):
            self.load(aliases=aliases)

    def test_unknown_state_is_rejected(self):
        data = deepcopy(self.data)
        data["other"][0]["state"] = "SOLVED"
        with self.assertRaisesRegex(AssertionError, "Unknown catalogue state"):
            self.load(data)


if __name__ == "__main__":
    unittest.main()
