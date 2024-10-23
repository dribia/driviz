"""Test the module initialization and version information."""

import sys
from importlib import reload
from importlib.metadata import PackageNotFoundError
from unittest.mock import patch


class TestInit:
    """Test the module initialization and version information."""

    @patch("importlib.metadata.version", side_effect=PackageNotFoundError)
    def test_version_not_found(self, mock_version):
        """Test `__version__` when the package is not found."""
        if "driviz" in sys.modules:
            del sys.modules["driviz"]

        import driviz

        reload(driviz)
        assert driviz.__version__ == "unknown"

    @patch("importlib.metadata.version")
    def test_version_found(self, mock_version):
        """Test `__version__` when the package is found."""
        mock_version.return_value = "0.1.0"
        if "driviz" in sys.modules:
            del sys.modules["driviz"]

        import driviz

        reload(driviz)
        assert driviz.__version__ == "0.1.0"
