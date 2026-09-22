import csv
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CCM_MERGE_SCRIPT = Path(__file__).resolve().parent.parent / "CCMetagen_merge.py"

HEADER = [
    "Closest_match",
    "Score",
    "Expected",
    "Template_length",
    "Template_Identity",
    "Template_Coverage",
    "Query_Identity",
    "Query_Coverage",
    "Depth",
    "q_value",
    "p_value",
    "LCA_TaxId",
    "Superkingdom",
    "Kingdom",
    "Phylum",
    "Class",
    "Order",
    "Family",
    "Genus",
    "Species",
]

# sampleA has one hit (Klebsiella), sampleB has two (E. coli and Klebsiella) --
# this is what previously crashed CCMetagen_merge.py's `groupby(axis=1)` call
# once concatenated, since both samples' frames carry duplicate-named
# taxonomic-rank columns that need collapsing back into one.
SAMPLE_A_ROWS = [
    [
        "573|Klebsiella pneumoniae",
        259203, 0, 4052, 100.0, 100.0, 100.0, 100.0, 886, 28707.86, 1e-26, 573,
        "unk_sk", "Pseudomonadati", "Pseudomonadota", "Gammaproteobacteria",
        "Enterobacterales", "Enterobacteriaceae", "Klebsiella", "Klebsiella pneumoniae",
    ],
]
SAMPLE_B_ROWS = [
    [
        "562|Escherichia coli",
        20167, 0, 2883, 31.77, 31.77, 100.0, 314.74, 70, 2237.9, 1e-26, 562,
        "unk_sk", "Pseudomonadati", "Pseudomonadota", "Gammaproteobacteria",
        "Enterobacterales", "Enterobacteriaceae", "Escherichia", "Escherichia coli",
    ],
    [
        "573|Klebsiella pneumoniae",
        67488, 0, 4709, 84.71, 85.43, 99.15, 117.05, 240, 6647.84, 1e-26, 573,
        "unk_sk", "Pseudomonadati", "Pseudomonadota", "Gammaproteobacteria",
        "Enterobacterales", "Enterobacteriaceae", "Klebsiella", "Klebsiella pneumoniae",
    ],
]


class TestCCMetagenMerge(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self._write_sample("sampleA.res.ccm.csv", SAMPLE_A_ROWS)
        self._write_sample("sampleB.res.ccm.csv", SAMPLE_B_ROWS)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _write_sample(self, filename, rows):
        path = Path(self.tmpdir) / filename
        with open(path, "w", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow(HEADER)
            writer.writerows(rows)

    def _run_merge(self, extra_args=()):
        out_prefix = str(Path(self.tmpdir) / "merged")
        subprocess.run(
            [sys.executable, str(CCM_MERGE_SCRIPT), "-i", self.tmpdir, "-o", out_prefix, *extra_args],
            check=True,
            capture_output=True,
            text=True,
        )
        return out_prefix + ".csv"

    def test_species_level_merge(self):
        out_fp = self._run_merge()
        with open(out_fp) as fh:
            rows = list(csv.DictReader(fh))

        by_species = {row["Species"]: row for row in rows}
        self.assertIn("Klebsiella pneumoniae", by_species)
        self.assertIn("Escherichia coli", by_species)
        self.assertEqual(float(by_species["Klebsiella pneumoniae"]["sampleA"]), 886.0)
        self.assertEqual(float(by_species["Klebsiella pneumoniae"]["sampleB"]), 240.0)
        # sampleA had no E. coli hit -- should be filled in as 0, not missing.
        self.assertEqual(float(by_species["Escherichia coli"]["sampleA"]), 0.0)
        self.assertEqual(float(by_species["Escherichia coli"]["sampleB"]), 70.0)

        # Exactly one column per taxonomic rank -- this is the bug: before the
        # fix, concatenating samples left duplicate rank columns uncollapsed.
        self.assertEqual(rows[0].keys().__len__(), len(HEADER[-8:]) + 2)  # 8 tax ranks + 2 samples

    def test_closest_match_level_merge(self):
        out_fp = self._run_merge(extra_args=["-t", "Closest_match"])
        with open(out_fp) as fh:
            rows = list(csv.DictReader(fh))

        self.assertIn("Closest_match", rows[0].keys())
        matches = {row["Closest_match"] for row in rows}
        self.assertIn("573|Klebsiella pneumoniae", matches)
        self.assertIn("562|Escherichia coli", matches)


if __name__ == "__main__":
    unittest.main()
