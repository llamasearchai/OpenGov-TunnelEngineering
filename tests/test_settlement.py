from __future__ import annotations

from open_gov_tunnel.settlement import SettlementInputs, settlement_trough, settlement_at_x

def test_settlement_trough() -> None:
    tr = settlement_trough(SettlementInputs(volume_loss_frac=0.015, radius_m=3.0, cover_to_axis_m=15.0, K=0.5))
    s0 = settlement_at_x(tr, 0.0)
    s10 = settlement_at_x(tr, 10.0)
    assert s0 > s10 >= 0.0
