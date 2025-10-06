from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class CostInputs:
    length_m: float
    diameter_m: float
    complexity: float = 1.0
    shaft_count: int = 2
    shaft_cost_usd: float = 5_000_000.0
    unit_cost_usd_per_m_small: float = 20_000.0   # D < 5 m
    unit_cost_usd_per_m_large: float = 40_000.0   # D >= 5 m

@dataclass(frozen=True)
class CostResult:
    tunnel_usd: float
    shafts_usd: float
    total_usd: float

def tunnel_cost(inp: CostInputs) -> CostResult:
    unit = inp.unit_cost_usd_per_m_large if inp.diameter_m >= 5.0 else inp.unit_cost_usd_per_m_small
    tun = unit * inp.length_m * max(0.5, inp.complexity)
    shafts = inp.shaft_count * inp.shaft_cost_usd
    return CostResult(tunnel_usd=float(tun), shafts_usd=float(shafts), total_usd=float(tun + shafts))
