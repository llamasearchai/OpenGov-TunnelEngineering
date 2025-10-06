from __future__ import annotations

from dataclasses import dataclass
import math

@dataclass(frozen=True)
class EgressInputs:
    tunnel_length_m: float
    max_spacing_m: float = 152.0  # ~500 ft
    walkway_speed_mps: float = 1.0

@dataclass(frozen=True)
class EgressResult:
    required_passages: int
    max_egress_time_s: float
    spacing_ok: bool

def egress_screen(inp: EgressInputs) -> EgressResult:
    n = max(0, math.ceil(inp.tunnel_length_m / inp.max_spacing_m) - 1)
    # worst-case egress distance ~ spacing/2
    t = (inp.max_spacing_m / 2.0) / max(0.1, inp.walkway_speed_mps)
    return EgressResult(required_passages=int(n), max_egress_time_s=float(t), spacing_ok=(n >= 0))
