from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class RMRInputs:
    rqd: float           # 0..100
    spacing_rating: float
    condition_rating: float
    groundwater_rating: float
    orientation_rating: float
    strength_rating: float

@dataclass(frozen=True)
class RMRResult:
    rmr: float
    class_label: str

def rmr_score(inp: RMRInputs) -> RMRResult:
    rmr = max(0.0, min(100.0, inp.rqd + inp.spacing_rating + inp.condition_rating + inp.groundwater_rating + inp.orientation_rating + inp.strength_rating))
    if rmr >= 80:
        label = "I (Very Good)"
    elif rmr >= 60:
        label = "II (Good)"
    elif rmr >= 40:
        label = "III (Fair)"
    elif rmr >= 20:
        label = "IV (Poor)"
    else:
        label = "V (Very Poor)"
    return RMRResult(rmr=float(rmr), class_label=label)

@dataclass(frozen=True)
class QInputs:
    rqd: float
    Jn: float
    Jr: float
    Ja: float
    Jw: float
    SRF: float

@dataclass(frozen=True)
class QResult:
    Q: float
    category: str

def q_system(inp: QInputs) -> QResult:
    Q = (max(0.0, inp.rqd) / max(1e-6, inp.Jn)) * (max(1e-6, inp.Jr) / max(1e-6, inp.Ja)) * (max(1e-6, inp.Jw) / max(1e-6, inp.SRF))
    if Q >= 10:
        cat = "Excellent/Very Good"
    elif Q >= 4:
        cat = "Good"
    elif Q >= 1:
        cat = "Fair"
    elif Q >= 0.1:
        cat = "Poor"
    else:
        cat = "Very Poor/Extremely Poor"
    return QResult(Q=float(Q), category=cat)
