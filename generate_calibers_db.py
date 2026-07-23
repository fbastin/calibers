#!/usr/bin/env python3
import sqlite3
import json
import csv
import os

# Root directory path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Mappings of simulator names to our hand-curated IDs
sim_key_to_id = {
    "308 Win.": "308_win",
    "9 mm Luger": "9x19_parabellum",
    "7 x 64": "7x64_brenneke",
    "6.5 Creedmoor": "65_creedmoor",
    "30-06 Spring.": "30_06_springfield",
    "9.3 x 62": "93x62_mauser",
    "300 Win. Mag.": "300_win_mag",
    "7.5 x 55 Swiss": "75x55_swiss",
    "243 Win.": "243_win",
    "7 x 57": "7x57_mauser",
    "7 Rem. Mag.": "7mm_rem_mag",
    "45 ACP (Auto)": "45_acp",
    "223 Rem.": "223_rem",
    "357 Magnum": "357_magnum",
    "44 Rem. Mag.": "44_magnum",
    "300 PRC": "300_prc",
    "6.5 x 55 SE": "65x55_swedish",
    "38 Special": "38_special",
    "222 Rem.": "222_rem",
    "270 Win.": "270_win",
    "6.5 PRC": "65_prc",
    "260 Rem.": "260_rem",
    "375 H&H Mag.": "375_hh_mag",
    "8 x 57 IS": "8x57_is",
    "8 x 68 S": "8x68s",
    "338 Lapua Mag.": "338_lapua",
    "45 - 70 Govt.": "45_70_govt",
    "22 Hornet": "22_hornet",
    "300 AAC BLK": "300_blackout",
    "10 mm Auto": "10mm_auto",
    "22-250 Rem.": "22_250_rem",
    "45 Colt": "45_colt",
    "9 mm Browning court": "380_acp",
    "30-30 Win.": "30_30_win",
    "6.5 x 47 Lapua": "65x47_lapua",
    "7.62 x 39": "762x39_m43",
    "7.62 x 54 R": "762x54r",
    "7 -08 Rem.": "7mm_08_rem",
    "40 S&W": "40_sw",
    "303 British": "303_british",
    "9.3 x 74 R": "93x74r",
    "41 Rem. Mag.": "41_rem_mag",
    "357 SIG": "357_sig",
    "6.5 Grendel": "65_grendel",
    "454 Casull": "454_casull",
    "460 S&W": "460_sw_mag",
    "257 Roberts": "257_roberts",
    "6 mm Creedmoor": "6mm_creedmoor",
    "25-06 Remington": "25_06_remington",
    "280 Remington": "280_remington",
    "50 AE": "50_ae",
    "416 Rigby": "416_rigby",
    "204 Ruger": "204_ruger",
    "458 Winchester Magnum": "458_win_mag",
}

