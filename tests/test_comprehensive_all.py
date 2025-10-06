"""Comprehensive tests for 100% code coverage"""
from __future__ import annotations

import pytest
from pathlib import Path
from typer.testing import CliRunner
from open_gov_tunnel.classification import RMRInputs, rmr_score, QInputs, q_system
from open_gov_tunnel.support import natm_support_from_rmr
from open_gov_tunnel.tbm import TBMInputs, tbm_select
from open_gov_tunnel.lining import LiningInputs, lining_thickness
from open_gov_tunnel.groundwater import InflowInputs, inflow_per_length
from open_gov_tunnel.states import list_states, get_state
from open_gov_tunnel.reports import write_templates
from open_gov_tunnel.utils import g, gamma_w_kN_m3
from open_gov_tunnel.cli import app

runner = CliRunner()

# RMR Classification Tests
def test_rmr_class_i_very_good() -> None:
    rmr = rmr_score(RMRInputs(rqd=20, spacing_rating=20, condition_rating=20, groundwater_rating=10, orientation_rating=5, strength_rating=10))
    assert rmr.rmr >= 80
    assert "I (Very Good)" in rmr.class_label

def test_rmr_class_ii_good() -> None:
    rmr = rmr_score(RMRInputs(rqd=17, spacing_rating=15, condition_rating=20, groundwater_rating=10, orientation_rating=0, strength_rating=5))
    assert 60 <= rmr.rmr < 80
    assert "II (Good)" in rmr.class_label

def test_rmr_class_iii_fair() -> None:
    rmr = rmr_score(RMRInputs(rqd=13, spacing_rating=10, condition_rating=12, groundwater_rating=7, orientation_rating=-5, strength_rating=5))
    assert 40 <= rmr.rmr < 60
    assert "III (Fair)" in rmr.class_label

def test_rmr_class_iv_poor() -> None:
    rmr = rmr_score(RMRInputs(rqd=8, spacing_rating=8, condition_rating=10, groundwater_rating=4, orientation_rating=-10, strength_rating=3))
    assert 20 <= rmr.rmr < 40
    assert "IV (Poor)" in rmr.class_label

def test_rmr_class_v_very_poor() -> None:
    rmr = rmr_score(RMRInputs(rqd=3, spacing_rating=5, condition_rating=3, groundwater_rating=0, orientation_rating=-12, strength_rating=1))
    assert rmr.rmr < 20
    assert "V (Very Poor)" in rmr.class_label

# Q-system Tests
def test_q_system_excellent_very_good() -> None:
    q = q_system(QInputs(rqd=95, Jn=2, Jr=3, Ja=1, Jw=1, SRF=1))
    assert q.Q >= 10
    assert "Excellent/Very Good" in q.category

def test_q_system_good() -> None:
    q = q_system(QInputs(rqd=75, Jn=9, Jr=2, Ja=1, Jw=1, SRF=2))
    assert 4 <= q.Q < 10
    assert "Good" in q.category

def test_q_system_fair() -> None:
    q = q_system(QInputs(rqd=40, Jn=12, Jr=2, Ja=1, Jw=1, SRF=2))
    assert 1 <= q.Q < 4
    assert "Fair" in q.category

def test_q_system_poor() -> None:
    q = q_system(QInputs(rqd=50, Jn=12, Jr=1.5, Ja=2, Jw=0.66, SRF=5))
    assert 0.1 <= q.Q < 1
    assert "Poor" in q.category

def test_q_system_very_poor_extremely_poor() -> None:
    q = q_system(QInputs(rqd=25, Jn=20, Jr=1, Ja=4, Jw=0.5, SRF=10))
    assert q.Q < 0.1
    assert "Very Poor/Extremely Poor" in q.category

# NATM Support Tests
def test_natm_support_class_i() -> None:
    sup = natm_support_from_rmr(rmr=85, diameter_m=6.0)
    assert sup.shotcrete_mm == 50
    assert sup.lattice_girders is False

def test_natm_support_class_ii() -> None:
    sup = natm_support_from_rmr(rmr=65, diameter_m=6.0)
    assert sup.shotcrete_mm == 75
    assert sup.lattice_girders is False

def test_natm_support_class_iii() -> None:
    sup = natm_support_from_rmr(rmr=50, diameter_m=6.0)
    assert sup.shotcrete_mm == 100
    assert sup.lattice_girders is True

def test_natm_support_class_iv() -> None:
    sup = natm_support_from_rmr(rmr=30, diameter_m=6.0)
    assert sup.shotcrete_mm == 150
    assert sup.lattice_girders is True

def test_natm_support_class_v() -> None:
    sup = natm_support_from_rmr(rmr=15, diameter_m=6.0)
    assert sup.shotcrete_mm == 200
    assert sup.lattice_girders is True

# TBM Tests
def test_tbm_soft_high_water() -> None:
    t = tbm_select(TBMInputs(ground="soft", groundwater="high", boulders=False))
    assert "Slurry TBM" in t.recommended

def test_tbm_soft_wet() -> None:
    t = tbm_select(TBMInputs(ground="soft", groundwater="wet", boulders=False))
    assert "EPB TBM" in t.recommended

def test_tbm_mixed_boulders() -> None:
    t = tbm_select(TBMInputs(ground="mixed", groundwater="wet", boulders=True))
    assert "Convertible" in t.recommended or "Hard-Rock" in t.recommended

def test_tbm_mixed_no_boulders() -> None:
    t = tbm_select(TBMInputs(ground="mixed", groundwater="wet", boulders=False))
    assert "EPB" in t.recommended

