from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class PermitsInputs:
    nepa_or_ceqa: bool
    usace_404_401: bool
    groundwater_discharge: bool
    railroad_coord: bool
    utility_relocations: bool
    fire_authority: bool

@dataclass(frozen=True)
class PermitsResult:
    ready: bool
    missing: list[str]

def permits_check(inp: PermitsInputs) -> PermitsResult:
    checks = {
        "nepa_or_ceqa": inp.nepa_or_ceqa,
        "usace_404_401": inp.usace_404_401,
        "groundwater_discharge": inp.groundwater_discharge,
        "railroad_coord": inp.railroad_coord,
        "utility_relocations": inp.utility_relocations,
        "fire_authority": inp.fire_authority,
    }
    missing = [k for k, ok in checks.items() if not ok]
    return PermitsResult(ready=len(missing) == 0, missing=missing)
