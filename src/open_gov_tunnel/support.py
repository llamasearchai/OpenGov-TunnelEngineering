from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class NATMSupport:
    shotcrete_mm: int
    bolt_length_m: float
    bolt_spacing_m: float
    lattice_girders: bool

def natm_support_from_rmr(rmr: float, diameter_m: float) -> NATMSupport:
    """
    Screening NATM support suggestion based on RMR class.
    """
    if rmr >= 80:
        return NATMSupport(shotcrete_mm=50, bolt_length_m=2.0, bolt_spacing_m=2.5, lattice_girders=False)
    if rmr >= 60:
        return NATMSupport(shotcrete_mm=75, bolt_length_m=3.0, bolt_spacing_m=2.0, lattice_girders=False)
    if rmr >= 40:
        return NATMSupport(shotcrete_mm=100, bolt_length_m=4.0, bolt_spacing_m=1.5, lattice_girders=True)
    if rmr >= 20:
        return NATMSupport(shotcrete_mm=150, bolt_length_m=4.0, bolt_spacing_m=1.2, lattice_girders=True)
    return NATMSupport(shotcrete_mm=200, bolt_length_m=5.0, bolt_spacing_m=1.0, lattice_girders=True)
