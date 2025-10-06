from __future__ import annotations

from open_gov_tunnel.support import natm_support_from_rmr


def test_natm_support_class_i_very_good() -> None:
    """Test NATM support for Class I (RMR >= 80)"""
    sup = natm_support_from_rmr(rmr=85, diameter_m=6.0)
    assert sup.shotcrete_mm == 50
    assert sup.bolt_length_m == 2.0
    assert sup.bolt_spacing_m == 2.5
    assert sup.lattice_girders is False


def test_natm_support_class_ii_good() -> None:
    """Test NATM support for Class II (60 <= RMR < 80)"""
    sup = natm_support_from_rmr(rmr=65, diameter_m=6.0)
    assert sup.shotcrete_mm == 75
    assert sup.bolt_length_m == 3.0
    assert sup.bolt_spacing_m == 2.0
    assert sup.lattice_girders is False


def test_natm_support_class_iii_fair() -> None:
    """Test NATM support for Class III (40 <= RMR < 60)"""
    sup = natm_support_from_rmr(rmr=50, diameter_m=6.0)
    assert sup.shotcrete_mm == 100
    assert sup.bolt_length_m == 4.0
    assert sup.bolt_spacing_m == 1.5
    assert sup.lattice_girders is True


def test_natm_support_class_iv_poor() -> None:
    """Test NATM support for Class IV (20 <= RMR < 40)"""
    sup = natm_support_from_rmr(rmr=30, diameter_m=6.0)
    assert sup.shotcrete_mm == 150
    assert sup.bolt_length_m == 4.0
    assert sup.bolt_spacing_m == 1.2
    assert sup.lattice_girders is True


def test_natm_support_class_v_very_poor() -> None:
    """Test NATM support for Class V (RMR < 20)"""
    sup = natm_support_from_rmr(rmr=15, diameter_m=6.0)
    assert sup.shotcrete_mm == 200
    assert sup.bolt_length_m == 5.0
    assert sup.bolt_spacing_m == 1.0
    assert sup.lattice_girders is True


def test_natm_support_boundary_80() -> None:
    """Test boundary condition at RMR = 80"""
    sup = natm_support_from_rmr(rmr=80, diameter_m=6.0)
    assert sup.shotcrete_mm == 50
    assert sup.lattice_girders is False


def test_natm_support_boundary_60() -> None:
    """Test boundary condition at RMR = 60"""
    sup = natm_support_from_rmr(rmr=60, diameter_m=6.0)
    assert sup.shotcrete_mm == 75
    assert sup.lattice_girders is False


def test_natm_support_boundary_40() -> None:
    """Test boundary condition at RMR = 40"""
    sup = natm_support_from_rmr(rmr=40, diameter_m=6.0)
    assert sup.shotcrete_mm == 100
    assert sup.lattice_girders is True


def test_natm_support_boundary_20() -> None:
    """Test boundary condition at RMR = 20"""
    sup = natm_support_from_rmr(rmr=20, diameter_m=6.0)
    assert sup.shotcrete_mm == 150
    assert sup.lattice_girders is True
