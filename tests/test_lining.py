from __future__ import annotations

from open_gov_tunnel.lining import LiningInputs, lining_thickness

def test_lining_thickness() -> None:
    res = lining_thickness(LiningInputs(ground_pressure_kPa=300, radius_m=3.0, phi_resistance=0.7, fc_allow_kPa=15000.0, t_min_m=0.25))
    assert res.t_req_m >= 0.25
