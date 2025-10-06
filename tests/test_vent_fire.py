from __future__ import annotations

from open_gov_tunnel.ventilation import VentInputs, construction_vent_airflow
from open_gov_tunnel.fire_safety import EgressInputs, egress_screen

def test_vent_and_egress() -> None:
    v = construction_vent_airflow(VentInputs(diesel_kW=500.0, persons=20))
    assert v.airflow_m3_s > 0.0
    e = egress_screen(EgressInputs(tunnel_length_m=1000.0, max_spacing_m=152.0, walkway_speed_mps=1.2))
    assert e.required_passages >= 0
