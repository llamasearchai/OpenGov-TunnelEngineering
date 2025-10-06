from __future__ import annotations

from dataclasses import dataclass
import math

@dataclass(frozen=True)
class SettlementInputs:
    volume_loss_frac: float   # e.g., 0.01 for 1%
    radius_m: float
    cover_to_axis_m: float
    K: float = 0.5

@dataclass(frozen=True)
class SettlementTrough:
    Smax_m: float
    i_m: float

def settlement_trough(inp: SettlementInputs) -> SettlementTrough:
    A = math.pi * (inp.radius_m ** 2)
    i = max(0.1, inp.K * inp.cover_to_axis_m)
    Smax = (inp.volume_loss_frac * A) / (math.sqrt(2.0 * math.pi) * i)
    return SettlementTrough(Smax_m=float(Smax), i_m=float(i))

def settlement_at_x(trough: SettlementTrough, x_m: float) -> float:
    return float(trough.Smax_m * math.exp(-(x_m ** 2) / (2.0 * (trough.i_m ** 2))))
