# OpenGov-TunnelEngineering

A professional, terminal-first screening toolkit for tunnel planning and engineering, with immediately usable calculators for California (CA), Indiana (IN), and Ohio (OH) infrastructure projects.

## Overview

OpenGov-TunnelEngineering provides rapid, standards-based screening calculations for tunnel projects in compliance with FHWA, Caltrans, INDOT, and ODOT guidelines. This toolkit enables early-phase decision support, preliminary design validation, and QC checks across the tunnel project lifecycle.

## Features

- **Rock Mass Classification**: RMR (Rock Mass Rating) and Q-system calculations with automatic class determination
- **NATM Support Design**: Screening-level support recommendations based on rock mass quality
- **Lining Analysis**: Hoop stress and thickness calculations for preliminary lining design
- **Groundwater Analysis**: Radial inflow calculations per unit length using cylindrical flow theory
- **Settlement Prediction**: Gaussian settlement trough analysis from volume loss estimates
- **Construction Ventilation**: Airflow requirements for diesel equipment and personnel
- **Fire and Life Safety**: Egress spacing screening per NFPA 130/502 guidelines
- **TBM Selection**: Tunnel boring machine type recommendations based on ground conditions
- **Cost Estimation**: Preliminary tunnel and shaft cost modeling
- **Permitting Checklist**: Regulatory compliance tracking for environmental and construction permits
- **State-Specific Profiles**: Tailored guidance for CA, IN, and OH regulatory frameworks
- **CSV Templates**: Batch processing templates for multiple scenarios

## Key Screening Equations

### Hoop Stress (Thin Cylinder)
\\[ t_{\\text{req}} = \\frac{p \\, r}{\\phi \\, f_{\\text{allow}}} \\]