# Hand-curated descriptions and histories
hand_curated_metadata = {
    "22_lr": {
        "name": ".22 Long Rifle",
        "intro_year": 1887,
        "origin_country": "États-Unis",
        "description": "Le calibre à percussion annulaire le plus populaire au monde. Utilisé pour le tir de loisir, la compétition (pistolet et carabine à 50m) et l'initiation."
    },
    "22_wmr": {
        "name": ".22 Winchester Magnum Rimfire",
        "intro_year": 1959,
        "origin_country": "États-Unis",
        "description": "Une version allongée et plus puissante du .22 LR, offrant une trajectoire plus tendue et une plus grande portée pour la petite chasse ou le tir récréatif."
    },
    "17_hmr": {
        "name": ".17 Hornady Magnum Rimfire",
        "intro_year": 2002,
        "origin_country": "États-Unis",
        "description": "Obtenu en rétreignant un étui de .22 WMR au calibre .17. Vitesse de sortie exceptionnelle pour un calibre à percussion annulaire (plus de 770 m/s)."
    },
    "25_acp": {
        "name": ".25 ACP",
        "intro_year": 1905,
        "origin_country": "Belgique / États-Unis",
        "description": "Conçu par John Browning pour les pistolets de poche ultra-compacts (gilets de protection). Très faible recul."
    },
    "32_acp": {
        "name": ".32 ACP",
        "intro_year": 1899,
        "origin_country": "Belgique",
        "description": "Calibre mythique de John Browning ayant équipé d'innombrables pistolets policiers et militaires européens au XXe siècle (ex: Walther PP/PPK, Ruby)."
    },
    "380_acp": {
        "name": ".380 ACP",
        "intro_year": 1908,
        "origin_country": "États-Unis",
        "description": "Conçu pour les pistolets semi-automatiques compacts à culasse non calée (blowback). Populaire pour la défense personnelle."
    },
    "9x19_parabellum": {
        "name": "9×19mm Parabellum",
        "intro_year": 1902,
        "origin_country": "Allemagne",
        "description": "Le calibre d'arme de poing le plus répandu au monde. Standard de l'OTAN pour les pistolets et pistolets-mitrailleurs."
    },
    "9x21_imi": {
        "name": "9×21mm IMI",
        "intro_year": 1984,
        "origin_country": "Israël",
        "description": "Développé par Israel Military Industries (IMI) pour contourner les législations interdisant le 9x19mm militaire dans certains pays européens (ex. Italie)."
    },
    "9x18_makarov": {
        "name": "9×18mm Makarov",
        "intro_year": 1951,
        "origin_country": "Union Soviétique",
        "description": "Calibre militaire soviétique standard pour le pistolet Makarov. Le projectile est légèrement plus large que le 9mm occidental."
    },
    "762x25_tokarev": {
        "name": "7.62×25mm Tokarev",
        "intro_year": 1930,
        "origin_country": "Union Soviétique",
        "description": "Calibre à douille bouteille ultra-rapide utilisé dans les pistolets TT-33 et pistolets-mitrailleurs (PPSh-41). Forte capacité de perforation."
    },
    "763_mauser": {
        "name": "7.63×25mm Mauser",
        "intro_year": 1896,
        "origin_country": "Allemagne",
        "description": "Munition d'origine du pistolet Mauser C96. Très proche du Tokarev mais avec une pression de fonctionnement légèrement inférieure."
    },
    "357_sig": {
        "name": ".357 SIG",
        "intro_year": 1994,
        "origin_country": "Suisse / États-Unis",
        "description": "Créé en rétreignant un étui de .40 S&W pour y loger une balle de 9mm. Conçu pour reproduire la balistique du .357 Mag dans un pistolet semi-automatique."
    },
    "38_special": {
        "name": ".38 Smith & Wesson Special",
        "intro_year": 1898,
        "origin_country": "États-Unis",
        "description": "Le calibre de revolver le plus populaire au monde, réputé pour sa précision exceptionnelle et son recul modéré."
    },
    "357_magnum": {
        "name": ".357 Magnum",
        "intro_year": 1934,
        "origin_country": "États-Unis",
        "description": "Créé en allongeant la douille du .38 Special pour supporter de très fortes pressions. Un grand classique pour revolvers de défense et de sport."
    },
    "40_sw": {
        "name": ".40 Smith & Wesson",
        "intro_year": 1990,
        "origin_country": "États-Unis",
        "description": "Compromis entre le 9mm Parabellum et le .45 ACP, conçu à la demande du FBI après la fusillade de Miami."
    },
    "10mm_auto": {
        "name": "10mm Auto",
        "intro_year": 1983,
        "origin_country": "États-Unis",
        "description": "Calibre d'arme de poing très puissant à trajectoire tendue, initialement adopté par le FBI avant d'être jugé trop puissant pour un usage généralisé."
    },
    "41_rem_mag": {
        "name": ".41 Remington Magnum",
        "intro_year": 1964,
        "origin_country": "États-Unis",
        "description": "Calibre intermédiaire de revolver destiné à combler le fossé entre le .357 Magnum et le .44 Magnum pour le maintien de l'ordre."
    },
    "44_special": {
        "name": ".44 Smith & Wesson Special",
        "intro_year": 1907,
        "origin_country": "États-Unis",
        "description": "Grand frère historique du .44 Magnum. Réputé pour sa douceur et sa précision dans les revolvers compacts."
    },
    "44_magnum": {
        "name": ".44 Remington Magnum",
        "intro_year": 1955,
        "origin_country": "États-Unis",
        "description": "Popularisé par le film 'L'Inspecteur Harry'. Calibre mythique pour la chasse de gros gigier à l'arme de poing et la silhouette métallique."
    },
    "45_acp": {
        "name": ".45 ACP",
        "intro_year": 1904,
        "origin_country": "États-Unis",
        "description": "Développé par John Browning pour le célèbre pistolet Colt M1911. Calibre lourd et lent doté d'un excellent pouvoir d'arrêt."
    },
    "45_colt": {
        "name": ".45 Colt",
        "intro_year": 1872,
        "origin_country": "États-Unis",
        "description": "Calibre historique du revolver Colt Single Action Army (Peacemaker) à l'époque de la conquête de l'Ouest. Très populaire en Cowboy Action Shooting."
    },
    "454_casull": {
        "name": ".454 Casull",
        "intro_year": 1957,
        "origin_country": "États-Unis",
        "description": "Développé par Dick Casull. Version sur-vitaminée du .45 Colt conçue pour résister à d'immenses pressions, destinée à la chasse aux grands fauves."
    },
    "460_sw_mag": {
        "name": ".460 S&W Magnum",
        "intro_year": 2005,
        "origin_country": "États-Unis",
        "description": "Le calibre de revolver à percussion centrale de série le plus rapide du monde. Développé pour la chasse à longue distance."
    },
    "500_sw_mag": {
        "name": ".500 S&W Magnum",
        "intro_year": 2003,
        "origin_country": "États-Unis",
        "description": "Conçu par Smith & Wesson pour son revolver géant à carcasse X. L'une des munitions d'arme de poing de série les plus énergétiques."
    },
    "50_ae": {
        "name": ".50 Action Express",
        "intro_year": 1988,
        "origin_country": "États-Unis",
        "description": "Munition reine du pistolet semi-automatique Desert Eagle. Diamètre de culot réduit (identique au .44 Mag) pour faciliter la conversion d'armes."
    },
    "57x28_fn": {
        "name": "5.7×28mm",
        "intro_year": 1990,
        "origin_country": "Belgique",
        "description": "Conçu par la FN Herstal pour remplacer le 9mm dans les rôles de défense individuelle (P90 et Five-seveN). Projectile léger ultra-rapide."
    },
    "46x30_hk": {
        "name": "4.6×30mm HK",
        "intro_year": 1999,
        "origin_country": "Allemagne",
        "description": "Cartouche de très petit calibre à haute vitesse conçue par Heckler & Koch pour l'arme de défense individuelle MP7. Projectile léger optimisé pour la perforation des gilets pare-balles souples, avec recul et masse réduits. Concurrente directe du 5.7×28 mm FN."
    },
    "556x45_nato": {
        "name": "5.56×45mm NATO",
        "intro_year": 1980,
        "origin_country": "Belgique",
        "description": "Standard OTAN (STANAG 4172) dérivé du .223 Remington, adopté avec le projectile SS109/M855 à noyau d'acier. Cotes extérieures identiques au .223, mais chambre à cône de forcement (leade) plus long et chargement à plus haute pression. Munition de service des fusils d'assaut de l'OTAN (M16, HK416, etc.)."
    },
    "762x51_nato": {
        "name": "7.62×51mm NATO",
        "intro_year": 1954,
        "origin_country": "États-Unis",
        "description": "Standard OTAN (STANAG 2310) dérivé du .308 Winchester, adopté en 1954 pour le fusil M14 et la mitrailleuse M60. Cotes proches du .308 mais spécifications militaires (mesure de pression EPVAT, parois d'étui plus épaisses). Munition de service de nombreux fusils d'appui et de précision de l'OTAN."
    },
    "765_luger": {
        "name": "7.65×21mm Parabellum",
        "intro_year": 1898,
        "origin_country": "Allemagne",
        "description": "Prédécesseur du 9x19mm Parabellum. Utilisé notamment dans le pistolet Luger original et adopté par l'armée suisse."
    },
    "32_sw_long": {
        "name": ".32 S&W Long",
        "intro_year": 1896,
        "origin_country": "États-Unis",
        "description": "Calibre réputé pour sa précision extrême à courte distance. Très prisé dans les épreuves de tir de précision ISSF à 25 mètres (Pistolet Sport)."
    },
    "44_40_win": {
        "name": ".44-40 Winchester",
        "intro_year": 1873,
        "origin_country": "États-Unis",
        "description": "Premier calibre polyvalent moderne permettant d'utiliser les mêmes cartouches dans sa carabine Winchester 1873 et son revolver Colt Frontier."
    },
    "75_swiss_rev": {
        "name": "7.5mm 1882 Swiss",
        "intro_year": 1882,
        "origin_country": "Suisse",
        "description": "Munition de service du revolver d'ordonnance suisse Modèle 1882. Chargée à l'origine à la poudre noire puis à la poudre sans fumée."
    },
    "8mm_lebel_rev": {
        "name": "8mm Lebel Revolver",
        "intro_year": 1892,
        "origin_country": "France",
        "description": "Conçue pour le Revolver Modèle 1892 français d'ordonnance. Munition de service de l'armée française durant la Grande Guerre."
    },
    "204_ruger": {
        "name": ".204 Ruger",
        "intro_year": 2004,
        "origin_country": "États-Unis",
        "description": "Développé en partenariat avec Hornady et Ruger. Un calibre 'varmint' (petite nuisible) tirant à très haute vélocité (1280 m/s) à trajectoire ultra-tendue."
    },
    "222_rem": {
        "name": ".222 Remington",
        "intro_year": 1950,
        "origin_country": "États-Unis",
        "description": "Calibre mythique de Benchrest et de chasse légendaire pour sa précision. Très populaire en France en raison des anciennes législations sur les calibres militaires."
    },
    "223_rem": {
        "name": ".223 Remington",
        "intro_year": 1957,
        "origin_country": "États-Unis",
        "description": "Dérivé du .222 Rem, il a servi de base au standard militaire de l'OTAN (5.56x45mm). Universellement répandu dans les fusils de type AR-15."
    },
    "22_250_rem": {
        "name": ".22-250 Remington",
        "intro_year": 1937,
        "origin_country": "États-Unis",
        "description": "Calibre de chasse varmint ultra-rapide capable de dépasser les 1200 m/s avec un projectile léger. Très apprécié pour le tir de régulation."
    },
    "243_win": {
        "name": ".243 Winchester",
        "intro_year": 1955,
        "origin_country": "États-Unis",
        "description": "Créé en rétreignant le collet de la douille du .308 Win. Très polyvalent pour le chevreuil, le renard et le tir de précision."
    },
    "6mm_creedmoor": {
        "name": "6mm Creedmoor",
        "intro_year": 2007,
        "origin_country": "États-Unis",
        "description": "Version de compétition issue du 6.5 Creedmoor, optimisée pour le tir à très longue distance avec un recul encore plus modéré."
    },
    "65x55_swedish": {
        "name": "6.5×55mm Swedish",
        "intro_year": 1894,
        "origin_country": "Suède / Norvège",
        "description": "Calibre militaire historique scandinave (Mauser suédois), légendaire pour sa précision, son recul doux et la grande densité de section de ses projectiles."
    },
    "65_creedmoor": {
        "name": "6.5 Creedmoor",
        "intro_year": 2007,
        "origin_country": "États-Unis",
        "description": "Calibre moderne développé par Hornady. Standard de fait pour le tir à longue distance (TLD) à faible recul, optimisé pour les culasses courtes d'action standard."
    },
    "65_grendel": {
        "name": "6.5 Grendel",
        "intro_year": 2003,
        "origin_country": "États-Unis",
        "description": "Développé pour maximiser les performances à moyenne et longue distance de la plateforme AR-15 en remplaçant la munition 5.56 NATO."
    },
    "260_rem": {
        "name": ".260 Remington",
        "intro_year": 1997,
        "origin_country": "États-Unis",
        "description": "Un étui de .308 Winchester rétreint en 6.5mm. Offre des performances très similaires au 6.5 Creedmoor."
    },
    "270_win": {
        "name": ".270 Winchester",
        "intro_year": 1925,
        "origin_country": "États-Unis",
        "description": "Obtenu en rétreignant le collet du .30-06. Une munition légendaire de grande chasse à tir très tendu (grand gibier, plaine et montagne)."
    },
    "7mm_08_rem": {
        "name": "7mm-08 Remington",
        "intro_year": 1980,
        "origin_country": "États-Unis",
        "description": "Douille de .308 rétreinte en 7mm. Offre un excellent équilibre entre le recul modéré et une excellente efficacité à la chasse et en TLD."
    },
    "7mm_rem_mag": {
        "name": "7mm Remington Magnum",
        "intro_year": 1962,
        "origin_country": "États-Unis",
        "description": "Une des munitions magnum de grande chasse les plus populaires au monde, réputée pour sa vitesse et son énergie résiduelle à longue distance."
    },
    "75x55_swiss": {
        "name": "7.5×55mm Swiss",
        "intro_year": 1911,
        "origin_country": "Suisse",
        "description": "Munition militaire d'ordonnance suisse (GP11) utilisée dans le K31. Exceptionnelle régularité de fabrication d'origine."
    },
    "308_win": {
        "name": ".308 Winchester",
        "intro_year": 1952,
        "origin_country": "États-Unis",
        "description": "Standard militaire de fait (7.62x51). Calibre universel de précision pour fusils à verrou ou semi-automatiques, réputé stable et tolérant."
    },
    "30_06_springfield": {
        "name": ".30-06 Springfield",
        "intro_year": 1906,
        "origin_country": "États-Unis",
        "description": "Calibre militaire des deux guerres mondiales (M1 Garand, Springfield 1903). Devenu l'une des munitions de chasse les plus utilisées au monde."
    },
    "30_30_win": {
        "name": ".30-30 Winchester",
        "intro_year": 1895,
        "origin_country": "États-Unis",
        "description": "Calibre emblématique des carabines de cow-boy à levier de sous-garde (Winchester 94, Marlin 336). Portée pratique limitée mais recul modéré."
    },
    "300_blackout": {
        "name": ".300 AAC Blackout",
        "intro_year": 2011,
        "origin_country": "États-Unis",
        "description": "Développé pour offrir des performances similaires au 7.62x39mm dans une carcasse d'AR-15 standard, excellent comportement en chargement subsonique avec modérateur de son."
    },
    "762x39_m43": {
        "name": "7.62×39mm",
        "intro_year": 1943,
        "origin_country": "Union Soviétique",
        "description": "Calibre de l'AK-47 et de la SKS. Conçu pour le combat à moyenne portée. Munition économique et rustique."
    },
    "545x39_m74": {
        "name": "5.45×39mm",
        "intro_year": 1974,
        "origin_country": "Union Soviétique",
        "description": "Réponse soviétique au 5.56 NATO. Utilisé dans le fusil d'assaut AK-74, réputé pour sa flèche très tendue et son recul quasi-inexistant."
    },
    "762x54r": {
        "name": "7.62×54mmR",
        "intro_year": 1891,
        "origin_country": "Union Soviétique",
        "description": "Le plus ancien calibre militaire toujours en service actif dans le monde (Dragunov SVD, PKM, Mosin-Nagant). Puissant et doté d'un gros bourrelet."
    },
    "303_british": {
        "name": ".303 British",
        "intro_year": 1889,
        "origin_country": "Royaume-Uni",
        "description": "Calibre militaire du Lee-Enfield de l'Empire britannique. À l'origine conçu pour la poudre noire avec une balle à calotte de papier."
    },
    "8x57_is": {
        "name": "8×57mm IS (8mm Mauser)",
        "intro_year": 1905,
        "origin_country": "Allemagne",
        "description": "Calibre militaire légendaire du Mauser 98k. Attention : ne pas confondre avec le 8x57 I (diamètre de balle de .318\")."
    },
    "300_win_mag": {
        "name": ".300 Winchester Magnum",
        "intro_year": 1963,
        "origin_country": "États-Unis",
        "description": "Très populaire pour le tir d'élite longue distance (militaires et forces de l'ordre) ainsi que pour la chasse au très gros gibier."
    },
    "338_lapua": {
        "name": ".338 Lapua Magnum",
        "intro_year": 1989,
        "origin_country": "Finlande",
        "description": "Conçu spécifiquement pour le tir de précision militaire longue distance (jusqu'à 1500m+) afin de se situer entre le 7.62 NATO et le .50 BMG."
    },
    "375_hh_mag": {
        "name": ".375 Holland & Holland Magnum",
        "intro_year": 1912,
        "origin_country": "Royaume-Uni",
        "description": "La référence absolue pour le safari africain. Considéré comme le calibre minimum légal pour la chasse aux « Big Five » (les 5 grands fauves) dans de nombreux pays."
    },
    "45_70_govt": {
        "name": ".45-70 Government",
        "intro_year": 1873,
        "origin_country": "États-Unis",
        "description": "Munition de l'armée américaine à la fin du XIXe siècle. Très prisée dans les carabines modernes à levier de sous-garde pour la chasse en sous-bois."
    },
    "50_bmg": {
        "name": ".50 BMG",
        "intro_year": 1921,
        "origin_country": "États-Unis",
        "description": "Munition lourde de mitrailleuse lourde (M2 Browning) et de fusil de précision à très longue portée antimatériel (ex: Barrett M82)."
    },
    "22_hornet": {
        "name": ".22 Hornet",
        "intro_year": 1930,
        "origin_country": "États-Unis",
        "description": "Un des plus petits calibres de carabine de chasse à percussion centrale. Idéal pour les renards et le tir nuisible silencieux à 100-150m."
    },
    "220_swift": {
        "name": ".220 Swift",
        "intro_year": 1935,
        "origin_country": "États-Unis",
        "description": "Calibre pionnier de la très haute vélocité (dépassant 1200 m/s). Réputé exigeant pour les canons."
    },
    "65x47_lapua": {
        "name": "6.5×47mm Lapua",
        "intro_year": 2005,
        "origin_country": "Finlande",
        "description": "Développé spécifiquement par Lapua pour la compétition de tir de précision à 300m. Exceptionnellement régulier."
    },
    "7x57_mauser": {
        "name": "7×57mm Mauser",
        "intro_year": 1892,
        "origin_country": "Allemagne",
        "description": "Calibre militaire historique adopté par l'Espagne et plusieurs pays d'Amérique du Sud. Réputé pour son recul confortable et sa pénétration élevée."
    },
    "7x64_brenneke": {
        "name": "7×64mm Brenneke",
        "intro_year": 1917,
        "origin_country": "Allemagne",
        "description": "Une des munitions de chasse au grand gibier les plus populaires d'Europe centrale et de France, conçue par Wilhelm Brenneke."
    },
    "75x54_french": {
        "name": "7.5×54mm French",
        "intro_year": 1929,
        "origin_country": "France",
        "description": "Calibre de service français pour les fusils MAS 36, MAS 49/56 et fusils-mitrailleurs 24/29."
    },
    "765_argentined": {
        "name": "7.65×53mm Argentine",
        "intro_year": 1889,
        "origin_country": "Allemagne",
        "description": "Calibre militaire historique conçu par Mauser pour la Belgique et l'Argentine. Très proche balistiquement du .303 British ou du 7.62x54R."
    },
    "8x50r_lebel": {
        "name": "8×50mmR Lebel",
        "intro_year": 1886,
        "origin_country": "France",
        "description": "La toute première cartouche militaire chargée de poudre sans fumée (poudre B) de l'histoire, adoptée pour le fusil Lebel Mle 1886."
    },
    "93x62_mauser": {
        "name": "9.3×62mm Mauser",
        "intro_year": 1905,
        "origin_country": "Allemagne",
        "description": "Conçue par Otto Bock pour les colons européens en Afrique. Une munition formidable pour la chasse en battue du sanglier et des grands cervidés."
    },
    "93x74r": {
        "name": "9.3×74mmR",
        "intro_year": 1900,
        "origin_country": "Allemagne",
        "description": "Version à bourrelet pour carabines express (canons basculants) du calibre 9.3mm. Calibre roi de la battue de grand gibier en France."
    },
    "408_cheytac": {
        "name": ".408 Cheyenne Tactical",
        "intro_year": 2001,
        "origin_country": "États-Unis",
        "description": "Conçu pour combler le vide entre le .338 Lapua et le .50 BMG. Détient de nombreux records mondiaux de tir à très longue distance (ELR)."
    },
    "416_barrett": {
        "name": ".416 Barrett",
        "intro_year": 2005,
        "origin_country": "États-Unis",
        "description": "Développé en modifiant un étui de .50 BMG. Conçu pour le tir à ultra-longue distance, avec un vol supersonique au-delà de 2000 mètres."
    },
    "450_bushmaster": {
        "name": ".450 Bushmaster",
        "intro_year": 2007,
        "origin_country": "États-Unis",
        "description": "Conçu pour le concept de 'gros calibre' (Thumper) dans la plateforme AR-15, tirant des balles de .452\" à courte distance pour la chasse en battue."
    },
    "458_win_mag": {
        "name": ".458 Winchester Magnum",
        "intro_year": 1956,
        "origin_country": "États-Unis",
        "description": "Créé pour remplacer les coûteux calibres anglais de double Express en safari. Calibre lourd et puissant pour éléphants et buffles."
    },
    "65_prc": {
        "name": "6.5 PRC",
        "intro_year": 2018,
        "origin_country": "États-Unis",
        "description": "Version 'Magnum' moderne du 6.5 Creedmoor conçue par Hornady. Offre environ 80 m/s de vitesse supplémentaire pour le tir à longue distance et la chasse."
    },
    "300_prc": {
        "name": ".300 PRC",
        "intro_year": 2018,
        "origin_country": "États-Unis",
        "description": "Calibre magnum moderne sans ceinture de feu (beltless) optimisé pour loger des balles très longues à coefficient balistique très élevé pour le tir ELR."
    },
    "8x68s": {
        "name": "8×68mm S",
        "intro_year": 1939,
        "origin_country": "Allemagne",
        "description": "L'un des calibres de chasse de 8mm les plus performants, souvent appelé 'Magnum sans ceinture de feu allemand'. Conçu pour les chasses de montagne et de plaine de gros gibier."
    }
}

