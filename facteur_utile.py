#!/usr/bin/env python3
"""Facteur de volume utile : volume de l'estimateur ÷ capacité en eau mesurée par un fabricant.

    python3 calibers/facteur_utile.py

La base des calibres convertit une capacité en eau publiée (jusqu'à la bouche) en volume UTILE
sous la balle, la grandeur des volumes de l'estimateur, par un facteur. L'estimateur écrivait
« carabine ~0,87 » sans source. Le tableau de Peterson (peterson_capacity_reference.json, relevé
le 2026-10-12) donne la capacité de dizaines de cartouches que l'estimateur couvre aussi : le
rapport de leurs deux volumes, sur les cartouches dont le volume de l'estimateur vient des
remplissages Reload Swiss, est le facteur retenu (case_volume_reference.json).

Un rapport supérieur à 1 est impossible (plus de volume sous la balle que dans l'étui) : il
signale un volume de l'estimateur faux, et le script le dit.
"""
import json
import os
import re
import statistics as st

ICI = os.path.dirname(os.path.abspath(__file__))
EST = os.path.join(ICI, '..', 'reloading', 'tireur_reloaded', 'data')
GR_PAR_CM3 = 15.4324


def norm(s):
    s = s.lower().replace('winchester', 'win').replace('remington', 'rem').replace('magnum', 'mag')
    s = s.replace('springfield', 'spring')
    return re.sub(r'[^a-z0-9]', '', s)


def main():
    pet = json.load(open(os.path.join(ICI, 'peterson_capacity_reference.json'), encoding='utf-8'))['calibres']
    est = json.load(open(os.path.join(EST, 'calibers.json'), encoding='utf-8'))['calibers']
    rs = {r['cartridge'] for r in json.load(open(os.path.join(EST, 'rs_dataset.local.json'), encoding='utf-8'))} \
        if os.path.exists(os.path.join(EST, 'rs_dataset.local.json')) else set()
    idx = {}
    for k, v in est.items():
        for a in [k] + v.get('aliases', []):
            idx[norm(a)] = k
    # Une entrée par cartouche : l'étui à grosse amorce si Peterson le fait, sinon la variante SRP.
    choix = {}
    for nom, v in pet.items():
        base = re.sub(r' \(SRP\)| - Long', '', nom)
        if base not in choix or nom == base:
            choix[base] = v
    lignes = []
    for nom, v in sorted(choix.items()):
        k = idx.get(norm(nom)) or idx.get(norm(nom.split(' (')[0]))
        if not k:
            continue
        cap = v['mediane_gr'] / GR_PAR_CM3
        lignes.append((nom, k, v['lots'], v['mediane_gr'], est[k]['case_vol_cm3'], est[k]['case_vol_cm3'] / cap, k in rs))
    for nom, k, n, gr, U, r, src in lignes:
        print(f"{nom:34s} {k:22s} {n:3d} lots {gr:6.1f} gr  U {U:6.3f} cm³  U/cap {r:.3f}  {'Reload Swiss' if src else 'charges publiées'}"
              + ('   <- IMPOSSIBLE (> 1)' if r > 1 else ''))
    tous = [l[5] for l in lignes]
    rsw = [l[5] for l in lignes if l[6]]
    print(f"\n{len(tous)} cartouches : médiane {st.median(tous):.3f} ({min(tous):.3f} à {max(tous):.3f})")
    if rsw:
        print(f"{len(rsw)} à volume Reload Swiss : médiane {st.median(rsw):.3f} ({min(rsw):.3f} à {max(rsw):.3f}) "
              f"-> facteur retenu {round(st.median(rsw), 2):.2f}")


if __name__ == '__main__':
    main()
