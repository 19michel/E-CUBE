url='https://pyris.datajazz.io/api'
import pandas as pd
import grequests

poste_elec = pd.read_csv(r"C:\Users\guera\projects\E-CUBE\postes-electriques-rte.csv", sep=';')

poste_elec.set_index("Code poste")

poste_elec['IRIS']= 0

shape=poste_elec.shape

urls=[]
str=''

for i in range(10):
    str = url + "/coords" + "?geojson=false" + f"&lat={poste_elec.loc[i,'Latitude poste (DD)']}" + f"&lon={poste_elec.loc[i,'Longitude poste (DD)']}"
    urls.append(str)
    

reqs = (grequests.get(u, stream=True) for u in urls)

reponse=grequests.map(reqs)

print(reponse)

