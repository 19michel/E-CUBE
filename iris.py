

import shapely
import shapely.geometry
from shapely.strtree import STRtree
import shapefile
import pandas as pd
from math import sin, cos, sqrt, pow, log, pi, tan, exp
from pyproj import Proj, transform

##On commence par ouvrir les différents fichiers

folder="/mnt/c/Users/guera/projects/E-CUBE"

poste_elec = pd.read_csv(folder+"/data/postes-electriques-rte.csv", sep=';')
siren_eta_geo = pd.read_csv(folder+"/data/SIREN/StockEtablissementActif_utf8_geo.csv", sep=',',usecols=["siren", "siret","longitude","latitude"], nrows=10)
siren_ul = pd.read_csv(folder+"/data/SIREN/StockUniteLegale_utf8.csv", sep=',',usecols=["siren", "categorieJuridiqueUniteLegale"], nrows=10)
print("loaded")

#Ensuite, on supprime les auto-entrepreneurs de la base de données SIREN

print(siren_eta_geo.size)
print(siren_ul.size)
siren=siren_eta_geo.merge(siren_ul)
print(siren.size)
siren = siren.loc[siren.loc[:, "categorieJuridiqueUniteLegale"] != 1000]
print(siren.size)

#On charge le contour des IRIS pour pouvoir déterminer l'IRIS d'un point en particulier

file_name="/mnt/c/Users/guera/projects/E-CUBE/data/CONTOURS-IRIS_2-1__SHP__FRA_2020-01-01/CONTOURS-IRIS/1_DONNEES_LIVRAISON_2020-01-00139/CONTOURS-IRIS_2-1_SHP_LAMB93_FXX-2019/CONTOURS-IRIS.shp"

sh = shapefile.Reader(file_name)
shapes= sh.shapes()


assert shapes[0].shapeType==5

p=[]
for i in range(len(shapes)):
    p.append(shapely.geometry.Polygon(shapes[i].points))

tree=STRtree(p)

query_geom=shapely.geometry.Point(498282,6741165)

print(tree.query(query_geom))

L93_Proj = Proj(init='epsg:2154')
WGS_Proj = Proj(init='epsg:4326')
x1,y1 = 47.7982506, 0.2997251
x2,y2 = transform(WGS_Proj,L93_Proj,y1,x1)
print(x2,y2)