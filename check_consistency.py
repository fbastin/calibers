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

# Doublons DANS l'estimateur : deux entrées désignant la même cartouche (nom ou alias
# se normalisant pareil). Cause des bugs 6 Norma BR (2026-06-25) et 6 XC / 7x64 / 8x57
# (2026-07-11) : les ancres partent sur une clé, l'UI en propose une autre, quasi vide.
est_seen = {}
duplicates = []
for ek, ev in est.items():
    for key in [ek] + ev.get("aliases", []):
        n = norm(key)
        prev = est_seen.get(n)
        if prev is not None and prev != ek:
            duplicates.append(f"{prev!r} et {ek!r} désignent la même cartouche (via {key!r})")
        est_seen[n] = ek

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
if duplicates:
    print(f"  /!\\ {len(duplicates)} doublon(s) de cartouche dans l'estimateur :")
    for d in duplicates:
        print(f"     - {d}")
if missing:
    print(f"  /!\\ {len(missing)} calibre(s) de l'estimateur ABSENT(s) de la base : {', '.join(missing)}")
if discrepancies:
    print(f"  /!\\ {len(discrepancies)} écart(s) :")
    for d in discrepancies:
        print(f"     - {d}")

if missing or discrepancies or duplicates:
    sys.exit(1)
print("  OK — aucune divergence.")
sys.exit(0)
