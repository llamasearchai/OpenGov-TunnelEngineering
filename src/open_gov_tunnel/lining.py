from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class LiningInputs:
    ground_pressure_kPa: float
    radius_m: float
    phi_resistance: float
    fc_allow_kPa: float
    t_min_m: float = 0.2

@dataclass(frozen=True)
class LiningResult:
    t_req_m: float
    OK: bool

def lining_thickness(inp: LiningInputs) -> LiningResult:
    if inp.radius_m <= 0 or inp.fc_allow_kPa <= 0 or inp.phi_resistance <= 0:
        raise ValueError("radius, fc_allow, phi must be > 0")
    t_req = (inp.ground_pressure_kPa * inp.radius_m) / (inp.phi_resistance * inp.fc_allow_kPa)
    t_use = max(inp.t_min_m, t_req)
    return LiningResult(t_req_m=float(t_use), OK=(t_req <= t_use + 1e-9))
