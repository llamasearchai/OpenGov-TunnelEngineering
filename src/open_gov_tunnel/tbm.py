from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class TBMInputs:
    ground: str           # 'rock','mixed','soft'
    groundwater: str      # 'dry','wet','high'
    boulders: bool = False

@dataclass(frozen=True)
class TBMResult:
    recommended: str
    notes: str

def tbm_select(inp: TBMInputs) -> TBMResult:
    g = inp.ground.lower()
    w = inp.groundwater.lower()
    if g == "soft":
        if w == "high":
            return TBMResult("Slurry TBM", "High head/flows; slurry separation and pressure control.")
        return TBMResult("EPB TBM", "Fine-grained soils or mixed fill; foam/polymer conditioning.")
    if g == "mixed":
        if inp.boulders:
            return TBMResult("Convertible EPB/Hard-Rock", "Mixed face with boulders; robust cutterhead and conditioning.")
        return TBMResult("EPB", "Mixed geology; face pressure recommended.")
    # rock
    if w == "high":
        return TBMResult("Single/Double Shield TBM", "Rock with water; pre-excavation grouting and robust sealing.")
    return TBMResult("Open TBM", "Competent rock, low water inflow.")