def clean_id(key):
    return key.lower().replace('.', '').replace('-', '').replace(' ', '_').replace('__', '_')

def clean_display_name(key):
    name = key
    replacements = {
        "Win. Mag.": "Winchester Magnum",
        "Win.": "Winchester",
        "Rem. Mag.": "Remington Magnum",
        "Rem.": "Remington",
        "Spring.": "Springfield",
        "Govt.": "Government",
        "Mag.": "Magnum",
        "Auto": "Auto",
        " court": " Court",
        " x ": " × ",
        " mm": "mm"
    }
    for k, v in replacements.items():
        name = name.replace(k, v)
        
    # Standard formats
    if "9mm Luger" in name or "9 mm Luger" in name:
        name = "9×19mm Parabellum"
    elif "45 ACP" in name:
        name = ".45 ACP"
    elif "38 Special" in name:
        name = ".38 Special"
    elif "357 Magnum" in name:
        name = ".357 Magnum"
    elif "44 Rem. Magnum" in name or "44 Rem. Mag" in name:
        name = ".44 Remington Magnum"
    elif "223 Remington" in name or "223 Rem" in name:
        name = ".223 Remington"
    elif "308 Winchester" in name or "308 Win" in name:
        name = ".308 Winchester"
    elif "30-06" in name:
        name = ".30-06 Springfield"
    elif "300 AAC BLK" in name:
        name = ".300 AAC Blackout"
    elif "7.5 × 55 Swiss" in name:
        name = "7.5×55mm Swiss (GP11)"
    elif "7.62 × 39" in name:
        name = "7.62×39mm"
    elif "7.62 × 54 R" in name:
        name = "7.62×54mmR"
    elif "303 British" in name:
        name = ".303 British"
    elif "8 × 57 IS" in name:
        name = "8×57mm IS (8mm Mauser)"
    elif "6.5 × 55 SE" in name:
        name = "6.5×55mm Swedish"
    elif "22-250" in name:
        name = ".22-250 Remington"
    elif "30-30" in name:
        name = ".30-30 Winchester"
    elif "10mm Auto" in name:
        name = "10mm Auto"
    elif "40 S&W" in name:
        name = ".40 S&W"
    elif "45 Colt" in name:
        name = ".45 Colt"
        
    # Add dot prefix if it starts with digit + unit
    first_word = name.split()[0] if name else ""
    if first_word.replace('.', '').isdigit() and (
        first_word.startswith("22") or first_word.startswith("24") or 
        first_word.startswith("25") or first_word.startswith("26") or 
        first_word.startswith("27") or first_word.startswith("28") or 
        first_word.startswith("30") or first_word.startswith("33") or 
        first_word.startswith("37") or first_word.startswith("40") or 
        first_word.startswith("41") or first_word.startswith("44") or 
        first_word.startswith("45") or first_word.startswith("50")
    ):
        if not name.startswith("."):
            name = "." + name
            
    return name