### Radial Inflow per Unit Length
\\[ Q' = \\frac{2\\pi \\, k \\, (H - z)}{\\ln(R/r_0)} \\]

### Gaussian Settlement Trough (Greenfield)
\\[ S(x) = S_{\\text{max}} \\, \\exp\\!\\left(-\\frac{x^2}{2i^2}\\right), \\quad S_{\\text{max}} = \\frac{VL \\, A}{\\sqrt{2\\pi} \\, i}, \\ i = K \\, z_0 \\]

### Q-system
\\[ Q = \\frac{\\text{RQD}}{J_n} \\cdot \\frac{J_r}{J_a} \\cdot \\frac{J_w}{\\text{SRF}} \\]

## Safety and Compliance

**IMPORTANT**: All outputs are screening-level estimates only. Final designs must follow:
- Agency standards: FHWA, Caltrans, INDOT, ODOT as applicable
- Fire/life safety codes: NFPA 130, NFPA 502
- Project-specific geotechnical investigations
- Detailed structural analysis and design
- Environmental permit requirements
- Local authority having jurisdiction (AHJ) requirements

## Installation and Testing

### Prerequisites
- Python 3.11 or higher
- uv package manager (recommended) or pip

### Installation with uv

Install uv: https://docs.astral.sh/uv/

```bash
# Create virtual environment
uv venv -p 3.11

# Install dependencies and project
uv sync

# Verify installation
uv run opengov-tunnel --help
```

### Run Tests

```bash
# Quick test run
uv run pytest -q

# Verbose test output
uv run pytest -v

# With coverage report
uv run pytest --cov=open_gov_tunnel --cov-report=term-missing
```

## CLI Command Reference

### State Profiles

List supported states with agency information and regional considerations:

```bash
uv run opengov-tunnel list-states
```

### Rock Mass Classification

**RMR (Rock Mass Rating)**:
```bash
uv run opengov-tunnel rmr --rqd 60 --spacing 10 --cond 10 --gw 8 --orient 4 --strength 10
```

**Q-system**:
```bash
uv run opengov-tunnel qsystem --rqd 60 --Jn 9 --Jr 2 --Ja 1 --Jw 1 --SRF 2
```

### NATM Support Design

```bash
uv run opengov-tunnel support --rmr 65 --D 6
```

### Lining Thickness

```bash
uv run opengov-tunnel lining --p 300 --r 3 --phi 0.7 --fc 15000 --tmin 0.25
```

Parameters:
- `--p`: Ground pressure (kPa)
- `--r`: Tunnel radius (m)
- `--phi`: Resistance/strength reduction factor
- `--fc`: Allowable compressive stress (kPa)
- `--tmin`: Minimum thickness (m)

### Groundwater Inflow

```bash
uv run opengov-tunnel inflow --k 1e-6 --head 10 --r 3 --R 100 --df 0.8
```

Parameters:
- `--k`: Hydraulic conductivity (m/s)
- `--head`: Head above tunnel axis (m)
- `--r`: Tunnel radius (m)
- `--R`: Influence radius (m)
- `--df`: Drainage factor (0-1)

### Settlement Analysis

```bash
uv run opengov-tunnel settlement --VL 0.015 --r 3 --cover 15 --K 0.5 --x 10
```

Parameters:
- `--VL`: Volume loss fraction (e.g., 0.015 = 1.5%)
- `--r`: Tunnel radius (m)
- `--cover`: Cover depth to axis (m)
- `--K`: Trough width parameter
- `--x`: Lateral distance from centerline (m)

### Construction Ventilation

```bash
uv run opengov-tunnel vent --kW 500 --persons 20
```

### Fire and Life Safety

```bash
uv run opengov-tunnel fire-egress --length 1000 --spacing 152 --speed 1.0
```

Parameters:
- `--length`: Tunnel length (m)
- `--spacing`: Maximum cross-passage spacing (m, default 152m/500ft)
- `--speed`: Walking speed (m/s)

### TBM Selection

```bash
uv run opengov-tunnel tbm-select --ground soft --gw high --boulders false
```

Ground types: `rock`, `mixed`, `soft`
Groundwater conditions: `dry`, `wet`, `high`

### Cost Estimation

```bash
uv run opengov-tunnel cost --length 1000 --D 6 --complexity 1.2 --shafts 2 --shaftcost 4000000
```

Parameters:
- `--length`: Tunnel length (m)
- `--D`: Tunnel diameter (m)
- `--complexity`: Complexity multiplier (default 1.0)
- `--shafts`: Number of shafts (default 2)
- `--shaftcost`: Cost per shaft (USD, default $5M)

### Permits Checklist

```bash
uv run opengov-tunnel permits --envdoc true --usace true --gw true --rr false --utilities true --fire true
```

### Generate CSV Templates

```bash
uv run opengov-tunnel templates --folder templates
```

Generates batch processing templates:
- `rmr_template.csv`: Rock mass rating inputs
- `inflow_template.csv`: Groundwater inflow scenarios
- `settlement_template.csv`: Settlement analysis cases
- `cost_template.csv`: Cost estimation parameters

## State-Specific Guidance

### California (CA)
- **Environmental**: CEQA documentation, NEPA compliance for federal projects
- **Water Quality**: RWQCB permits, USACE Section 404/401 permits
- **Seismic**: Active fault considerations, seismic design requirements
- **Agencies**: Caltrans, CPUC (rail), local AHJs
- **Key Standards**: Caltrans Tunnel Manual, FHWA guidelines

### Indiana (IN)
- **Geotechnical**: Glacial till management, soft ground considerations
- **Groundwater**: Dewatering permits, discharge requirements
- **Winter Operations**: Cold weather concreting, freeze-thaw considerations
- **Agencies**: INDOT, IDEM, USACE
- **Key Standards**: INDOT Design Manual, FHWA guidelines

### Ohio (OH)
- **Geotechnical**: Karst terrain evaluation, Great Lakes influence
- **Groundwater**: Regional aquifer protection, discharge permits
- **Environmental**: OEPA coordination, USACE permits
- **Agencies**: ODOT, OEPA, local AHJs
- **Key Standards**: ODOT LRFD Design Manual, FHWA guidelines

## Development Workflow

### With uv (Recommended)

```bash
# Setup
uv venv -p 3.11
uv sync

# Development
uv run pytest -q                    # Run tests
uv run pytest --cov=open_gov_tunnel # Coverage report
uv run ruff check .                 # Lint code
uv run ruff format .                # Format code
uv run mypy src                     # Type checking
```

### With hatch

```bash
hatch run test       # Run tests
hatch run cov        # Coverage report
hatch run lint       # Lint code
hatch run format     # Format code
hatch run typecheck  # Type checking
```

### With tox

```bash
tox  # Run tests in isolated environment
```

## Project Structure

```
OpenGov-TunnelEngineering/
├── pyproject.toml          # Project configuration
├── tox.ini                 # Tox configuration
├── README.md               # This file
├── .gitignore             # Git ignore patterns
├── .ruff.toml             # Ruff configuration
├── src/
│   └── open_gov_tunnel/
│       ├── __init__.py           # Package initialization
│       ├── cli.py                # CLI interface (Typer)
│       ├── utils.py              # Common utilities
│       ├── states.py             # State profiles
│       ├── classification.py     # RMR and Q-system
│       ├── support.py            # NATM support
│       ├── lining.py             # Lining calculations
│       ├── groundwater.py        # Inflow calculations
│       ├── settlement.py         # Settlement analysis
│       ├── ventilation.py        # Ventilation calculations
│       ├── fire_safety.py        # Fire/life safety
│       ├── tbm.py                # TBM selection
│       ├── cost.py               # Cost estimation
│       ├── permits.py            # Permits checklist
│       └── reports.py            # Report generation
└── tests/
    ├── test_cli_states.py        # CLI and states tests
    ├── test_class_support.py     # Classification tests
    ├── test_lining.py            # Lining tests
    ├── test_groundwater.py       # Groundwater tests
    ├── test_settlement.py        # Settlement tests
    ├── test_vent_fire.py         # Ventilation/fire tests
    └── test_tbm_cost_permits.py  # TBM/cost/permits tests
```

## Technical Requirements

- Python >= 3.11
- numpy >= 1.26.4
- pandas >= 2.2.2
- typer >= 0.12.3
- rich >= 13.7.1

## Contributing

This is a professional engineering toolkit. Contributions should:
- Follow existing code style and type annotations
- Include comprehensive tests
- Update documentation
- Maintain professional presentation (no emojis or placeholders)
- Adhere to engineering standards and best practices

## Author

Nik Jois <nikjois@llamasearch.ai>

## License

MIT License

Copyright (c) 2024 Nik Jois

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Disclaimer

This toolkit provides screening-level estimates for preliminary planning and design validation. It does not replace detailed geotechnical investigations, structural analysis, environmental assessments, or professional engineering judgment. Users are responsible for verifying all outputs and ensuring compliance with applicable codes, standards, and regulations.

---

**Version**: 0.1.0  
**Last Updated**: October 2025  

This codebase delivers practical tunnel screening utilities to support federal and state infrastructure programs in CA/IN/OH from early planning through QC checks and cost/permit readiness.