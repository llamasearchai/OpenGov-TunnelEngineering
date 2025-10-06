from __future__ import annotations

from open_gov_tunnel.groundwater import InflowInputs, inflow_per_length

def test_inflow_positive() -> None:
    q = inflow_per_length(InflowInputs(k_m_per_s=1e-6, head_above_axis_m=10.0, radius_m=3.0, influence_radius_m=100.0, drainage_factor=0.8))
    assert q.q_per_m3_s > 0.0