def classify_rim_type(name, category, rim, base):
    name_lower = name.lower()
    if any(x in name_lower for x in ["belted", "belt", "mag.", "magnum", "weatherby", "wby"]):
        belted_list = [
            "300 win. mag.", "7 rem. mag.", "375 h&h", "338 win.", "257 wby.", 
            "270 wby.", "300 wby.", "7mm wby.", "240 wby.", "458 win.", 
            "458 lott", "300 lapua", "300 norma", "338 norma", "belted"
        ]
        if any(x in name_lower for x in belted_list) and category == "Rifle":
            return "Belted"
            
    # Rimmed check
    rimmed_indicators = [
        " r ", " r", "govt", "government", "hornet", "winchester-rimmed", 
        "303 british", "lebel", "nagant", "tokarev-rimmed", "marlin", 
        "zipper", "maximum"
    ]
    if category == "Rimfire":
        return "Rimmed"
    if any(name_lower.endswith(x) for x in [" r", " irs"]) or any(x in name_lower for x in rimmed_indicators):
        return "Rimmed"
    if category == "Handgun" and any(x in name_lower for x in ["special", "magnum", "colt", "casull", "s&w", "linebaugh"]):
        return "Rimmed"
        
    if rim and base:
        diff = rim - base
        if diff < -0.12:
            return "Rebated"
        elif diff > 0.4:
            if category == "Handgun" and any(x in name_lower for x in ["acp", "browning"]):
                return "Semi-rimmed"
            return "Rimmed"
            
    return "Rimless"

