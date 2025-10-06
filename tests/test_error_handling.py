from __future__ import annotations

import pytest
from open_gov_tunnel.lining import LiningInputs, lining_thickness
from open_gov_tunnel.groundwater import InflowInputs, inflow_per_length
from open_gov_tunnel.states import get_state


def test_lining_invalid_radius() -> None:
    """Test lining thickness with invalid radius"""
    with pytest.raises(ValueError, match="radius.*must be > 0"):
        lining_thickness(LiningInputs(ground_pressure_kPa=300, radius_m=0, phi_resistance=0.7, fc_allow_kPa=15000.0))


def test_lining_invalid_fc_allow() -> None:
    """Test lining thickness with invalid allowable stress"""
    with pytest.raises(ValueError, match="fc_allow.*must be > 0"):
        lining_thickness(LiningInputs(ground_pressure_kPa=300, radius_m=3.0, phi_resistance=0.7, fc_allow_kPa=0))


def test_lining_invalid_phi() -> None:
    """Test lining thickness with invalid resistance factor"""
    with pytest.raises(ValueError, match="phi must be > 0"):
        lining_thickness(LiningInputs(ground_pressure_kPa=300, radius_m=3.0, phi_resistance=0, fc_allow_kPa=15000.0))


def test_lining_negative_radius() -> None:
    """Test lining thickness with negative radius"""
    with pytest.raises(ValueError):
        lining_thickness(LiningInputs(ground_pressure_kPa=300, radius_m=-3.0, phi_resistance=0.7, fc_allow_kPa=15000.0))


def test_inflow_invalid_k() -> None:
    """Test inflow with invalid hydraulic conductivity"""
    with pytest.raises(ValueError, match="Invalid inputs"):
        inflow_per_length(InflowInputs(k_m_per_s=0, head_above_axis_m=10.0, radius_m=3.0, influence_radius_m=100.0))


def test_inflow_invalid_radius() -> None:
    """Test inflow with invalid radius"""
    with pytest.raises(ValueError, match="Invalid inputs"):
        inflow_per_length(InflowInputs(k_m_per_s=1e-6, head_above_axis_m=10.0, radius_m=0, influence_radius_m=100.0))


def test_inflow_invalid_influence_radius() -> None:
    """Test inflow with influence radius <= tunnel radius"""
    with pytest.raises(ValueError, match="Invalid inputs"):
        inflow_per_length(InflowInputs(k_m_per_s=1e-6, head_above_axis_m=10.0, radius_m=50.0, influence_radius_m=50.0))


def test_inflow_negative_head() -> None:
    """Test inflow with negative head"""
    with pytest.raises(ValueError, match="Invalid inputs"):
        inflow_per_length(InflowInputs(k_m_per_s=1e-6, head_above_axis_m=-10.0, radius_m=3.0, influence_radius_m=100.0))


def test_state_invalid_code() -> None:
    """Test get_state with invalid state code"""
    with pytest.raises(KeyError, match="Unsupported state"):
        get_state("TX")  # type: ignore


def test_inflow_drainage_factor_clamping() -> None:
    """Test that drainage factor is properly clamped to 0-1"""
    q1 = inflow_per_length(InflowInputs(k_m_per_s=1e-6, head_above_axis_m=10.0, radius_m=3.0, influence_radius_m=100.0, drainage_factor=1.5))
    q2 = inflow_per_length(InflowInputs(k_m_per_s=1e-6, head_above_axis_m=10.0, radius_m=3.0, influence_radius_m=100.0, drainage_factor=1.0))
    assert abs(q1.q_per_m3_s - q2.q_per_m3_s) < 1e-9
    
    q3 = inflow_per_length(InflowInputs(k_m_per_s=1e-6, head_above_axis_m=10.0, radius_m=3.0, influence_radius_m=100.0, drainage_factor=-0.5))
    assert q3.q_per_m3_s == 0.0
