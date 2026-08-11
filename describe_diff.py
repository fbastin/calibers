#!/usr/bin/env python3
"""Décrit, champ par champ, ce que la régénération a changé dans calibers.json.

L'alerte de daily_maintenance.sh ne montrait qu'un nom de fichier (« M calibers.json »)
et concluait « le dépôt est en retard sur ses sources, à committer ». Le 2026-08-11, la
conclusion était fausse et le conseil dangereux : le fichier committé portait un relevé
C.I.P. fait à la main, la régénération l'écrasait, et le committer aurait figé douze
culots faux dans l'historique. Un diff ne dit PAS qui a raison — il dit qu'il faut
regarder. Ce script montre quoi regarder.

Usage : python3 calibers/describe_diff.py [--max N]
Sort en 0 si aucun écart, 1 s'il y en a (le contenu part alors par courriel).
"""
import argparse
import json
import os
import subprocess
import sys

here = os.path.dirname(os.path.abspath(__file__))

# Champs dont un changement silencieux se voit sur le site public.
SUIVIS = [
    "case_length_mm", "bullet_diameter_mm", "rim_diameter_mm", "base_diameter_mm",
    "shoulder_diameter_mm", "neck_diameter_mm", "rim_type", "case_volume_cm3",
    "max_pressure_bar", "pmax_cip_bar", "pmax_saami_bar", "name", "wiki_url",
]


def charge_committe():
    r = subprocess.run(["git", "-C", here, "show", "HEAD:calibers.json"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None
    return json.loads(r.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=40,
                    help="nombre maximal de fiches détaillées (défaut 40)")
    args = ap.parse_args()

    ancien = charge_committe()
    if ancien is None:
        print("Impossible de lire la version committée (dépôt absent ?) — diff non décrit.")
        return 0
    with open(os.path.join(here, "calibers.json"), encoding="utf-8") as f:
        nouveau = json.load(f)

    a = {r["id"]: r for r in ancien}
    b = {r["id"]: r for r in nouveau}

    ajouts = sorted(set(b) - set(a))
    retraits = sorted(set(a) - set(b))
    modifs = []
    for cid in sorted(set(a) & set(b)):
        ecarts = [(f, a[cid].get(f), b[cid].get(f))
                  for f in SUIVIS if a[cid].get(f) != b[cid].get(f)]
        if ecarts:
            modifs.append((cid, b[cid].get("name", cid), ecarts))

    if not (ajouts or retraits or modifs):
        print("Régénération sans écart sur les champs suivis.")
        return 0

    print(f"{len(modifs)} fiche(s) modifiée(s), {len(ajouts)} ajoutée(s), "
          f"{len(retraits)} retirée(s).\n")
    if ajouts:
        print("  Ajoutées :  " + ", ".join(ajouts))
    if retraits:
        print("  RETIRÉES :  " + ", ".join(retraits) + "   <-- un retrait est rarement voulu")
    if ajouts or retraits:
        print()

    for cid, nom, ecarts in modifs[:args.max]:
        print(f"  {nom}  [{cid}]")
        for f, av, ap_ in ecarts:
            print(f"      {f:22} committé {av!r}  ->  régénéré {ap_!r}")
    if len(modifs) > args.max:
        print(f"  … et {len(modifs) - args.max} autre(s) fiche(s).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