def guess_country(name):
    name_lower = name.lower()
    if any(x in name_lower for x in ["swiss", "schmidt", "gp11", "1882"]):
        return "Suisse"
    if any(x in name_lower for x in ["winchester", "win", "remington", "rem", "springfield", "spring", "colt", "s&w", "smith", "barrett", "cheytac", "aac", "nosler", "savage", "hornady", "weatherby", "wby", "federal", "fed", "creedmoor", "grendel", "valkyrie", "bushmaster", "socom", "linebaugh", "marlin", "zipper", "cheyenne", "fireball"]):
        return "États-Unis"
    if any(x in name_lower for x in ["mauser", "brenneke", "sauer", "luger", "anschutz", "heckler", "koch", "walther", "kurz", "blaser"]):
        return "Allemagne"
    if any(x in name_lower for x in ["lapua", "sako"]):
        return "Finlande"
    if any(x in name_lower for x in ["french", "lebel", "mas"]):
        return "France"
    if any(x in name_lower for x in ["british", "h&h", "holland", "enfield", "webley"]):
        return "Royaume-Uni"
    if any(x in name_lower for x in ["soviet", "makarov", "tokarev", "kalashnikov", "russian", "nagant", "m43", "m74"]):
        return "Union Soviétique"
    if "imi" in name_lower or "israel" in name_lower:
        return "Israël"
    if "cz" in name_lower or "bren" in name_lower:
        return "République Tchèque"
    if "browning" in name_lower:
        return "Belgique"
    if "steyr" in name_lower or "mannlicher" in name_lower:
        return "Autriche"
    return "Inconnu"

def guess_primer(category, bullet_dia, case_len):
    if category == "Handgun":
        if case_len < 25:
            return "Small Pistol"
        return "Large Pistol"
    else: # Rifle
        if bullet_dia < 6.5:
            return "Small Rifle"
        return "Large Rifle"

