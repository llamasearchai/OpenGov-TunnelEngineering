from __future__ import annotations

from pathlib import Path
import pandas as pd

def write_templates(folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(columns=["rqd","spacing_rating","condition_rating","groundwater_rating","orientation_rating","strength_rating"]).to_csv(folder / "rmr_template.csv", index=False)
    pd.DataFrame(columns=["k_m_per_s","head_above_axis_m","radius_m","influence_radius_m","drainage_factor"]).to_csv(folder / "inflow_template.csv", index=False)
    pd.DataFrame(columns=["volume_loss_frac","radius_m","cover_to_axis_m","K"]).to_csv(folder / "settlement_template.csv", index=False)
    pd.DataFrame(columns=["length_m","diameter_m","complexity","shaft_count","shaft_cost_usd"]).to_csv(folder / "cost_template.csv", index=False)
