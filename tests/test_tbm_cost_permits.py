from __future__ import annotations

from open_gov_tunnel.tbm import TBMInputs, tbm_select
from open_gov_tunnel.cost import CostInputs, tunnel_cost
from open_gov_tunnel.permits import PermitsInputs, permits_check

def test_tbm_cost_permits() -> None:
    t = tbm_select(TBMInputs(ground="soft", groundwater="high", boulders=False))
    assert "Slurry" in t.recommended or "EPB" in t.recommended
    c = tunnel_cost(CostInputs(length_m=1000.0, diameter_m=6.0, complexity=1.2, shaft_count=2, shaft_cost_usd=4_000_000.0))
    assert c.total_usd > 0.0
    p = permits_check(PermitsInputs(nepa_or_ceqa=True, usace_404_401=False, groundwater_discharge=True, railroad_coord=False, utility_relocations=True, fire_authority=True))
    assert p.ready is False
    assert "usace_404_401" in p.missing
