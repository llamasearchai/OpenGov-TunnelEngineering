from __future__ import annotations

from typer.testing import CliRunner
from open_gov_tunnel.cli import app

runner = CliRunner()


def test_cli_help_command() -> None:
    """Test the CLI help command"""
    r = runner.invoke(app, ["--help"])
    assert r.exit_code == 0
    assert "OpenGov-TunnelEngineering" in r.stdout
