from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Literal

StateCode = Literal["CA", "IN", "OH"]

@dataclass(frozen=True)
class StateProfile:
    code: StateCode
    name: str
    agencies: List[str]
    notes: str

def _ca() -> StateProfile:
    return StateProfile(
        code="CA",
        name="California",
        agencies=["Caltrans", "CPUC (rail)", "RWQCB/USACE", "Local AHJs"],
        notes="NEPA/CEQA, environmental and water permits; seismic and faulting considerations.",
    )

def _in_() -> StateProfile:
    return StateProfile(
        code="IN",
        name="Indiana",
        agencies=["INDOT", "IDEM/USACE", "Local AHJs"],
        notes="Glacial tills and soft ground; groundwater control and winter operations.",
    )

def _oh() -> StateProfile:
    return StateProfile(
        code="OH",
        name="Ohio",
        agencies=["ODOT", "OEPA/USACE", "Local AHJs"],
        notes="Karst pockets in some regions; Great Lakes influence on groundwater.",
    )

_REGISTRY: Dict[StateCode, StateProfile] = {"CA": _ca(), "IN": _in_(), "OH": _oh()}

def list_states() -> list[StateProfile]:
    return [p for _, p in sorted(_REGISTRY.items(), key=lambda kv: kv[0])]

def get_state(code: StateCode) -> StateProfile:
    if code not in _REGISTRY:
        raise KeyError(f"Unsupported state '{code}'. Supported: {', '.join(_REGISTRY.keys())}")
    return _REGISTRY[code]
