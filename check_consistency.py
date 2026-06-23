#!/usr/bin/env python3
"""Vérifie que la base de calibres (calibers.json) reste en accord avec
l'estimateur de balistique intérieure, qui en est la source via
generate_calibers_db.py (champs : bore_mm/case_mm/case_vol_cm3/pmax_cip_bar).

Compare, pour chaque calibre connu de l'estimateur, les 4 cotes clés. Sort en
code 1 si un écart dépasse la tolérance (utile en cron / pré-commit).

Usage : python3 calibers/check_consistency.py
"""
import json
import os
import re
import sys

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, ".."))

est_path = os.path.join(root, "reloading/tireur_reloaded/data/calibers.json")
db_path = os.path.join(here, "calibers.json")

with open(est_path, encoding="utf-8") as f:
    est = json.load(f)["calibers"]
with open(db_path, encoding="utf-8") as f:
    db = json.load(f)


def norm(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


idx = {}
for r in db:
    for k in [r["name"]] + r.get("aliases", []):
        idx[norm(k)] = r

# (label, clé estimateur, clé base, tolérance absolue, tolérance relative)
FIELDS = [
    ("Ø balle (mm)", "bore_mm", "bullet_diameter_mm", 0.05, 0.0),
    ("longueur étui (mm)", "case_mm", "case_length_mm", 0.30, 0.0),
    ("volume étui (cm³)", "case_vol_cm3", "case_volume_cm3", 0.05, 0.02),
    ("pression CIP (bar)", "pmax_cip_bar", "max_pressure_bar", 1.0, 0.0),
]

missing = []
discrepancies = []
checked = 0

for ek, ev in est.items():
    r = idx.get(norm(ek))
    if r is None:
        missing.append(ek)
        continue
    checked += 1
    for label, ke, kd, atol, rtol in FIELDS:
        a, b = ev.get(ke), r.get(kd)
        if a is None or b is None:
            if a != b:
                discrepancies.append(f"{ek} · {label} : estimateur {a} vs base {b}")
            continue
        if abs(a - b) > atol + rtol * abs(a):
            discrepancies.append(f"{ek} · {label} : estimateur {a} vs base {b} (Δ {b - a:+.3g})")

print(f"Cohérence base ↔ estimateur : {checked}/{len(est)} calibres comparés.")
if missing:
    print(f"  /!\\ {len(missing)} calibre(s) de l'estimateur ABSENT(s) de la base : {', '.join(missing)}")
if discrepancies:
    print(f"  /!\\ {len(discrepancies)} écart(s) :")
    for d in discrepancies:
        print(f"     - {d}")

if missing or discrepancies:
    sys.exit(1)
print("  OK — aucune divergence.")
sys.exit(0)
