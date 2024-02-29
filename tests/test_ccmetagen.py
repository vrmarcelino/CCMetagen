import unittest
import shutil
from pathlib import Path


class TestCCMetagen(unittest.TestCase):
    def test_import_ccmetagen_module(self):
        try:
            import ccmetagen
            _ = f"CCMetagen version {ccmetagen.__version__}." # noqa
        except ImportError:
            self.fail("Failed to import ccmetagen module")

    def test_ccmetagen_scripts_on_path(self):
        scripts = ["CCMetagen.py", "CCMetagen_extract_seqs.py", "CCMetagen_merge.py"]
        for script_name in scripts:
            try:
                # Check if the script is on the PATH
                script_path = shutil.which(script_name)
                self.assertIsNotNone(script_path, f"{script_name} not found on PATH")

                # Check if the script can be executed
                script_path = Path(script_path)
                self.assertTrue(script_path.is_file(), f"{script_name} is not a file")
                self.assertTrue(script_path.exists(), f"{script_name} does not exist")

            except Exception as e:
                self.fail(f"Unexpected error: {e}")


if __name__ == "__main__":
    unittest.main()
