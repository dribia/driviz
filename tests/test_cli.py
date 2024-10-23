"""Test the Command Line Interface."""

import sys
from importlib import reload
from unittest.mock import patch

from typer.testing import CliRunner

from driviz.cli import app

runner = CliRunner()


class TestInit:
    """Test the module initialization and version information."""

    @patch("importlib.metadata.version")
    def test_version_output(self, mock_version):
        """Test `__version__` when the package is found."""
        # Set the version
        version = "12.13.14"
        mock_version.return_value = version

        # Reload the CLI
        if "driviz" in sys.modules:
            del sys.modules["driviz"]

        from driviz import cli

        reload(cli)

        # Run the CLI
        result = runner.invoke(app, ["--version"])

        # Assert the output
        assert result.exit_code == 0
        assert result.stdout.strip() == f"driviz, version {version}"
