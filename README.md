# Caliber Database (Tireur.org)

This repository contains an exhaustive database detailing the physical dimensions, C.I.P. specifications, and historical metadata of major rifle, handgun, and rimfire cartridges. It powers the interactive [Calibers Database](https://www.tireur.org/calibres.php) and the interior ballistics estimator on the website.

## Repository Structure

The database is distributed in three formats alongside its compilation script:

*   **`calibers.json`**: Raw JSON database, ideal for client-side web applications (e.g. autocompletion, dynamic filtering in JS).
*   **`calibers.db`**: SQLite 3 database file, optimized for quick relational queries on the server side (PHP, Python, etc.).
*   **`calibers.csv`**: Universal tabular format, facilitating imports into Excel, LibreOffice Calc, or R.
*   **`generate_calibers_db.py`**: Python compiler script that merges hand-curated historical metadata with C.I.P. geometry data pulled from the interior ballistics simulator.

---

## Data Schema

Each caliber entry contains the following fields:

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | String (Key) | Unique normalized identifier (e.g., `308_win`, `9x19_parabellum`). |
| `name` | String | Official display name (e.g., `.308 Winchester`). |
| `aliases` | Array | List of common alternative names (e.g., `7.62x51 NATO`, `308 Win`). |
| `category` | String | Cartridge category (`Rifle`, `Handgun`, `Rimfire`). |
| `bullet_diameter_mm` | Float | Projectile diameter in mm (Ø G1 in C.I.P. specsheets). |
| `bullet_diameter_in` | Float | Theoretical bullet diameter in inches. |
| `case_length_mm` | Float | Casing length in mm (L3 in C.I.P. specsheets). |
| `rim_diameter_mm` | Float | Rim diameter in mm (Ø R1 in C.I.P. specsheets). |
| `rim_type` | String | Case rim type (`Rimless`, `Rimmed`, `Semi-rimmed`, `Rebated`, `Belted`). |
| `base_diameter_mm` | Float | Base diameter of the case body in mm (Ø P1). |
| `shoulder_diameter_mm`| Float/Null | Diameter at the bottom of the shoulder in mm (Ø P2, for bottleneck cases). |
| `neck_diameter_mm` | Float | Neck outer diameter in mm (Ø H2). |
| `max_pressure_bar` | Int/Null | Maximum C.I.P. safety pressure limit (in bar). |
| `case_volume_cm3` | Float | Total internal case volume capacity measured in H₂O (in cm³). |
| `primer_type` | String | Standard primer type (e.g., `Large Rifle`, `Small Pistol`, `Rimfire`). |
| `intro_year` | Int/Null | Official year of introduction to the market. |
| `origin_country` | String | Country of origin/design. |
| `description` | String | Historical, technical, and usage summary of the cartridge. |

---

## Compilation & Updates

To compile or rebuild the database files locally, make sure Python 3 is installed on your system and run:

```bash
python3 generate_calibers_db.py
```

The script will read the raw simulator inputs from the parent project, process the metrics, and regenerate `calibers.json`, `calibers.db`, and `calibers.csv` directly inside this directory.

## Licenses & Sources

*   Physical dimensions and safety pressures are cross-referenced with official **C.I.P.** and **SAAMI** technical sheets.
*   Internal case volumes and secondary dimensions are sourced from the CC0 **zen/grt_databases** dataset (originating from the *Gordon's Reloading Tool* community).
*   The source code in this repository is distributed under the MIT license.
