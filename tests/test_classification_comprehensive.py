from __future__ import annotations

import pytest
from open_gov_tunnel.classification import RMRInputs, rmr_score, QInputs, q_system


def test_rmr_class_i_very_good() -> None:
    """Test RMR Class I (Very Good) - RMR >= 80"""
    rmr = rmr_score(RMRInputs(rqd=20, spacing_rating=20, condition_rating=20, groundwater_rating=10, orientation_rating=5, strength_rating=10))
    assert rmr.rmr >= 80
    assert "I (Very Good)" in rmr.class_label


def test_rmr_class_ii_good() -> None:
    """Test RMR Class II (Good) - 60 <= RMR < 80"""
    rmr = rmr_score(RMRInputs(rqd=17, spacing_rating=15, condition_rating=20, groundwater_rating=10, orientation_rating=0, strength_rating=5))
    assert 60 <= rmr.rmr < 80
    assert "II (Good)" in rmr.class_label


def test_rmr_class_iii_fair() -> None:
    """Test RMR Class III (Fair) - 40 <= RMR < 60"""
    rmr = rmr_score(RMRInputs(rqd=13, spacing_rating=10, condition_rating=12, groundwater_rating=7, orientation_rating=-5, strength_rating=5))
    assert 40 <= rmr.rmr < 60
    assert "III (Fair)" in rmr.class_label


def test_rmr_class_iv_poor() -> None:
    """Test RMR Class IV (Poor) - 20 <= RMR < 40"""
    rmr = rmr_score(RMRInputs(rqd=8, spacing_rating=8, condition_rating=10, groundwater_rating=4, orientation_rating=-10, strength_rating=3))
    assert 20 <= rmr.rmr < 40
    assert "IV (Poor)" in rmr.class_label


def test_rmr_class_v_very_poor() -> None:
    """Test RMR Class V (Very Poor) - RMR < 20"""
    rmr = rmr_score(RMRInputs(rqd=3, spacing_rating=5, condition_rating=3, groundwater_rating=0, orientation_rating=-12, strength_rating=1))
    assert rmr.rmr < 20
    assert "V (Very Poor)" in rmr.class_label


def test_rmr_clamping_upper() -> None:
    """Test RMR clamping at 100"""
    rmr = rmr_score(RMRInputs(rqd=100, spacing_rating=50, condition_rating=50, groundwater_rating=50, orientation_rating=50, strength_rating=50))
    assert rmr.rmr == 100.0


def test_rmr_clamping_lower() -> None:
    """Test RMR clamping at 0"""
    rmr = rmr_score(RMRInputs(rqd=-50, spacing_rating=-50, condition_rating=-50, groundwater_rating=-50, orientation_rating=-50, strength_rating=-50))
    assert rmr.rmr == 0.0


def test_q_system_excellent_very_good() -> None:
    """Test Q-system Excellent/Very Good - Q >= 10"""
    q = q_system(QInputs(rqd=95, Jn=2, Jr=3, Ja=1, Jw=1, SRF=1))
    assert q.Q >= 10
    assert "Excellent/Very Good" in q.category


def test_q_system_good() -> None:
    """Test Q-system Good - 4 <= Q < 10"""
    q = q_system(QInputs(rqd=75, Jn=9, Jr=2, Ja=1, Jw=1, SRF=2))
    assert 4 <= q.Q < 10
    assert "Good" in q.category


def test_q_system_fair() -> None:
    """Test Q-system Fair - 1 <= Q < 4"""
    q = q_system(QInputs(rqd=40, Jn=12, Jr=2, Ja=1, Jw=1, SRF=2))
    assert 1 <= q.Q < 4
    assert "Fair" in q.category


def test_q_system_poor() -> None:
    """Test Q-system Poor - 0.1 <= Q < 1"""
    q = q_system(QInputs(rqd=50, Jn=12, Jr=1.5, Ja=2, Jw=0.66, SRF=5))
    assert 0.1 <= q.Q < 1
    assert "Poor" in q.category


def test_q_system_very_poor_extremely_poor() -> None:
    """Test Q-system Very Poor/Extremely Poor - Q < 0.1"""
    q = q_system(QInputs(rqd=25, Jn=20, Jr=1, Ja=4, Jw=0.5, SRF=10))
    assert q.Q < 0.1
    assert "Very Poor/Extremely Poor" in q.category


def test_q_system_zero_handling() -> None:
    """Test Q-system with zero inputs (should use minimum values)"""
    q = q_system(QInputs(rqd=0, Jn=0, Jr=0, Ja=0, Jw=0, SRF=0))
    assert q.Q >= 0.0
