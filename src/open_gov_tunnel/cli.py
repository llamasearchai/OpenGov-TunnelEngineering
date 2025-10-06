from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme

from .states import list_states
from .classification import RMRInputs, rmr_score, QInputs, q_system
from .support import natm_support_from_rmr
from .lining import LiningInputs, lining_thickness
from .groundwater import InflowInputs, inflow_per_length
from .settlement import SettlementInputs, settlement_trough, settlement_at_x
from .ventilation import VentInputs, construction_vent_airflow
from .fire_safety import EgressInputs, egress_screen
from .tbm import TBMInputs, tbm_select
from .cost import CostInputs, tunnel_cost
from .permits import PermitsInputs, permits_check
from .reports import write_templates

app = typer.Typer(help="OpenGov-TunnelEngineering: Tunnel planning/engineering screening (CA/IN/OH).")
console = Console(theme=Theme({"info": "cyan", "error": "red", "success": "green"}))


@app.command("list-states")
def cmd_list_states() -> None:
    lines = [f"{p.code}: {p.name} — Agencies: {', '.join(p.agencies)}. {p.notes}" for p in list_states()]
    console.print(Panel("\n".join(lines), title="Supported States"))


@app.command("rmr")
def cmd_rmr(
    rqd: float = typer.Option(..., "--rqd"),
    spacing: float = typer.Option(..., "--spacing"),
    condition: float = typer.Option(..., "--cond"),
    gw: float = typer.Option(..., "--gw"),
    orient: float = typer.Option(..., "--orient"),
    strength: float = typer.Option(..., "--strength"),
) -> None:
    res = rmr_score(RMRInputs(rqd=rqd, spacing_rating=spacing, condition_rating=condition, groundwater_rating=gw, orientation_rating=orient, strength_rating=strength))
    console.print(Panel(f"RMR = {res.rmr:.1f} ({res.class_label})", title="RMR"))


@app.command("qsystem")
def cmd_qsystem(
    rqd: float = typer.Option(..., "--rqd"),
    Jn: float = typer.Option(..., "--Jn"),
    Jr: float = typer.Option(..., "--Jr"),
    Ja: float = typer.Option(..., "--Ja"),
    Jw: float = typer.Option(..., "--Jw"),
    SRF: float = typer.Option(..., "--SRF"),
) -> None:
    res = q_system(QInputs(rqd=rqd, Jn=Jn, Jr=Jr, Ja=Ja, Jw=Jw, SRF=SRF))
    console.print(Panel(f"Q = {res.Q:.2f} ({res.category})", title="Q-system"))


@app.command("support")
def cmd_support(
    rmr: float = typer.Option(..., "--rmr"),
    D: float = typer.Option(..., "--D", help="Tunnel diameter (m)"),
) -> None:
    s = natm_support_from_rmr(rmr, D)
    console.print(Panel(f"Shotcrete: {s.shotcrete_mm} mm\nBolts: {s.bolt_length_m:.1f} m @ {s.bolt_spacing_m:.1f} m\nLattice girders: {s.lattice_girders}", title="NATM Support (Screening)"))


@app.command("lining")
def cmd_lining(
    p: float = typer.Option(..., "--p", help="Ground pressure (kPa)"),
    r: float = typer.Option(..., "--r", help="Radius (m)"),
    phi: float = typer.Option(..., "--phi", help="Strength factor"),
    fc: float = typer.Option(..., "--fc", help="Allowable compressive stress (kPa)"),
    tmin: float = typer.Option(0.2, "--tmin"),
) -> None:
    res = lining_thickness(LiningInputs(ground_pressure_kPa=p, radius_m=r, phi_resistance=phi, fc_allow_kPa=fc, t_min_m=tmin))
    console.print(Panel(f"Required thickness ≈ {res.t_req_m:.2f} m\nOK(min): {res.OK}", title="Lining Hoop Thickness"))


@app.command("inflow")
def cmd_inflow(
    k: float = typer.Option(..., "--k"),
    head: float = typer.Option(..., "--head"),
    r: float = typer.Option(..., "--r"),
    R: float = typer.Option(..., "--R"),
    df: float = typer.Option(1.0, "--df"),
) -> None:
    q = inflow_per_length(InflowInputs(k_m_per_s=k, head_above_axis_m=head, radius_m=r, influence_radius_m=R, drainage_factor=df))
    console.print(Panel(f"Inflow per meter ≈ {q.q_per_m3_s:.6f} m^3/s·m", title="Groundwater Inflow"))


