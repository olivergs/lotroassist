# -*- coding: utf-8 -*-
###############################################################################
# (C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>
# Map Mark Plugin common map data
###############################################################################

# Map marker types
markertypes={
    'Mob': ['red',(1,0,0)],
    'POI': ['yellow',(1,1,0)],
    'NPC': ['blue',(0,0,1)],
    'Item': ['magenta',(1,0,1)],
    'Milestone': ['darkgrey',(0.3,0.3,0.3)],
    'Stablemaster': ['orange',(1,0.5,0)],
}

# Zones
zones={
    # Region maps
    'Middle Earth': [None,'middleearth.png',0,0,0,0,None],
    'Eriador': [None,'eriador.png',0,0,0,0,'Middle Earth'],
    'Rhovanion': [None,'rhovanion.png',0,0,0,0,'Middle Earth'],
    'Moria': ['moria','moria.png',3.1,-121.9,-22.4,-88,'Middle Earth'],
    'Enedwaith': ['enedwaith','enedwaith.png',-53.5,-31.6,-76.7,-0.6,'Middle Earth'],
    # Area maps
    'Annuminas': ['annuminas','annuminas.png',-15.4,-73.5,-21.2,-65.7,'Evendim'],
    'Angmar': ['angmar','angmar.png',14.7,-42.8,-7.3,-13.6,'Eriador'],
    'Archet': ['archet','archet.png',-24.2,-50.7,-28.3,-45.2,'Bree Land'],
    'Bree Land': ['breeland','breeland.png',-17.7,-65.6,-38.9,-37.4,'Eriador'],
    'Bree Town': ['breetown','breetown.png',-28,-54.6,-33.1,-47.9,'Bree Land'],
    'Caras Galadhon': ['carasgaladhon','carasgaladhon.png',-12.9,-70,-17.1,-64.4,'Lothlórien'],
    'Durin\'s Way': ['durins_way','durinsway.png',2.1,-114.1,-9.8,-98.1,'Moria'],
    'Ered Luin': ['ered_luin','eredluin.png',-12.6,-113,-32.3,-86.6,'Eriador'],
    'Eregion': ['eregion','eregion.png',-35.3,-23.8,-57.9,6.5,'Eriador'],
    'Ettenmoors': ['ettenmoors','ettenmoors.png',-10,-24.3,-22,-8.3,'Eriador'],
    'Evendim': ['evendim','evendim.png',-1.6,-82.6,-24.4,-52.3,'Eriador'],
    'Flaming Deeps': ['flaming_deeps','flamingdeeps.png',-12.3,-112.2,-18,-104.7,'Moria'],
    'Forochel': ['forochel','forochel.png',24.9,-92.8,-5.7,-51.9,'Eriador'],
    'Foundations of Stone': ['foundations_of_stone','foundationsofstone.png',-10.5,-102.9,-16.4,-95,'Moria'],
    'Lone-Lands': ['lone_lands','lonelands.png',-26.2,-44.3,-43.7,-20.9,'Eriador'],
    'Lothlórien': ['lothlorien','lothlorien.png',-4.6,-82,-20.4,-61.0,'Rhovanion'],
    'Mirkwood': ['mirkwood','mirkwood.png',-4.9,-63.6,-23.5,-38.8,'Rhovanion'],
    'Misty Mountains': ['misty_mountains','mistymountains.png',-14.6,-11.9,-33.2,12.9,'Eriador'],
    'North Downs': ['north_downs','northdowns.png',-1,-60.5,-22.2,-32.2,'Eriador'],
    'Northern Barrow-Downs': ['nothern_barrow_downs','northernbarrowdowns.png',-29.8,-57.3,-33.3,-52.7,'Bree Land'],
    'Nud-Melek': ['nud_melek','nudmelek.png',-3.9,-105.3,-12.2,-94.1,'Moria'],
    'Old Forest': ['old_forest','oldforest.png',-29.2,-65.3,-38.9,-52.3,'Bree Land'],
    'Redhorn Lodes': ['redhorn_lodes','redhornlodes.png',-9.3,-109.1,-16.3,-99.8,'Moria'],
    'Rivendell': ['rivendell','rivendell.png',-26.3,-9.4,-33.5,0.3,'Trollshaws'],
    'Southern Barrow-Downs': ['southern_barrow_downs','southernbarrowdowns.png',-32.6,-57.8,-37,-51.9,'Bree Land'],
    'The Grand Stair': ['the_grand_stair','grandstair.png',74,-141.5,69.3,-135.2,'Redhorn Lodes'],
    'The Great Delving': ['the_great_delving','greatdelving.png',-4.9,-117.2,-10.3,-110.1,'Moria'],
    'The Silvertine Lodes': ['the_silvertine_lodes','silvertinelodes.png',-8.5,-116.2,-14,-108.8,'Moria'],
    'The Shire': ['the_shire','theshire.png',-22.9,-80.9,-38.8,-59.8,'Eriador'],
    'The Walls of Moria': ['the_walls_of_moria','wallsofmoria.png',-48.5,-9,-54,-1.6,'Eregion'],
    'The Water-Works': ['the_water_works','waterworks.png',-12.3,-120.5,-22.5,-106.8,'Moria'],
    'Thorin\'s Gate': ['thorins_gate','thorinsgate.png',-11.2,-106.8,-17.2,-98.8,'Ered Luin'],
    'Trollshaws': ['trollshaws','trollshaws.png',-20.8,-26.3,-41.3,0.9,'Eriador'],
    'Zelem-Melek': ['zelem_melek','zelemmelek.png',-3.8,-114.0,-13.8,-100.7,'Moria'],
    'Zirakzigil': ['zirakzigil','zirakzigil.png',17.8,-113.5,11.5,-105,'Moria'],
    # Homesteads
    'Bree Land Homesteads': [None,'breelandhomesteads.png',-34,-50,-38,-44.6,'Bree Land'],
    'Falathlorn Homesteads': [None,'falathlornhomesteads.png',-24.3,-93.6,-28.4,-88.6,'Ered Luin'],
    'Shire Homesteads': [None,'shirehomesteads.png',-36.6,-77.4,-38.7,-73.3,'The Shire'],
    'Thorin\'s Hall Homesteads': [None,'thorinshallhomesteads.png',-13.2,-109.9,-17.2,-104.6,'Thorin\'s Gate'],
}

