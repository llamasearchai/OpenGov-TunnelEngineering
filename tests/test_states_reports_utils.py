from __future__ import annotations

from pathlib import Path
from open_gov_tunnel.states import list_states, get_state
from open_gov_tunnel.reports import write_templates
from open_gov_tunnel.utils import g, gamma_w_kN_m3


def test_list_states_returns_three() -> None:
    """Test that list_states returns exactly 3 states"""
    states = list_states()
    assert len(states) == 3


def test_list_states_sorted() -> None:
    """Test that states are sorted by code"""
    states = list_states()
    codes = [s.code for s in states]
    assert codes == ["CA", "IN", "OH"]


def test_get_state_california() -> None:
    """Test getting California state profile"""
    ca = get_state("CA")
    assert ca.code == "CA"
    assert ca.name == "California"
    assert "Caltrans" in ca.agencies
    assert len(ca.notes) > 0


def test_get_state_indiana() -> None:
    """Test getting Indiana state profile"""
    ind = get_state("IN")
    assert ind.code == "IN"
    assert ind.name == "Indiana"
    assert "INDOT" in ind.agencies


def test_get_state_ohio() -> None:
    """Test getting Ohio state profile"""
    oh = get_state("OH")
    assert oh.code == "OH"
    assert oh.name == "Ohio"
    assert "ODOT" in oh.agencies


def test_write_templates_creates_directory(tmp_path: Path) -> None:
    """Test that write_templates creates output directory"""
    test_dir = tmp_path / "test_output"
    write_templates(test_dir)
    assert test_dir.exists()


def test_write_templates_creates_files(tmp_path: Path) -> None:
    """Test that all template files are created"""
    test_dir = tmp_path / "test_output"
    write_templates(test_dir)
    assert (test_dir / "rmr_template.csv").exists()
    assert (test_dir / "inflow_template.csv").exists()
    assert (test_dir / "settlement_template.csv").exists()
    assert (test_dir / "cost_template.csv").exists()


def test_write_templates_file_contents(tmp_path: Path) -> None:
    """Test that template files have correct headers"""
    test_dir = tmp_path / "test_output"
    write_templates(test_dir)
    
    rmr_content = (test_dir / "rmr_template.csv").read_text()
    assert "rqd" in rmr_content
    assert "spacing_rating" in rmr_content
    
    inflow_content = (test_dir / "inflow_template.csv").read_text()
    assert "k_m_per_s" in inflow_content
    assert "head_above_axis_m" in inflow_content
    
    settlement_content = (test_dir / "settlement_template.csv").read_text()
    assert "volume_loss_frac" in settlement_content
    assert "radius_m" in settlement_content
    
    cost_content = (test_dir / "cost_template.csv").read_text()
    assert "length_m" in cost_content
    assert "diameter_m" in cost_content


def test_write_templates_existing_directory(tmp_path: Path) -> None:
    """Test that write_templates works with existing directory"""
    test_dir = tmp_path / "test_output"
    test_dir.mkdir()
    write_templates(test_dir)
    assert (test_dir / "rmr_template.csv").exists()


def test_utils_constants() -> None:
    """Test that utility constants are defined"""
    assert g > 0
    assert gamma_w_kN_m3 > 0
    assert abs(g - 9.80665) < 0.001
    assert abs(gamma_w_kN_m3 - 9.81) < 0.01
