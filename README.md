# Base de données des Calibres (Tireur.org)

Cette base de données répertorie de manière exhaustive les dimensions physiques, spécifications C.I.P. et historiques des calibres majeurs d'armes d'épaule et d'armes de poing. Elle est utilisée pour alimenter la [Base de données des calibres](https://www.tireur.org/calibres.php) ainsi que l'estimateur de balistique intérieure du site.

## Structure du Dépôt

Le dépôt contient la base de données déclinée en trois formats de distribution ainsi que son script de compilation :

*   **`calibers.json`** : Version brute idéale pour les applications Web interactives côté client (ex: autocomplétion, filtrage dynamique en JS).
*   **`calibers.db`** : Base de données SQLite 3 optimisée pour les requêtes relationnelles rapides côté serveur en PHP ou Python.
*   **`calibers.csv`** : Fichier tabulaire universel facilitant l'importation sous Excel, LibreOffice Calc ou R.
*   **`generate_calibers_db.py`** : Script Python de compilation qui fusionne les métadonnées historiques écrites à la main avec les caractéristiques géométriques C.I.P. issues de l'estimateur de balistique intérieure.

---

## Schéma des Données

Chaque calibre contient les champs suivants :

| Champ | Type | Description |
| :--- | :--- | :--- |
| `id` | Chaîne (clef) | Identifiant unique normalisé (ex: `308_win`, `9x19_parabellum`). |
| `name` | Chaîne | Nom d'affichage officiel (ex: `.308 Winchester`). |
| `aliases` | Tableau | Liste des autres appellations courantes (ex: `7.62x51 NATO`, `308 Win`). |
| `category` | Chaîne | Catégorie de munition (`Rifle`, `Handgun`, `Rimfire`). |
| `bullet_diameter_mm` | Réel | Diamètre du projectile en mm (Ø G1 dans les fiches C.I.P.). |
| `bullet_diameter_in` | Réel | Diamètre théorique en pouces. |
| `case_length_mm` | Réel | Longueur de l'étui en mm (L3 dans les fiches C.I.P.). |
| `rim_diameter_mm` | Réel | Diamètre du bourrelet/culot en mm (Ø R1). |
| `rim_type` | Chaîne | Type de culot (`Rimless`, `Rimmed`, `Semi-rimmed`, `Rebated`, `Belted`). |
| `base_diameter_mm` | Réel | Diamètre de la base du corps de l'étui en mm (Ø P1). |
| `shoulder_diameter_mm`| Réel/Null | Diamètre au bas de l'épaulement en mm (Ø P2, pour étuis bouteille). |
| `neck_diameter_mm` | Réel | Diamètre externe du collet en mm (Ø H2). |
| `max_pressure_bar` | Entier/Null | Pression admissible maximale homologuée par la C.I.P. (en bar). |
| `case_volume_cm3` | Réel | Volume interne total utile de l'étui mesuré en H₂O (en cm³). |
| `primer_type` | Chaîne | Type d'amorce usuelle (ex: `Large Rifle`, `Small Pistol`, `Rimfire`). |
| `intro_year` | Entier/Null | Année d'introduction officielle du calibre sur le marché. |
| `origin_country` | Chaîne | Pays d'origine de conception. |
| `description` | Chaîne | Résumé historique, technique et d'usage de la munition. |

---

## Compilation et Mise à Jour

Pour mettre à jour ou reconstruire la base de données, assurez-vous d'avoir Python 3 installé sur votre machine et exécutez le script :

```bash
python3 generate_calibers_db.py
```

Le script lira les données brutes présentes dans les sous-modules de l'estimateur de balistique et régénérera les fichiers `calibers.json`, `calibers.db` et `calibers.csv` directement dans ce dossier.

## Licences et Sources

*   Les données physiques sont croisées avec les tables de référence officielles de la **C.I.P.** (Commission Internationale Permanente) et de la **SAAMI**.
*   Certaines métadonnées de volume et de dimensions proviennent de la base de données open-source CC0 **zen/grt_databases** liée au projet *Gordon's Reloading Tool*.
*   Le code source de ce dépôt est distribué sous licence MIT.
