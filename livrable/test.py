import pandas as pd

df_test=pd.read_csv(name)

print("Vérification de la positivité des valeurs")


assert df['CONSO']>=0

