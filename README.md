# NOAA Water Temperature CA

This repository downloads recent NOAA coastal water temperature observations for a small set of California stations and stores them as CSV files.

## What this repo contains

- `main.py` — script that requests water temperature data from the NOAA Tides & Currents API and writes one CSV per station.
- `stations.csv` — list of California stations used by the script.
- `data/` — downloaded station-level water temperature files.
- `pyproject.toml` — minimal Python project configuration and dependencies.

## Data source

The data comes from the NOAA Tides & Currents API using the `water_temperature` product.

The script requests:
- station observations
- metric units
- local station time (`lst_ldt`)
- CSV output format

## Repository structure

```text
.
├── data/
│   ├── water_temperature-<StationName>-<begin_date>-<end_date>.csv
├── main.py
├── stations.csv
├── pyproject.toml
└── README.md
```

## Input file

### `stations.csv`

List of stations to query.

| column | description |
|---|---|
| `id` | NOAA station ID |
| `name` | human-readable station name |

Example:

```csv
id,name
9410170,San Diego
9410230,La Jolla
```

## Output data

The script writes one CSV file per station into `data/`.

Filename pattern:

```text
data/water_temperature-<StationName>-<begin_date>-<end_date>.csv
```

Example:

```text
data/water_temperature-San Diego-20260619-20260720.csv
```

### Output columns

| column | description |
|---|---|
| `StationID` | NOAA station ID |
| `StationName` | station name from `stations.csv` |
| `Date_Time` | observation timestamp in local station time |
| `Water_Temperature` | water temperature in degrees Celsius |
| `X` | NOAA quality/control flag field from the API output |
| `N` | NOAA quality/control flag field from the API output |
| `R` | NOAA quality/control flag field from the API output |

### Minimal metadata dictionary

```python
{
    "StationID": "NOAA station identifier",
    "StationName": "Human-readable station name",
    "Date_Time": "Observation timestamp in local station time (lst_ldt)",
    "Water_Temperature": "Observed water temperature in degrees Celsius",
    "X": "NOAA flag column carried through from source data",
    "N": "NOAA flag column carried through from source data",
    "R": "NOAA flag column carried through from source data",
}
```

## How it works

1. Read the station list from `stations.csv`
2. Request water temperature data for each station
3. Normalize column names
4. Add `StationID` and `StationName`
5. Save one CSV file per station under `data/`

## Running the script

Install dependencies and run:

```bash
python main.py
```

## Notes

- The date range is currently hard-coded in `main.py`.
- Existing files are not overwritten unless you confirm it interactively.
- Some stations may return no data for the selected date range.
