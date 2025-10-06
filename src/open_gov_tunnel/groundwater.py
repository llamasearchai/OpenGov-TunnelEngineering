from __future__ import annotations

from dataclasses import dataclass
import math

@dataclass(frozen=True)
class InflowInputs:
    k_m_per_s: float
    head_above_axis_m: float
    radius_m: float
    influence_radius_m: float
    drainage_factor: float = 1.0  # <1 if grouted/drained

@dataclass(frozen=True)
class InflowResult:
    q_per_m3_s: float

def inflow_per_length(inp: InflowInputs) -> InflowResult:
    if inp.k_m_per_s <= 0 or inp.radius_m <= 0 or inp.influence_radius_m <= inp.radius_m or inp.head_above_axis_m < 0:
        raise ValueError("Invalid inputs.")
    q = (2.0 * math.pi * inp.k_m_per_s * inp.head_above_axis_m) / math.log(inp.influence_radius_m / inp.radius_m)
    q *= max(0.0, min(1.0, inp.drainage_factor))
    return InflowResult(q_per_m3_s=float(q))
