from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class VentInputs:
    diesel_kW: float
    persons: int
    base_per_kw_m3_s: float = 0.08
    per_person_m3_s: float = 0.006

@dataclass(frozen=True)
class VentResult:
    airflow_m3_s: float

def construction_vent_airflow(inp: VentInputs) -> VentResult:
    q = inp.base_per_kw_m3_s * max(0.0, inp.diesel_kW) + inp.per_person_m3_s * max(0, inp.persons)
    return VentResult(airflow_m3_s=float(q))
