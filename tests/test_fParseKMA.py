import tempfile
import unittest
from pathlib import Path

from ccmetagen import fParseKMA

# Older KMA versions (no '## command' line): 6 metadata lines, header on line 7.
OLD_FORMAT_MAPSTAT = """## method\tKMA
## version\t1.2.11
## database\tncbi_nt_no_env_11jun2019
## fragmentCount\t21958
## bpTotal\t6222811
## date\t2021-01-01
# refSequence\treadCount\tfragmentCount\tmapScoreSum\trefCoveredPositions\trefConsensusSum\tbpTotal\tdepthVariance\tnucHighDepthVariance\tdepthMax\tsnpSum\tinsertSum\tdeletionSum\treadCountAln\tfragmentCountAln
some_template\t10\t5\t100\t50\t50\t500\t0.1\t0.1\t2\t0\t0\t0\t10\t5
"""

# KMA >=1.6.x adds a '## command' line, pushing the header down to line 8.
NEW_FORMAT_MAPSTAT = """## method\tKMA
## version\t1.6.15
## database\tncbi_nt_no_env_11jun2019
## fragmentCount\t21958
## bpTotal\t6222811
## date\t2026-09-22
## command\tkma -ipe "sample_1.fastq.gz" "sample_2.fastq.gz" -o "out" -t_db db -t 4 -1t1 -mem_mode -and -apm p -ef
# refSequence\treadCount\tfragmentCount\tmapScoreSum\trefCoveredPositions\trefConsensusSum\tbpTotal\tdepthVariance\tnucHighDepthVariance\tdepthMax\tsnpSum\tinsertSum\tdeletionSum\treadCountAln\tfragmentCountAln
some_template\t10\t5\t100\t50\t50\t500\t0.1\t0.1\t2\t0\t0\t0\t10\t5
"""


class TestParseMapstatHeader(unittest.TestCase):
    def _write(self, tmpdir, content):
        path = Path(tmpdir) / "sample.mapstat"
        path.write_text(content)
        return str(path)

    def test_old_format_six_metadata_lines(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            mapstat_fp = self._write(tmpdir, OLD_FORMAT_MAPSTAT)
            metadata, header_row = fParseKMA.parse_mapstat_header(mapstat_fp)

            self.assertEqual(header_row, 6)
            self.assertEqual(metadata["fragmentCount"], "21958")
            self.assertNotIn("command", metadata)

    def test_new_format_with_command_line(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            mapstat_fp = self._write(tmpdir, NEW_FORMAT_MAPSTAT)
            metadata, header_row = fParseKMA.parse_mapstat_header(mapstat_fp)

            self.assertEqual(header_row, 7)
            self.assertEqual(metadata["fragmentCount"], "21958")
            self.assertIn("-ipe", metadata["command"].split())

    def test_both_formats_agree_on_data_row(self):
        # Regardless of how many metadata lines precede it, pandas should be
        # able to read the actual data row using the returned header_row.
        import pandas as pd

        with tempfile.TemporaryDirectory() as tmpdir:
            for content in (OLD_FORMAT_MAPSTAT, NEW_FORMAT_MAPSTAT):
                mapstat_fp = self._write(tmpdir, content)
                metadata, header_row = fParseKMA.parse_mapstat_header(mapstat_fp)
                df = pd.read_csv(
                    mapstat_fp, sep="\t", index_col=0, header=header_row, encoding="latin1"
                )
                self.assertEqual(list(df["fragmentCount"]), [5])

    def test_missing_header_line_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            mapstat_fp = self._write(tmpdir, "## method\tKMA\n## version\t1.6.15\n")
            with self.assertRaises(ValueError):
                fParseKMA.parse_mapstat_header(mapstat_fp)


class TestTaxaColumnsAcceptMixedTypes(unittest.TestCase):
    # Regression test for a separate bug surfaced alongside the mapstat one:
    # populate_w_tax seeds its taxa columns (LCA_TaxId, Superkingdom, ...) with
    # "", then later assigns a mix of int taxids and strings like 'unk_taxid'
    # into them. Under pandas >=3.0, an all-"" column is inferred as a strict
    # StringDtype that raises TypeError the first time an int is assigned.
    # This doesn't call populate_w_tax directly (that needs a real ete3
    # NCBITaxa database), it isolates just the column-typing pattern it uses.
    def test_mixed_int_and_str_assignment_does_not_raise(self):
        import pandas as pd

        df = pd.DataFrame({"x": [1, 2]}).assign(LCA_TaxId="", Superkingdom="")
        df = df.astype({"LCA_TaxId": object, "Superkingdom": object})

        df.at[0, "LCA_TaxId"] = 12345
        df.at[1, "LCA_TaxId"] = "unk_taxid"

        self.assertEqual(df.at[0, "LCA_TaxId"], 12345)
        self.assertEqual(df.at[1, "LCA_TaxId"], "unk_taxid")


if __name__ == "__main__":
    unittest.main()
