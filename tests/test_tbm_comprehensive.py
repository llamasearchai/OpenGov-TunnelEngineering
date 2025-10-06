from __future__ import annotations

from open_gov_tunnel.tbm import TBMInputs, tbm_select


def test_tbm_soft_ground_high_water() -> None:
    """Test TBM selection for soft ground with high water"""
    t = tbm_select(TBMInputs(ground="soft", groundwater="high", boulders=False))
    assert "Slurry TBM" in t.recommended
    assert "slurry separation" in t.notes.lower()


def test_tbm_soft_ground_wet() -> None:
    """Test TBM selection for soft ground with wet conditions"""
    t = tbm_select(TBMInputs(ground="soft", groundwater="wet", boulders=False))
    assert "EPB TBM" in t.recommended
    assert "foam/polymer conditioning" in t.notes.lower()


def test_tbm_soft_ground_dry() -> None:
    """Test TBM selection for soft ground with dry conditions"""
    t = tbm_select(TBMInputs(ground="soft", groundwater="dry", boulders=False))
    assert "EPB TBM" in t.recommended


def test_tbm_mixed_ground_with_boulders() -> None:
    """Test TBM selection for mixed ground with boulders"""
    t = tbm_select(TBMInputs(ground="mixed", groundwater="wet", boulders=True))
    assert "Convertible" in t.recommended or "Hard-Rock" in t.recommended
    assert "boulders" in t.notes.lower()


def test_tbm_mixed_ground_no_boulders() -> None:
    """Test TBM selection for mixed ground without boulders"""
    t = tbm_select(TBMInputs(ground="mixed", groundwater="wet", boulders=False))
    assert "EPB" in t.recommended
    assert "face pressure" in t.notes.lower()


def test_tbm_rock_high_water() -> None:
    """Test TBM selection for rock with high water"""
    t = tbm_select(TBMInputs(ground="rock", groundwater="high", boulders=False))
    assert "Shield TBM" in t.recommended
    assert "grouting" in t.notes.lower()


def test_tbm_rock_dry() -> None:
    """Test TBM selection for rock with dry conditions"""
    t = tbm_select(TBMInputs(ground="rock", groundwater="dry", boulders=False))
    assert "Open TBM" in t.recommended
    assert "Competent rock" in t.notes


def test_tbm_rock_wet() -> None:
    """Test TBM selection for rock with wet conditions"""
    t = tbm_select(TBMInputs(ground="rock", groundwater="wet", boulders=False))
    assert "Open TBM" in t.recommended


def test_tbm_case_insensitive() -> None:
    """Test that ground and groundwater inputs are case insensitive"""
    t1 = tbm_select(TBMInputs(ground="SOFT", groundwater="HIGH", boulders=False))
    t2 = tbm_select(TBMInputs(ground="Soft", groundwater="High", boulders=False))
    assert t1.recommended == t2.recommended
