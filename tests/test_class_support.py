from __future__ import annotations

from open_gov_tunnel.classification import RMRInputs, rmr_score, QInputs, q_system
from open_gov_tunnel.support import natm_support_from_rmr

def test_rmr_q_and_support() -> None:
    rmr = rmr_score(RMRInputs(rqd=60, spacing_rating=10, condition_rating=10, groundwater_rating=8, orientation_rating=4, strength_rating=10))
    assert 0 <= rmr.rmr <= 100
    q = q_system(QInputs(rqd=60, Jn=9, Jr=2, Ja=1, Jw=1, SRF=2))
    assert q.Q > 0
    sup = natm_support_from_rmr(rmr.rmr, diameter_m=6.0)
    assert sup.shotcrete_mm > 0
