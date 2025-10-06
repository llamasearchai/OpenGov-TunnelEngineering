from __future__ import annotations

from pathlib import Path
from typer.testing import CliRunner
from open_gov_tunnel.cli import app

runner = CliRunner()


def test_cli_rmr_command() -> None:
    """Test RMR CLI command"""
    r = runner.invoke(app, ["rmr", "--rqd", "60", "--spacing", "10", "--cond", "10", "--gw", "8", "--orient", "4", "--strength", "10"])
    assert r.exit_code == 0
    assert "RMR" in r.stdout


def test_cli_qsystem_command() -> None:
    """Test Q-system CLI command"""
    r = runner.invoke(app, ["qsystem", "--rqd", "60", "--Jn", "9", "--Jr", "2", "--Ja", "1", "--Jw", "1", "--SRF", "2"])
    assert r.exit_code == 0
    assert "Q" in r.stdout


def test_cli_support_command() -> None:
    """Test NATM support CLI command"""
    r = runner.invoke(app, ["support", "--rmr", "65", "--D", "6"])
    assert r.exit_code == 0
    assert "Shotcrete" in r.stdout


def test_cli_lining_command() -> None:
    """Test lining CLI command"""
    r = runner.invoke(app, ["lining", "--p", "300", "--r", "3", "--phi", "0.7", "--fc", "15000", "--tmin", "0.25"])
    assert r.exit_code == 0
    assert "thickness" in r.stdout.lower()


def test_cli_inflow_command() -> None:
    """Test inflow CLI command"""
    r = runner.invoke(app, ["inflow", "--k", "1e-6", "--head", "10", "--r", "3", "--R", "100", "--df", "0.8"])
    assert r.exit_code == 0
    assert "Inflow" in r.stdout


def test_cli_settlement_command() -> None:
    """Test settlement CLI command"""
    r = runner.invoke(app, ["settlement", "--VL", "0.015", "--r", "3", "--cover", "15", "--K", "0.5", "--x", "10"])
    assert r.exit_code == 0
    assert "Smax" in r.stdout


def test_cli_vent_command() -> None:
    """Test ventilation CLI command"""
    r = runner.invoke(app, ["vent", "--kW", "500", "--persons", "20"])
    assert r.exit_code == 0
    assert "Airflow" in r.stdout


def test_cli_fire_egress_command() -> None:
    """Test fire egress CLI command"""
    r = runner.invoke(app, ["fire-egress", "--length", "1000", "--spacing", "152", "--speed", "1.0"])
    assert r.exit_code == 0
    assert "passages" in r.stdout.lower()


def test_cli_tbm_select_command() -> None:
    """Test TBM selection CLI command"""
    r = runner.invoke(app, ["tbm-select", "--ground", "soft", "--gw", "high"])
    assert r.exit_code == 0
    assert "Recommended" in r.stdout


def test_cli_cost_command() -> None:
    """Test cost CLI command"""
    r = runner.invoke(app, ["cost", "--length", "1000", "--D", "6", "--complexity", "1.2", "--shafts", "2", "--shaftcost", "4000000"])
    assert r.exit_code == 0
    assert "Total" in r.stdout


def test_cli_permits_command() -> None:
    """Test permits CLI command with some missing permits"""
    r = runner.invoke(app, ["permits"])
    assert r.exit_code == 0
    # With defaults, should show READY or MISSING depending on default values
    assert "Permits Checklist" in r.stdout


def test_cli_templates_command(tmp_path: Path) -> None:
    """Test templates CLI command"""
    template_dir = tmp_path / "test_templates"
    r = runner.invoke(app, ["templates", "--folder", str(template_dir)])
    assert r.exit_code == 0
    assert template_dir.exists()
    assert (template_dir / "rmr_template.csv").exists()
    assert (template_dir / "inflow_template.csv").exists()
    assert (template_dir / "settlement_template.csv").exists()
    assert (template_dir / "cost_template.csv").exists()


def test_cli_permits_ready() -> None:
    """Test permits command - check it runs successfully"""
    r = runner.invoke(app, ["permits"])
    assert r.exit_code == 0
    # Should show either READY or MISSING
    assert ("READY" in r.stdout or "MISSING" in r.stdout)
