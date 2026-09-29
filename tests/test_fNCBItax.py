import unittest
from unittest import mock

from ccmetagen import cTaxInfo, fNCBItax

# Minimal lineages as returned by ete3's NCBITaxa: {taxid: (name, rank)}, root first.

# NCBI taxonomy since 2025: 'superkingdom' renamed to 'domain'.
ECOLI_NEW = {
    1: ("root", "no rank"),
    131567: ("cellular organisms", "cellular root"),
    2: ("Bacteria", "domain"),
    3379134: ("Pseudomonadati", "kingdom"),
    1224: ("Pseudomonadota", "phylum"),
    1236: ("Gammaproteobacteria", "class"),
    91347: ("Enterobacterales", "order"),
    543: ("Enterobacteriaceae", "family"),
    561: ("Escherichia", "genus"),
    562: ("Escherichia coli", "species"),
}

# Older ete3 databases: 'superkingdom' rank, no bacterial kingdom.
ECOLI_OLD = {
    1: ("root", "no rank"),
    131567: ("cellular organisms", "no rank"),
    2: ("Bacteria", "superkingdom"),
    1224: ("Pseudomonadota", "phylum"),
    1236: ("Gammaproteobacteria", "class"),
    91347: ("Enterobacterales", "order"),
    543: ("Enterobacteriaceae", "family"),
    561: ("Escherichia", "genus"),
    562: ("Escherichia coli", "species"),
}

# New taxonomy: the Viruses node is root-level, with realms below it.
HHV1_NEW = {
    1: ("root", "no rank"),
    10239: ("Viruses", "acellular root"),
    2731341: ("Duplodnaviria", "realm"),
    2731360: ("Heunggongvirae", "kingdom"),
    2731361: ("Peploviricota", "phylum"),
    2731363: ("Herviviricetes", "class"),
    548681: ("Herpesvirales", "order"),
    10292: ("Orthoherpesviridae", "family"),
    10294: ("Simplexvirus", "genus"),
    3050292: ("Simplexvirus humanalpha1", "species"),
}


def _fake_ncbitaxa(lineage_table):
    ncbi = mock.Mock()
    ncbi.get_lineage.return_value = list(lineage_table)
    ncbi.get_rank.side_effect = lambda ids: {t: lineage_table[t][1] for t in ids}
    ncbi.get_taxid_translator.side_effect = lambda ids: {t: lineage_table[t][0] for t in ids}
    return ncbi


class TestLineageExtractor(unittest.TestCase):
    def _extract(self, lineage_table):
        query_taxid = list(lineage_table)[-1]
        with mock.patch.object(fNCBItax, "NCBITaxa", return_value=_fake_ncbitaxa(lineage_table)):
            return fNCBItax.lineage_extractor(query_taxid, cTaxInfo.TaxInfo())

    def test_domain_rank_fills_superkingdom(self):
        info = self._extract(ECOLI_NEW)
        self.assertEqual(info.Superkingdom, "Bacteria")
        self.assertEqual(info.Superkingdom_TaxId, 2)
        self.assertEqual(info.Kingdom, "Pseudomonadati")
        self.assertEqual(info.Species, "Escherichia coli")

    def test_old_superkingdom_rank_still_supported(self):
        info = self._extract(ECOLI_OLD)
        self.assertEqual(info.Superkingdom, "Bacteria")
        self.assertEqual(info.Superkingdom_TaxId, 2)
        self.assertEqual(info.Kingdom, "unk_k")

    def test_viruses_identified_without_domain_rank(self):
        info = self._extract(HHV1_NEW)
        self.assertEqual(info.Superkingdom, "Viruses")
        self.assertEqual(info.Superkingdom_TaxId, 10239)
        self.assertEqual(info.Kingdom, "Heunggongvirae")


if __name__ == "__main__":
    unittest.main()