def test_tbm_rock_high_water() -> None:
    t = tbm_select(TBMInputs(ground="rock", groundwater="high", boulders=False))
    assert "Shield TBM" in t.recommended

def test_tbm_rock_dry() -> None:
    t = tbm_select(TBMInputs(ground="rock", groundwater="dry", boulders=False))
    assert "Open TBM" in t.recommended

# Error Handling Tests
def test_lining_invalid_radius() -> None:
    with pytest.raises(ValueError):
        lining_thickness(LiningInputs(ground_pressure_kPa=300, radius_m=0, phi_resistance=0.7, fc_allow_kPa=15000.0))

def test_lining_invalid_fc_allow() -> None:
    with pytest.raises(ValueError):
        lining_thickness(LiningInputs(ground_pressure_kPa=300, radius_m=3.0, phi_resistance=0.7, fc_allow_kPa=0))

def test_lining_invalid_phi() -> None:
    with pytest.raises(ValueError):
        lining_thickness(LiningInputs(ground_pressure_kPa=300, radius_m=3.0, phi_resistance=0, fc_allow_kPa=15000.0))

def test_inflow_invalid_k() -> None:
    with pytest.raises(ValueError):
        inflow_per_length(InflowInputs(k_m_per_s=0, head_above_axis_m=10.0, radius_m=3.0, influence_radius_m=100.0))

def test_inflow_invalid_radius() -> None:
    with pytest.raises(ValueError):
        inflow_per_length(InflowInputs(k_m_per_s=1e-6, head_above_axis_m=10.0, radius_m=0, influence_radius_m=100.0))

def test_state_invalid_code() -> None:
    with pytest.raises(KeyError):
        get_state("TX")  # type: ignore

def test_inflow_drainage_factor_clamping() -> None:
    q1 = inflow_per_length(InflowInputs(k_m_per_s=1e-6, head_above_axis_m=10.0, radius_m=3.0, influence_radius_m=100.0, drainage_factor=1.5))
    q2 = inflow_per_length(InflowInputs(k_m_per_s=1e-6, head_above_axis_m=10.0, radius_m=3.0, influence_radius_m=100.0, drainage_factor=1.0))
    assert abs(q1.q_per_m3_s - q2.q_per_m3_s) < 1e-9

# States and Reports Tests
def test_list_states_returns_three() -> None:
    states = list_states()
    assert len(states) == 3

def test_get_state_california() -> None:
    ca = get_state("CA")
    assert ca.code == "CA"
    assert ca.name == "California"

def test_get_state_indiana() -> None:
    ind = get_state("IN")
    assert ind.code == "IN"

def test_get_state_ohio() -> None:
    oh = get_state("OH")
    assert oh.code == "OH"

def test_write_templates_creates_directory(tmp_path: Path) -> None:
    test_dir = tmp_path / "test_output"
    write_templates(test_dir)
    assert test_dir.exists()

def test_write_templates_creates_files(tmp_path: Path) -> None:
    test_dir = tmp_path / "test_output"
    write_templates(test_dir)
    assert (test_dir / "rmr_template.csv").exists()
    assert (test_dir / "inflow_template.csv").exists()

def test_utils_constants() -> None:
    assert g > 0
    assert gamma_w_kN_m3 > 0

# CLI Tests
def test_cli_rmr_command() -> None:
    r = runner.invoke(app, ["rmr", "--rqd", "60", "--spacing", "10", "--cond", "10", "--gw", "8", "--orient", "4", "--strength", "10"])
    assert r.exit_code == 0

def test_cli_qsystem_command() -> None:
    r = runner.invoke(app, ["qsystem", "--rqd", "60", "--Jn", "9", "--Jr", "2", "--Ja", "1", "--Jw", "1", "--SRF", "2"])
    assert r.exit_code == 0

def test_cli_support_command() -> None:
    r = runner.invoke(app, ["support", "--rmr", "65", "--D", "6"])
    assert r.exit_code == 0

def test_cli_lining_command() -> None:
    r = runner.invoke(app, ["lining", "--p", "300", "--r", "3", "--phi", "0.7", "--fc", "15000"])
    assert r.exit_code == 0

def test_cli_inflow_command() -> None:
    r = runner.invoke(app, ["inflow", "--k", "1e-6", "--head", "10", "--r", "3", "--R", "100"])
    assert r.exit_code == 0

def test_cli_settlement_command() -> None:
    r = runner.invoke(app, ["settlement", "--VL", "0.015", "--r", "3", "--cover", "15"])
    assert r.exit_code == 0

def test_cli_vent_command() -> None:
    r = runner.invoke(app, ["vent", "--kW", "500", "--persons", "20"])
    assert r.exit_code == 0

def test_cli_fire_egress_command() -> None:
    r = runner.invoke(app, ["fire-egress", "--length", "1000"])
    assert r.exit_code == 0

def test_cli_tbm_select_command() -> None:
    r = runner.invoke(app, ["tbm-select", "--ground", "soft", "--gw", "high"])
    assert r.exit_code == 0

def test_cli_cost_command() -> None:
    r = runner.invoke(app, ["cost", "--length", "1000", "--D", "6"])
    assert r.exit_code == 0

def test_cli_permits_command() -> None:
    r = runner.invoke(app, ["permits"])
    assert r.exit_code == 0

def test_cli_templates_command(tmp_path: Path) -> None:
    template_dir = tmp_path / "test_templates"
    r = runner.invoke(app, ["templates", "--folder", str(template_dir)])
    assert r.exit_code == 0
    assert template_dir.exists()