# Lien vers une fiche wiki détaillée (par id de calibre)
WIKI_LINKS = {
    "75x55_swiss": "https://www.tireur.org/wiki/doku.php?id=technique:cartouche_7-5x55",
}

# Valeurs non vérifiées (estimées) — affichées comme telles dans la fiche.
ESTIMATED_NOTES = {
    "25_acp": "Volume d'étui estimé (non publié C.I.P./SAAMI).",
    "32_acp": "Volume d'étui estimé (non publié C.I.P./SAAMI).",
    "32_sw_long": "Volume d'étui estimé (non publié C.I.P./SAAMI).",
    "500_sw_mag": "Volume d'étui estimé (non publié C.I.P./SAAMI).",
    "8x50r_lebel": "Volume d'étui estimé (non publié C.I.P./SAAMI).",
    "416_barrett": "Pression maximale indicative (cartouche non normalisée C.I.P.).",
    "556x45_nato": "Cotes extérieures identiques au .223 Remington, mais cartouches NON strictement interchangeables : une munition 5.56 OTAN tirée dans une chambre .223 Rem peut générer une surpression dangereuse. L'inverse (.223 Rem dans une chambre 5.56/OTAN) est généralement sans risque. Spécification militaire OTAN, non normalisée C.I.P.",
    "762x51_nato": "Très proche du .308 Winchester, mais cartouches NON strictement interchangeables : le 7.62 OTAN se tire généralement sans risque dans une chambre .308 Win, alors qu'une munition .308 (pression plus élevée, parois d'étui plus fines) tirée dans une chambre militaire 7.62 (headspace plus long) peut provoquer une rupture d'étui. Spécification militaire OTAN, non normalisée C.I.P.",
    "223_rem": "Voir aussi la variante militaire distincte 5.56×45mm NATO (cotes extérieures identiques, mais chambre à leade plus long et pression supérieure). Une chambre .223 Rem n'est pas prévue pour la munition 5.56 OTAN.",
    "308_win": "Voir aussi la variante militaire distincte 7.62×51mm NATO (cotes proches, spécifications différentes). Tirer une munition .308 Win dans une chambre militaire 7.62 OTAN (headspace plus long) peut provoquer une rupture d'étui.",
}