# Map linking
maplinks={
    'Middle Earth': {
        (726,369,1017,417): 'Eriador',
        (1140,458,1308,488): 'Moria',
        (1317,384,1646,432): 'Rhovanion',
        (969,418,1136,551): 'Enedwaith'
    },
    'Eriador': {
        (1310,233,1468,258): 'Angmar',
        (1078,614,1272,642): 'Bree Land',
        (526,436,708,466): 'Ered Luin',
        (1536,786,1690,814): 'Eregion',
        (1424,432,1658,462): 'Ettenmoors',
        (854,480,1020,508): 'Evendim',
        (788,182,964,212): 'Forochel',
        (1258,546,1464,578): 'Lone-Lands',
        (1652,370,1856,416): 'Misty Mountains',
        (1110,390,1355,420): 'North Downs',
        (1702,980,1888,1026): 'Rhovanion',
        (808,618,990,650): 'The Shire',
        (1514,572,1738,600): 'Trollshaws',
    },
    'Moria': {
        (120,478,260,524): 'The Walls of Moria',
        (350,458,614,528): 'The Great Delving',
        (398,616,662,690): 'The Silvertine Lodes',
        (370,904,565,1000): 'The Water-Works',
        (724,282,1076,324): 'Durin\'s Way',
        (656,478,1010,514): 'Zelem-Melek',
        (872,650,1094,718): 'Redhorn Lodes',
        (656,814,872,906): 'Flaming Deeps',
        (1046,496,1336,528): 'Nud-Melek',
        (1164,752,1498,816): 'Foundations of Stone',
        (1462,128,1556,284): 'Zirakzigil',
        (1538,474,1662,538): 'Lothlórien',
    },
    'Rhovanion': {
        (45,441,195,488): 'Eriador',
        (410,468,630,500): 'Moria',
        (255,246,630,624): 'Misty Mountains',
        (644,495,940,536): 'Lothlórien',
        (986,150,1182,399): 'Mirkwood',
    },
    'Archet': {
        (302,1140,496,1167): 'Bree Land',
    },
    'Bree Land': {
        (1296,954,1342,990): 'Bree Land Homesteads',
        (876,700,992,732): 'Bree Town',
        (1674,924,1899,952): 'Lone-Lands',
        (788,30,1050,56): 'North Downs',
        (1482,30,1722,56): 'North Downs',
        (662,740,790,854): 'Northern Barrow-Downs',
        (344,862,576,892): 'Old Forest',
        (662,855,790,1008): 'Southern Barrow-Downs',
        (0,644,122,688): 'The Shire',
    },
    'Bree Town': {
        (20,314,224,362): 'Bree Land',
        (1480,616,1666,648): 'Bree Land',
        (1440,1056,1654,1104): 'Bree Land',
    },
    'Durin\'s Way': {
        (1516,874,1722,924): 'Nud-Melek',
        (58,836,374,886): 'The Great Delving',
        (870,878,1112,922): 'Zelem-Melek',
        (310,410,482,462): 'Zirakzigil',
    },
    'Enedwaith': {
        (1064,62,1233,91): 'Eregion',
    },
    'Ered Luin': {
        (1594,746,1640,782): 'Falathlorn Homesteads',
        (1608,782,1828,808): 'The Shire',
        (567,171,610,207): 'Thorin\'s Hall Homesteads',
        (484,82,908,128): 'Thorin\'s Gate',
    },
    'Eregion': {
        (150,69,384,111): 'Trollshaws',
        (1260,16,1500,56): 'Trollshaws',
        (1148,874,1334,922): 'The Walls of Moria',
        (1432,828,1530,868): 'Moria',
    },
    'Evendim': {
        (676,861,921,889): 'Annuminas',
        (1311,31,1524,55): 'Forochel',
        (1624,487,1855,535): 'North Downs',
        (717,1065,855,1111): 'The Shire',
    },
    'Flaming Deeps': {
        (1604,646,1758,714): 'Redhorn Lodes',
        (110,698,344,746): 'The Water-Works',
        (796,58,1054,104): 'Zelem-Melek',
    },
    'Forochel': {
        (1306,1150,1510,1180): 'Evendim',
    },
    'Foundations of Stone': {
        (242,108,444,156): 'Nud-Melek',
        (44,226,198,294): 'Redhorn Lodes',
    },
    'Lone-Lands': {
        (57,99,231,120): 'Bree Land',
        (4,573,177,594): 'Bree Land',
        (1731,436,1918,458): 'Trollshaws',
    },
    'Lothlórien': {
        (1197,699,1563,784): 'Caras Galadhon',
        (1690,52,1881,99): 'Mirkwood',
        (134,138,252,189): 'Moria',
    },
    'Mirkwood': {
        (20,711,147,744): 'Lothlórien',
    },
    'Misty Mountains': {
        (504,770,712,792): 'Rivendell',
        (402,957,681,993): 'Rivendell',
    },
    'North Downs': {
        (1304,154,1488,184): 'Angmar',
        (1710,222,1898,250): 'Angmar',
        (394,1058,604,1086): 'Bree Land',
        (32,314,168,354): 'Evendim',
    },
    'Northern Barrow-Downs': {
        (942,147,1206,200): 'Bree Land',
        (1318,754,1580,808): 'Bree Land',
        (372,686,516,738): 'Old Forest',
        (1244,1102,1548,1156): 'Southern Barrow-Downs',
    },
    'Nud-Melek': {
        (122,106,234,170): 'Durin\'s Way',
        (900,38,1014,100): 'Durin\'s Way',
        (544,1074,740,1154): 'Foundations of Stone',
        (1728,508,1848,572): 'Lothlórien',
        (380,868,516,932): 'Redhorn Lodes',
        (50,454,262,500): 'Zelem-Melek',
    },
    'Old Forest': {
        (486,382,536,600): 'Bree Land',
        (1000,50,1169,67): 'Bree Land',
        (1400,354,1612,502): 'Northern Barrow-Downs',
    },
    'Redhorn Lodes': {
        (1005,129,1203,177): 'The Grand Stair',
        (1377,441,1606,508): 'Foundations of Stone',
        (486,1035,634,1101): 'Flaming Deeps',
        (1353,171,1560,214): 'Nud-Melek',
        (322,378,572,424): 'Zelem-Melek',
    },
    'Rivendell': {
        (1144,52,1580,80): 'Misty Mountains',
        (490,1068,820,1102): 'Trollshaws',
    },
    'Southern Barrow-Downs': {
        (1446,612,1616,634): 'Bree Land',
        (1005,42,1268,86): 'Northern Barrow-Downs',
    },
    'The Grand Stair': {
        (879,238,1119,294): 'Nud-Melek',
        (861,885,1060,969): 'Redhorn Lodes',
    },
    'The Great Delving': {
        (1206,184,1424,234): 'Durin\'s Way',
        (1226,946,1500,990): 'The Silvertine Lodes',
        (22,576,180,628): 'The Walls of Moria',
        (1722,626,1916,662): 'Zelem-Melek',
    },
    'The Shire': {
        (1740,610,1886,650): 'Bree Land',
        (219,232,357,277): 'Ered Luin',
        (933,42,1058,81): 'Evendim',
        (484,1028,700,1074): 'Shire Homesteads',
    },
    'The Silvertine Lodes': {
        (852,32,1050,70): 'The Great Delving',
        (777,1060,972,1101): 'The Water-Works',
    },
    'The Walls of Moria': {
        (6,508,154,552): 'Eregion',
        (1364,718,1546,790): 'Moria',
        (1666,686,1863,730): 'Rhovanion',
    },
    'The Water-Works': {
        (1068,10,1196,58): 'Flaming Deeps',
        (1468,368,1574,420): 'The Silvertine Lodes',
    },
    'Thorin\'s Gate': {
        (910,1154,1144,1178): 'Ered Luin',
        (440,874,492,920): 'Thorin\'s Hall Homesteads',
    },
    'Trollshaws': {
        (912,1146,1100,1170): 'Eregion',
        (1494,992,1680,1016): 'Eregion',
        (48,638,224,662): 'Lone-Lands',
        (1380,255,1730,280): 'Misty Mountains',
    },
    'Zelem-Melek': {
        (1034,38,1248,81): 'Durin\'s Way',
        (758,208,974,256): 'Durin\'s Way',
        (910,1102,1120,1166): 'Flaming Deeps',
        (1416,436,1580,471): 'Nud-Melek',
        (1060,888,1208,956): 'Redhorn Lodes',
        (464,436,668,472): 'The Great Delving',
    },
    'Zirakzigil': {
        (1034,1026,1167,1106): 'Durin\'s Way',
    },
}
