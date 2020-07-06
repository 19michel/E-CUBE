import pandas as pd
import json

json_file = json.load("data.json")
SDES_path=json_file['SDES']
res_path=json_file['results']

df_sdes=pd.read_csv(SDES_path + "/donnees_elec_iris_2018.csv", sep=';', encoding='latin-1')  # Importation de la base pour vérifier la consommation totale électrique par IRIS
df_sdes['CONSO']= df_sdes['CONSO'].str.replace(',', '.')
df_sdes['CONSO']=pd.to_numeric(df_sdes['CONSO'])
df_iris=df_sdes[['CODE_IRIS','CONSO']]                # On ne conserve que les informations utiles : le numéro d'IRIS et sa consommation
df_iris=df_sdes.groupby(['CODE_IRIS']).sum()

df_test=pd.read_csv(res_path + "/sirene_res.csv", sep=',', usecols=['IRIS', 'conso'])   # Importation d'un fichier résultat

# 1er test
print("Vérification de la positivité des valeurs")

assert df_test['CONSO']>=0, "Erreur : consommation électrique négative"


# 2e test
print("Vérification de la consommation totale de chaque IRIS")

for iris_nb in df_test['IRIS'].unique():
    assert df_test[(,)]['CONSO'].sum()==df_iris.loc[iris_nb,'CONSO'] f"Erreur : mauvaise valeur de consommation pour l'IRIS {iris_nb} "