def merge_databases():
    print("Loading simulator databases...")
    calibers_json_path = os.path.join(root_dir, "reloading/tireur_reloaded/data/calibers.json")
    dims_json_path = os.path.join(root_dir, "reloading/tireur_reloaded/data/cartridge_dims.json")
    
    with open(calibers_json_path, "r", encoding="utf-8") as f:
        sim_calibers = json.load(f)["calibers"]
        
    with open(dims_json_path, "r", encoding="utf-8") as f:
        sim_dims = json.load(f)["dims"]
        
    processed_ids = set()
    merged_list = []
    
    # 1. Process all calibers from the simulator
    for sim_name, sim_val in sim_calibers.items():
        cid = sim_key_to_id.get(sim_name, clean_id(sim_name))
        
        # Check if we have hand-curated metadata
        hand_curated = hand_curated_metadata.get(cid, {})
        
        # Category conversion
        category = "Rifle"
        if sim_val["type"] == "handgun":
            category = "Handgun"
        elif cid in ["22_lr", "22_wmr", "17_hmr"]:
            category = "Rimfire"
            
        bullet_dia = sim_val["bore_mm"]
        case_len = sim_val["case_mm"]
        pmax = sim_val.get("pmax_cip_bar")
        case_vol = sim_val.get("case_vol_cm3")
        
        # Dimensions from dims file
        dims_val = sim_dims.get(sim_name, {})
        rim = dims_val.get("rim")
        base = dims_val.get("base")
        neck = dims_val.get("neck")
        shoulder = dims_val.get("shoulder")
        
        # Fallbacks for dimensions if missing
        if not rim: rim = base if base else bullet_dia
        if not base: base = neck if neck else bullet_dia
        if not neck: neck = bullet_dia
        
        isBottleneck = (base - neck) > 0.8 and category == "Rifle"
        if not shoulder:
            if isBottleneck:
                shoulder = base - 0.2
            else:
                shoulder = None
                
        rim_type = classify_rim_type(sim_name, category, rim, base)
        
        # Aliases
        aliases = sim_val.get("aliases", [])
        if sim_name not in aliases:
            aliases.append(sim_name)
        if hand_curated.get("name") and hand_curated["name"] not in aliases:
            aliases.append(hand_curated["name"])
            
        # Merge properties
        name = hand_curated.get("name", clean_display_name(sim_name))
        intro_year = hand_curated.get("intro_year")
        country = hand_curated.get("origin_country", guess_country(sim_name))
        primer = hand_curated.get("primer_type", guess_primer(category, bullet_dia, case_len))
        
        # Specific overrides for primer types of known big rounds
        if "338" in cid or "300" in cid or "375" in cid or "416" in cid or "50" in cid:
            if category == "Rifle":
                primer = "Large Rifle Magnum"
        if "magnum" in name.lower() and category == "Handgun" and "32" not in cid:
            primer = "Small Pistol Magnum" if bullet_dia < 10 else "Large Pistol Magnum"
            
        description = hand_curated.get("description")
        if not description:
            description = f"Calibre d'arme {'de poing' if category == 'Handgun' else 'd\'épaule'} d'origine de type {rim_type.lower()}, développé et utilisé principalement en {country}. Ce calibre est entièrement pris en charge par le simulateur de balistique intérieure du site."
            
        item = {
            "id": cid,
            "name": name,
            "aliases": aliases,
            "category": category,
            "bullet_diameter_mm": bullet_dia,
            "bullet_diameter_in": round(bullet_dia / 25.4, 3),
            "case_length_mm": case_len,
            "rim_diameter_mm": round(rim, 2),
            "rim_type": rim_type,
            "base_diameter_mm": round(base, 2),
            "shoulder_diameter_mm": round(shoulder, 2) if shoulder else None,
            "neck_diameter_mm": round(neck, 2),
            "max_pressure_bar": pmax,
            "case_volume_cm3": round(case_vol, 3) if case_vol else None,
            "primer_type": primer,
            "intro_year": intro_year,
            "origin_country": country,
            "description": description,
            "wiki_url": WIKI_LINKS.get(cid),
            "data_note": ESTIMATED_NOTES.get(cid)
        }
        if cid in processed_ids:
            for existing_item in merged_list:
                if existing_item["id"] == cid:
                    for alias in aliases:
                        if alias not in existing_item["aliases"]:
                            existing_item["aliases"].append(alias)
                    break
            continue
            
        merged_list.append(item)
        processed_ids.add(cid)
        
    # 2. Add hand-curated calibers that are NOT in the simulator (like rimfires and specific revolvers)
    for cid, hand_val in hand_curated_metadata.items():
        if cid in processed_ids:
            continue
            
        # Determine defaults for missing dimensions in hand-curated list
        rim = 7.06
        base = 5.74
        shoulder = None
        neck = 5.72
        bullet = 5.72
        case_len = 15.57
        category = "Rimfire"
        rim_type = "Rimmed"
        pmax = 1700
        case_vol = 0.36
        primer = "Rimfire"
        aliases = []
        
        if cid == "22_lr":
            pass
        elif cid == "22_wmr":
            rim, base, neck, bullet, case_len, pmax = 7.40, 6.13, 6.10, 5.69, 26.80, 1610
            case_vol = 0.70
        elif cid == "17_hmr":
            rim, base, shoulder, neck, bullet, case_len, pmax = 7.40, 6.13, 5.70, 4.80, 4.38, 26.80, 1800
            case_vol = 0.65
        elif cid == "9x21_imi":
            rim, base, neck, bullet, case_len, pmax, category, rim_type, primer = 9.92, 9.90, 9.63, 9.03, 21.15, 2350, "Handgun", "Rimless", "Small Pistol"
            case_vol = 0.62
        elif cid == "763_mauser":
            rim, base, shoulder, neck, bullet, case_len, pmax, category, rim_type, primer = 9.90, 9.85, 9.60, 8.46, 7.86, 25.15, 2250, "Handgun", "Rimless", "Small Pistol"
            case_vol = 0.78
        elif cid == "44_special":
            rim, base, neck, bullet, case_len, pmax, category, rim_type, primer = 13.06, 11.61, 11.61, 10.97, 29.46, 1100, "Handgun", "Rimmed", "Large Pistol"
            case_vol = 1.62
        elif cid == "75_swiss_rev":
            rim, base, neck, bullet, case_len, pmax, category, rim_type, primer = 9.50, 8.80, 8.40, 7.82, 22.60, 1100, "Handgun", "Rimmed", "Small Pistol"
            case_vol = 0.75
        elif cid == "8mm_lebel_rev":
            rim, base, neck, bullet, case_len, pmax, category, rim_type, primer = 10.40, 9.75, 9.00, 8.35, 27.20, 1150, "Handgun", "Rimmed", "Small Pistol"
            case_vol = 0.95
        # --- Cotes ajoutées (CIP/SAAMI via Wikipédia) : cartouches qui héritaient à tort des valeurs .22 LR ---
        elif cid == "9x18_makarov":
            rim, base, neck, bullet, case_len, pmax, category, rim_type, primer = 9.95, 9.95, 9.91, 9.27, 18.10, 1620, "Handgun", "Rimless", "Small Pistol"
            case_vol = 0.83
        elif cid == "762x25_tokarev":
            rim, base, shoulder, neck, bullet, case_len, pmax, category, rim_type, primer = 9.95, 9.83, 9.48, 8.50, 7.85, 25.00, 2500, "Handgun", "Rimless", "Small Pistol"
            case_vol = 1.09
        elif cid == "765_luger":
            rim, base, neck, bullet, case_len, pmax, category, rim_type, primer = 9.98, 9.93, 8.43, 7.85, 21.59, 2350, "Handgun", "Rimless", "Small Pistol"
            case_vol = 0.93
        elif cid == "25_acp":
            rim, base, neck, bullet, case_len, pmax, category, rim_type, primer = 7.70, 7.10, 7.00, 6.38, 15.60, 1700, "Handgun", "Semi-rimmed", "Small Pistol"
            case_vol = 0.30
        elif cid == "32_acp":
            rim, base, neck, bullet, case_len, pmax, category, rim_type, primer = 9.10, 8.60, 8.55, 7.94, 17.30, 1410, "Handgun", "Semi-rimmed", "Small Pistol"
            case_vol = 0.55
        elif cid == "32_sw_long":
            rim, base, neck, bullet, case_len, pmax, category, rim_type, primer = 9.50, 8.60, 8.60, 7.90, 23.40, 1000, "Handgun", "Rimmed", "Small Pistol"
            case_vol = 0.95
        elif cid == "500_sw_mag":
            rim, base, neck, bullet, case_len, pmax, category, rim_type, primer = 14.10, 13.40, 13.40, 12.70, 41.30, 4100, "Handgun", "Semi-rimmed", "Large Rifle"
            case_vol = 3.50
        elif cid == "44_40_win":
            rim, base, shoulder, neck, bullet, case_len, pmax, category, rim_type, primer = 13.30, 12.00, 11.60, 11.30, 10.90, 33.10, 760, "Rifle", "Rimmed", "Large Pistol"
            case_vol = 2.60
        elif cid == "57x28_fn":
            rim, base, shoulder, neck, bullet, case_len, pmax, category, rim_type, primer = 7.80, 7.95, 7.95, 6.38, 5.70, 28.90, 3450, "Handgun", "Rebated", "Small Rifle"
            case_vol = 0.90
        elif cid == "545x39_m74":
            rim, base, shoulder, neck, bullet, case_len, pmax, category, rim_type, primer = 10.00, 10.00, 9.25, 6.29, 5.60, 39.82, 3550, "Rifle", "Rimless", "Small Rifle"
            case_vol = 1.75
        elif cid == "220_swift":
            rim, base, shoulder, neck, bullet, case_len, pmax, category, rim_type, primer = 12.00, 11.30, 10.20, 6.60, 5.70, 56.00, 4300, "Rifle", "Semi-rimmed", "Large Rifle"
            case_vol = 3.00
        elif cid == "75x54_french":
            rim, base, shoulder, neck, bullet, case_len, pmax, category, rim_type, primer = 12.34, 12.25, 11.30, 8.66, 7.84, 54.00, 3800, "Rifle", "Rimless", "Large Rifle"
            case_vol = 3.76
        elif cid == "765_argentined":
            rim, base, shoulder, neck, bullet, case_len, pmax, category, rim_type, primer = 12.05, 12.01, 10.90, 8.78, 7.94, 53.60, 3900, "Rifle", "Rimless", "Large Rifle"
            case_vol = 3.70
        elif cid == "8x50r_lebel":
            rim, base, shoulder, neck, bullet, case_len, pmax, category, rim_type, primer = 16.00, 13.77, 11.42, 8.85, 8.30, 50.50, 3200, "Rifle", "Rimmed", "Large Rifle"
            case_vol = 4.00
        elif cid == "450_bushmaster":
            rim, base, neck, bullet, case_len, pmax, category, rim_type, primer = 12.01, 12.70, 12.19, 11.48, 43.20, 2650, "Rifle", "Rebated", "Large Rifle"
            case_vol = 3.86
        elif cid == "408_cheytac":
            rim, base, shoulder, neck, bullet, case_len, pmax, category, rim_type, primer = 16.25, 16.18, 15.24, 11.12, 10.36, 77.21, 4400, "Rifle", "Rimless", "Large Rifle Magnum"
            case_vol = 10.32
        elif cid == "416_barrett":
            rim, base, shoulder, neck, bullet, case_len, pmax, category, rim_type, primer = 20.40, 20.40, 18.50, 11.60, 10.60, 83.00, 4000, "Rifle", "Rimless", "Large Rifle Magnum"
            case_vol = 13.00
        elif cid == "50_bmg":
            rim, base, shoulder, neck, bullet, case_len, pmax, category, rim_type, primer = 20.42, 20.42, 18.14, 14.22, 12.65, 99.31, 3700, "Rifle", "Rimless", "Large Rifle Magnum"
            case_vol = 18.97
        elif cid == "46x30_hk":
            rim, base, shoulder, neck, bullet, case_len, pmax, category, rim_type, primer = 8.00, 8.02, 7.75, 5.31, 4.65, 30.50, 4000, "Handgun", "Rimless", "Small Rifle"
            case_vol = 0.87
            aliases = ["4.6x30", "4.6 mm x 30", "4.6mm HK"]
        elif cid == "556x45_nato":
            rim, base, shoulder, neck, bullet, case_len, pmax, category, rim_type, primer = 9.60, 9.58, 9.00, 6.43, 5.70, 44.70, 4300, "Rifle", "Rimless", "Small Rifle"
            case_vol = 1.85
            aliases = ["5.56 NATO", "5.56x45", "5.56 mm x 45", "SS109", "M855"]
        elif cid == "762x51_nato":
            rim, base, shoulder, neck, bullet, case_len, pmax, category, rim_type, primer = 12.00, 11.90, 11.50, 8.80, 7.82, 51.20, 4150, "Rifle", "Rimless", "Large Rifle"
            case_vol = 3.38
            aliases = ["7.62 NATO", "7.62x51", "7.62 mm x 51"]

        # Garde-fou : signale toute cartouche curée tombée sur les valeurs .22 LR par défaut.
        if cid != "22_lr" and bullet == 5.72 and case_len == 15.57 and neck == 5.72:
            print(f"  /!\\ '{cid}' sans cotes dediees : valeurs .22 LR par defaut — entree a completer.")

        item = {
            "id": cid,
            "name": hand_val["name"],
            "aliases": [hand_val["name"]] + aliases,
            "category": category,
            "bullet_diameter_mm": bullet,
            "bullet_diameter_in": round(bullet / 25.4, 3),
            "case_length_mm": case_len,
            "rim_diameter_mm": rim,
            "rim_type": rim_type,
            "base_diameter_mm": base,
            "shoulder_diameter_mm": shoulder,
            "neck_diameter_mm": neck,
            "max_pressure_bar": pmax,
            "case_volume_cm3": case_vol,
            "primer_type": primer,
            "intro_year": hand_val["intro_year"],
            "origin_country": hand_val["origin_country"],
            "description": hand_val["description"],
            "wiki_url": WIKI_LINKS.get(cid),
            "data_note": ESTIMATED_NOTES.get(cid)
        }
        
        merged_list.append(item)
        processed_ids.add(cid)
        
    # Sort merged list alphabetically by name
    merged_list.sort(key=lambda x: x["name"])
    
    print(f"Total merged calibers: {len(merged_list)}")
    return merged_list

