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
| `case_volume_cm3` | Float/Null | Usable case volume under the seated bullet (cm³), as used by the interior-ballistics estimator — **not** the water capacity to the case mouth, which is larger (6 mm BR: 2.172 cm³ here, 38–39.5 gr = 2.46–2.56 cm³ of water for fire-formed Lapua brass). Hand-entered values are flagged by `case_volume_unsourced` (see below). |
| `case_volume_unsourced` | Bool | `true` for a hand-entered volume without a recorded source (order of magnitude only). |
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
*   Case volumes of the cartridges covered by the interior-ballistics estimator come from its own data (`reloading/tireur_reloaded/data/calibers.json`): the median of the Reload Swiss fill ratios, or for cartridges Reload Swiss does not list, the densest published loads. They are usable volumes under the bullet.
*   Outside the estimator, a volume is published as sourced only from a published water capacity read and recorded in `case_volume_reference.json`, converted with the estimator's usable fraction (0.87 for a rifle case): the .50 BMG since 2026-10-12 (290 gr of water, *Handloader*; the 18.97 cm³ entered before was Wikipedia's unreferenced 292.8 gr). The volumes of the other 27 cartridges were entered by hand **without a recorded source**: they do *not* come from the CC0 **zen/grt_databases** dataset, which covers only one of them (5.45×39, 28.30 gr H₂O there vs 1.75 cm³ = 27.0 gr here; checked on 2026-10-04). Thirteen of them equal the water capacity in the Wikipedia infobox, which cites no source; others match nothing found (checked on 2026-10-12). They are therefore of a different kind (water capacities, or unknown) and remain flagged.
*   Primer types, introduction years, design countries and descriptions are published only from sourced records (`primer_reference.json`, `intro_year_reference.json`, `country_reference.json`, `description_reference.json`); the C.I.P. registering country comes from the C.I.P. sheets (`cip_origin_reference.json`). `scripts/check_calibers.py` enforces this before every database write.
*   The source code in this repository is distributed under the MIT license.