@app.command("settlement")
def cmd_settlement(
    VL: float = typer.Option(..., "--VL"),
    r: float = typer.Option(..., "--r"),
    cover: float = typer.Option(..., "--cover"),
    K: float = typer.Option(0.5, "--K"),
    x: float = typer.Option(0.0, "--x"),
) -> None:
    tr = settlement_trough(SettlementInputs(volume_loss_frac=VL, radius_m=r, cover_to_axis_m=cover, K=K))
    s = settlement_at_x(tr, x)
    console.print(Panel(f"Smax ≈ {tr.Smax_m*1000:.1f} mm\ni ≈ {tr.i_m:.2f} m\nS(x={x} m) ≈ {s*1000:.1f} mm", title="Settlement Trough"))


@app.command("vent")
def cmd_vent(
    diesel_kW: float = typer.Option(..., "--kW"),
    persons: int = typer.Option(..., "--persons"),
) -> None:
    v = construction_vent_airflow(VentInputs(diesel_kW=diesel_kW, persons=persons))
    console.print(Panel(f"Airflow ≈ {v.airflow_m3_s:.2f} m^3/s", title="Construction Ventilation"))


@app.command("fire-egress")
def cmd_fire_egress(
    length: float = typer.Option(..., "--length"),
    spacing: float = typer.Option(152.0, "--spacing"),
    speed: float = typer.Option(1.0, "--speed"),
) -> None:
    e = egress_screen(EgressInputs(tunnel_length_m=length, max_spacing_m=spacing, walkway_speed_mps=speed))
    console.print(Panel(f"Required cross-passages: {e.required_passages}\nMax egress time ≈ {e.max_egress_time_s:.0f} s", title="Fire/Life Safety Egress"))


@app.command("tbm-select")
def cmd_tbm_select(
    ground: str = typer.Option(..., "--ground"),
    gw: str = typer.Option(..., "--gw"),
    boulders: bool = typer.Option(False, "--boulders"),
) -> None:
    t = tbm_select(TBMInputs(ground=ground, groundwater=gw, boulders=boulders))
    console.print(Panel(f"Recommended: {t.recommended}\nNotes: {t.notes}", title="TBM Selection (Screening)"))


@app.command("cost")
def cmd_cost(
    length: float = typer.Option(..., "--length"),
    D: float = typer.Option(..., "--D"),
    complexity: float = typer.Option(1.0, "--complexity"),
    shafts: int = typer.Option(2, "--shafts"),
    shaft_cost: float = typer.Option(5_000_000.0, "--shaftcost"),
) -> None:
    c = tunnel_cost(CostInputs(length_m=length, diameter_m=D, complexity=complexity, shaft_count=shafts, shaft_cost_usd=shaft_cost))
    console.print(Panel(f"Tunnel: ${c.tunnel_usd:,.0f}\nShafts: ${c.shafts_usd:,.0f}\nTotal: ${c.total_usd:,.0f}", title="Tunnel Cost"))


@app.command("permits")
def cmd_permits(
    envdoc: bool = typer.Option(True, "--envdoc"),
    usace: bool = typer.Option(True, "--usace"),
    gw_discharge: bool = typer.Option(True, "--gw"),
    rr: bool = typer.Option(False, "--rr"),
    utilities: bool = typer.Option(True, "--utilities"),
    fire: bool = typer.Option(True, "--fire"),
) -> None:
    pr = permits_check(PermitsInputs(nepa_or_ceqa=envdoc, usace_404_401=usace, groundwater_discharge=gw_discharge, railroad_coord=rr, utility_relocations=utilities, fire_authority=fire))
    console.print(Panel(("READY" if pr.ready else "MISSING: " + ", ".join(pr.missing)), title="Permits Checklist"))


@app.command("templates")
def cmd_templates(folder: Path = typer.Option(Path("templates"), "--folder")) -> None:
    write_templates(folder)
    console.print(Panel(f"Wrote templates to {folder}", title="Templates"))


def main() -> None:  # pragma: no cover
    """Main entry point for the CLI application."""
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