def make_sqlite_db(output_path, calibers_list):
    print(f"Writing SQLite database at {output_path}...")
    if os.path.exists(output_path):
        os.remove(output_path)
        
    conn = sqlite3.connect(output_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS calibers (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        aliases TEXT,
        category TEXT NOT NULL,
        bullet_diameter_mm REAL,
        bullet_diameter_in REAL,
        case_length_mm REAL,
        rim_diameter_mm REAL,
        rim_type TEXT,
        base_diameter_mm REAL,
        shoulder_diameter_mm REAL,
        neck_diameter_mm REAL,
        max_pressure_bar INTEGER,
        case_volume_cm3 REAL,
        primer_type TEXT,
        intro_year INTEGER,
        origin_country TEXT,
        description TEXT
    )
    """)
    
    for item in calibers_list:
        cursor.execute("""
        INSERT INTO calibers (
            id, name, aliases, category, bullet_diameter_mm, bullet_diameter_in,
            case_length_mm, rim_diameter_mm, rim_type, base_diameter_mm,
            shoulder_diameter_mm, neck_diameter_mm, max_pressure_bar, 
            case_volume_cm3, primer_type, intro_year, origin_country, description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item["id"],
            item["name"],
            json.dumps(item["aliases"]),
            item["category"],
            item["bullet_diameter_mm"],
            item["bullet_diameter_in"],
            item["case_length_mm"],
            item["rim_diameter_mm"],
            item["rim_type"],
            item["base_diameter_mm"],
            item["shoulder_diameter_mm"],
            item["neck_diameter_mm"],
            item["max_pressure_bar"],
            item["case_volume_cm3"],
            item["primer_type"],
            item["intro_year"],
            item["origin_country"],
            item["description"]
        ))
        
    conn.commit()
    conn.close()
    print("SQLite write done.")

def make_json_file(output_path, calibers_list):
    print(f"Writing JSON database at {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(calibers_list, f, ensure_ascii=False, indent=4)
    print("JSON write done.")

def make_csv_file(output_path, calibers_list):
    print(f"Writing CSV database at {output_path}...")
    if not calibers_list:
        return
    headers = list(calibers_list[0].keys())
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for item in calibers_list:
            row = []
            for h in headers:
                val = item[h]
                if isinstance(val, list):
                    row.append("|".join(val))
                else:
                    row.append(val)
            writer.writerow(row)
    print("CSV write done.")

def main():
    dest_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(dest_dir, exist_ok=True)
    
    calibers_list = merge_databases()
    
    make_sqlite_db(os.path.join(dest_dir, "calibers.db"), calibers_list)
    make_json_file(os.path.join(dest_dir, "calibers.json"), calibers_list)
    make_csv_file(os.path.join(dest_dir, "calibers.csv"), calibers_list)
    print("All databases successfully compiled and stored with case volume and shoulder diameter.")

if __name__ == "__main__":
    main()
