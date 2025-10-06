from __future__ import annotations

from typer.testing import CliRunner
from open_gov_tunnel.cli import app

runner = CliRunner()

def test_list_states() -> None:
    r = runner.invoke(app, ["list-states"])
    assert r.exit_code == 0
    assert "California" in r.stdout and "Indiana" in r.stdout and "Ohio" in r.stdout
