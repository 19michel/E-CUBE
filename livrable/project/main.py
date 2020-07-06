## Calcul des IRIS


import pandas as pd
import time
import shapely
import shapely.geometry
from shapely.strtree import STRtree
import shapefile
from pyproj import Proj, transform, CRS
import scipy.stats
import scipy.optimize
import json

# Lecture des chemins d'accès situés dans le fichier data.json

json_file = json.load("data.json")
SIREN_path=json_file['SIREN']
CLAP_path=json_file['CLAP']
SDES_path=json_file['SDES']
IRIS_path=json_file['IRIS']
data_path=json_file['data']

# Importation des bases de données SIRENE

def siren_eta_geo_importforIRIS():
    siren_eta_geo = pd.read_csv(SIREN_path + "/StockEtablissementActif_utf8_geo.csv", sep=',',usecols=["siren", "siret", "codeCommuneEtablissement", "longitude", "latitude"])
    return siren_eta_geo
    
def siren_ul_importforIRIS():
    siren_ul = pd.read_csv(SIREN_path + "/StockUniteLegale_utf8.csv", sep=',',usecols=["siren", "categorieJuridiqueUniteLegale"])
    return siren_ul



# Importation des contours des IRIS donnés par l'IGN

def shapes_importforIRIS():

    file_name_metro=IRIS_path + "/CONTOURS-IRIS_2-1_SHP_LAMB93_FXX-2019/CONTOURS-IRIS.shp"
    sh_metro = shapefile.Reader(file_name_metro)        # Le module shapefile permet de lire des fichiers .shp
    shapes_metro= sh_metro.shapes()                     
    
    file_name_guad=IRIS_path +"/CONTOURS-IRIS_2-1_SHP_RGAF09UTM20_GLP-2019/CONTOURS-IRIS.shp"
    sh_guad = shapefile.Reader(file_name_guad)
    shapes_guad= sh_guad.shapes()
    
    file_name_mart=IRIS_path +"/CONTOURS-IRIS_2-1_SHP_RGAF09UTM20_MTQ-2019/CONTOURS-IRIS.shp"
    sh_mart = shapefile.Reader(file_name_mart)
    shapes_mart= sh_mart.shapes()
    
    file_name_may=IRIS_path +"/CONTOURS-IRIS_2-1_SHP_RGM04UTM38S_MYT-2019/CONTOURS-IRIS.shp"
    sh_may = shapefile.Reader(file_name_may)
    shapes_may= sh_may.shapes()
    
    file_name_reu=IRIS_path +"/CONTOURS-IRIS_2-1_SHP_RGR92UTM40S_REU-2019/CONTOURS-IRIS.shp"
    sh_reu = shapefile.Reader(file_name_reu)
    shapes_reu= sh_reu.shapes()
    
    file_name_guy=IRIS_path +"/CONTOURS-IRIS_2-1_SHP_UTM22RGFG95_GUF-2019/CONTOURS-IRIS.shp"
    sh_guy = shapefile.Reader(file_name_guy)
    shapes_guy= sh_guy.shapes()
    
    return (shapes_metro, shapes_guad, shapes_mart, shapes_may, shapes_reu, shapes_guy)



# Récupération des correspondances entre les contours de chaque IRIS et le nom de chaque IRIS

def iris_dfs_importforIRIS():

    from simpledbf import Dbf5          # Le module simpledbf permet de lire des fichiers .dbf
    iris_metro_dbf=Dbf5(IRIS_path + "/CONTOURS-IRIS_2-1_SHP_LAMB93_FXX-2019/CONTOURS-IRIS.dbf")
    iris_metro_df=iris_metro_dbf.to_dataframe()
    
    iris_guad_dbf=Dbf5(IRIS_path + "/CONTOURS-IRIS_2-1_SHP_RGAF09UTM20_GLP-2019/CONTOURS-IRIS.dbf")
    iris_guad_df=iris_guad_dbf.to_dataframe()
    
    iris_mart_dbf=Dbf5(IRIS_path + "/CONTOURS-IRIS_2-1_SHP_RGAF09UTM20_MTQ-2019/CONTOURS-IRIS.dbf")
    iris_mart_df=iris_mart_dbf.to_dataframe()
    
    iris_may_dbf=Dbf5(IRIS_path + "/CONTOURS-IRIS_2-1_SHP_RGM04UTM38S_MYT-2019/CONTOURS-IRIS.dbf")
    iris_may_df=iris_may_dbf.to_dataframe()
    
    iris_reu_dbf=Dbf5(IRIS_path + "/CONTOURS-IRIS_2-1_SHP_RGR92UTM40S_REU-2019/CONTOURS-IRIS.dbf")
    iris_reu_df=iris_reu_dbf.to_dataframe()
    
    iris_guy_dbf=Dbf5(IRIS_path + "/CONTOURS-IRIS_2-1_SHP_UTM22RGFG95_GUF-2019/CONTOURS-IRIS.dbf")
    iris_guy_df=iris_guy_dbf.to_dataframe()
    
    return (iris_metro_df, iris_guad_df, iris_mart_df, iris_may_df, iris_reu_df, iris_guy_df)



# Première sélection : suppression des personnes physiques dans la liste des établissements


def phys_del():

    siren = siren_eta_geo.merge(siren_ul)
    siren_without_auto = siren.loc[siren.loc[:, "categorieJuridiqueUniteLegale"] != 1000]   # On supprime les lignes où la catégorie juridique légale vaut 1000 car cela correspond à des personnes physiques



# Récupération des différentes projections géographiques utilisées par l'IGN

# On utilise le module PyProj

#Lambert 93 -> France Metropolitaine
crs_L93 = CRS.from_epsg(2154)
L93_Proj = Proj(crs_L93)

#WGS -> coordonnées longitude, latitude
crs_WGS = CRS.from_epsg(4326)
WGS_Proj = Proj(crs_WGS)

#RGAF09UTM20 -> Antilles Françaises (Guadeloupe, Martinique)
crs_RGAF09UTM20 = CRS.from_epsg(5490)
RGAF09UTM20_Proj = Proj(crs_RGAF09UTM20)

#RGFG95UTM22 -> Guyane française
crs_RGFG95UTM22 = CRS.from_epsg(2972)
RGFG95UTM22_Proj = Proj(crs_RGFG95UTM22)

#RGR92UTM40S -> Réunion
crs_RGR92UTM40S = CRS.from_epsg(2975)
RGR92UTM40S_Proj = Proj(crs_RGR92UTM40S)

#RGM04UTM38S -> Mayotte
crs_RGM04UTM38S = CRS.from_epsg(4471)
RGM04UTM38S_Proj = Proj(crs_RGM04UTM38S)



# Création d'une base de données qui contient les informations nécessaires sur chaque IRIS : numéro, commune, contour

def df_iris():
    
    (shapes_metro, shapes_guad, shapes_mart, shapes_may, shapes_reu, shapes_guy) = shapes_importforIRIS()
    (iris_metro_df, iris_guad_df, iris_mart_df, iris_may_df, iris_reu_df, iris_guy_df) = iris_dfs_importforIRIS()
    
    listcc=[]
    listshape=[]
    listiris=[]
    
    for i in range(len(shapes_metro)):
        cc=iris_metro_df.loc[i,"INSEE_COM"]
        poly=shapely.geometry.Polygon(shapes_metro[i].points)
        iris=iris_metro_df.loc[i,"CODE_IRIS"]
        listcc.append(cc)
        listshape.append(poly)
        listiris.append(iris)
        
    for i in range(len(shapes_guad)):
        cc=iris_guad_df.loc[i,"INSEE_COM"]
        poly=shapely.geometry.Polygon(shapes_guad[i].points)
        iris=iris_guad_df.loc[i,"CODE_IRIS"]
        listcc.append(cc)
        listshape.append(poly)
        listiris.append(iris)
    
    for i in range(len(shapes_mart)):
        cc=iris_mart_df.loc[i,"INSEE_COM"]
        poly=shapely.geometry.Polygon(shapes_mart[i].points)
        iris=iris_mart_df.loc[i,"CODE_IRIS"]
        listcc.append(cc)
        listshape.append(poly)
        listiris.append(iris)
        
    for i in range(len(shapes_may)):
        cc=iris_may_df.loc[i,"INSEE_COM"]
        poly=shapely.geometry.Polygon(shapes_may[i].points)
        iris=iris_may_df.loc[i,"CODE_IRIS"]
        listcc.append(cc)
        listshape.append(poly)
        listiris.append(iris)
        
    for i in range(len(shapes_reu)):
        cc=iris_reu_df.loc[i,"INSEE_COM"]
        poly=shapely.geometry.Polygon(shapes_reu[i].points)
        iris=iris_reu_df.loc[i,"CODE_IRIS"]
        listcc.append(cc)
        listshape.append(poly)
        listiris.append(iris)
        
    for i in range(len(shapes_guy)):
        cc=iris_guy_df.loc[i,"INSEE_COM"]
        poly=shapely.geometry.Polygon(shapes_guy[i].points)
        iris=iris_guy_df.loc[i,"CODE_IRIS"]
        listcc.append(cc)
        listshape.append(poly)
        listiris.append(iris)
    
    communes=pd.DataFrame({'code commune':listcc, 'contour iris':listshape, 'iris':listiris})
    return(communes)

df_iris = df_iris()

# Création d'un dictionnaire qui associe à chaque commune un arbre de recherche contenant tous ses IRIS

def dict_iris():

    d={}
    for i in range(len(df_iris)):
        
        try:
            (p,l)=d[df_iris.iloc[i,0]]     # On vérifie que la commune de la ligne i est déjà une clé du dictionnaire
        except:
            p,l=[],[]
                                   # Sinon, on crée une clé associée à un couple de listes vides
        poly = df_iris.iloc[i,1]
        iris=df_iris.iloc[i,2]
        p.append(poly)
        l.append(iris)
        d[df_iris.iloc[i,0]] = (p,l)   # On ajoute à la liste associé à la clé de la commune l'iris correspondant à la ième ligne de la DataFrame df_iris
    
    for i in d:                     # On parcourt le dictionnaire et on remplace le couple composé de la liste des              contours d'IRIS et la liste des noms d'IRIS de la commune par un autre couple composé d'un dictionnaire qui associe à chaque contour le nom de l'IRIS et d'un R-arbre permettant de trouver l'IRIS contenant des coordonnées données
        p,l=d[i]    
        t=STRtree(p)
        lex=dict((id(p[i]),l[i]) for i in range(len(p)))
        d[i]=(lex,t)
        
    return(d)
    
d=dict_iris()

# Fonction qui permet d'obtenir l'IRIS dans lequel se situe l'établissement de la ième ligne de la base SIRENE
    
def iris_commune_dict(i):
    x2,y2=0,0
    cc=str(siren_without_auto.loc[i,"codeCommuneEtablissement"])    # On récupère le nom de la commune de la ligne i
    if len(cc)==4:
        cc='0'+cc
    try:
        lex,tree=d[cc]                                              # On essaie de récupérer les informations sur la commune dans le dictionnaire dict_iris
    except:
        return None
    if len(lex) == 1:                                               # S'il n'y a qu'un IRIS dans la commune, on obtient le résultat voulu
        return list(lex.values())[0]
        
        
    else:                                                           # Sinon, il faut utiliser le R-arbre pour trouver l'IRIS rechérché
    
        lat=siren_without_auto.loc[i,"latitude"]
        lon=siren_without_auto.loc[i,"longitude"]
        
        # Au préalable, il faut transformer les coordonnées GPS de la base SIRENE en celles utilisées par l'IGN dans les fichiers de contour d'IRIS
        
        if cc[:2]=='97':
            if cc[2]=='1':
                x2,y2 = transform(WGS_Proj,RGAF09UTM20_Proj,lat,lon)    
            elif cc[2]=='2':
                x2,y2 = transform(WGS_Proj,RGAF09UTM20_Proj,lat,lon)
            elif cc[2]=='3':
                x2,y2 = transform(WGS_Proj,RGFG95UTM22_Proj,lat,lon)
            elif cc[2]=='4':
                x2,y2 = transform(WGS_Proj,RGR92UTM40S_Proj,lat,lon)
            elif cc[2]=='5':
                x2,y2 = transform(WGS_Proj,RGM04UTM38S_Proj,lat,lon)
        else:
            x2,y2 = transform(WGS_Proj,L93_Proj,lat,lon)
        query_geom=shapely.geometry.Point(x2,y2)                    # A l'aide du module shapely, on utilise les R-arbres pour trouver la réponse à une requête
        ir=tree.query(query_geom)
        if ir==[]:
            return None
        return lex[id(ir[0])]



# Fonction qui permet d'effectuer le calcul des IRIS en enregistrant le résultat toutes les 10 000 établissements

def save(a,nb):
    global siren_without_auto
    global siren_without_auto_iris
    l=len(siren_without_auto)
    
    for j in range(nb):
        t0=time.time()
        
        df=siren_without_auto.iloc[(a + 10000*j):(a + 10000*(j+1)),:].copy()  # On copie une tranche de 10 000 données de la base SIRENE pour calculer les IRIS
        df['IRIS']=0
        
        for i in range(10000):
            if (a + 10000*j + i) == l:
                break
            df.iloc[i,6]=iris_commune_dict(siren_without_auto.index[a + 10000*j + i])
            
        t1=time.time()
        
        print(t1-t0)            # Affichage du temps pris pour calculer 10 000 IRIS
        print(j+1)
        
        
        #Enregistrement des résultats
        siren_without_auto_iris=pd.concat([siren_without_auto_iris,df], axis=0)
        siren_without_auto_iris.to_csv( SIREN_path + "/StockEtablissementActif_utf8_geo_iris.csv")
        
        

## Manipulation des bases de données

def siren_iris_import():

    siren_iris = pd.read_csv(SIREN_path + "/StockEtablissementActif_utf8_geo_iris_propre.csv", sep=',')
    siren_iris=siren_iris.astype(str)
    return siren_iris
    

def siren_eta_geo_import():

    siren_eta_geo = pd.read_csv(SIREN_path + "/StockEtablissementActif_utf8_geo.csv", sep=',',usecols=["siren", "siret", "activitePrincipaleEtablissement","trancheEffectifsEtablissement"])   # On importe de nouvelles informations de la base SIRENE
    siren_eta_geo = siren_eta_geo.astype(str)
    return siren_eta_geo

df_siren=pd.merge(siren_iris_import(),siren_eta_geo_import())


# Fonction pour supprimer les lignes où il manque des informations importantes ou où il n'y a pas de salariés

def nan_del():
    df_siren=df_siren[(df_siren != 'nan').all(1)]
    df_siren=df_siren[df_siren['trancheEffectifsEtablissement'] != 'NN']
    df_siren=df_siren[df_siren['trancheEffectifsEtablissement'] != '00']
    df_siren=df_siren[df_siren['trancheEffectifsEtablissement'] != '0.0']


# Création d'un MultiIndex

def reindex_siren():

    index=pd.MultiIndex.from_frame(df_siren[['IRIS','activitePrincipaleEtablissement','trancheEffectifsEtablissement','siret']])
    df_siren=df_siren.set_index(index)


# Ajout d'une valeur d'effectifs

eff={'01':1.5, '02':4.0, '03':7.5, '11':14.5, '12':34.5, '21':74.5, '22':149.5, '31':224.5, '32':374.5, '41':749.5, '42':1499.5, '51':3499.5, '52':7499.5, '53':15000, '1.0':1.5, '2.0':4.0, '3.0':7.5, '11.0':14.5, '12.0':34.5, '21.0':74.5, '22.0':149.5, '31.0':224.5, '32.0':374.5, '41.0':749.5, '42.0':1499.5, '51.0':3499.5, '52.0':7499.5, '53.0':15000}

def effec(x):
    return eff[x]
    

def effec_siren():
    
    df_siren['effectifs']=np.vectorize(effec)(df_siren['trancheEffectifsEtablissement'])





# On importe de nouvelles bases de données



def df_conso_commune():
    
#SDES

    # Importation de la base SDES et suppression des données incomplètes (l 313) ou des données inintéressantes (l 315)
    df_sdes=pd.read_csv(SDES_path + "/donnees_elec_iris_2018.csv", sep=';', encoding='latin-1')
    df_sdes.dropna(subset=['CODE_SECTEUR_NAF2'],inplace=True)       
    df_sdes.set_index('OPERATEUR',inplace=True)
    df_sdes.drop(index='RTE',inplace=True)
    
    df_sdes['CODE_COMMUNE']=df_sdes['CODE_IRIS'].str.slice(stop=5)
    index_bis=pd.MultiIndex.from_frame(df_sdes[['CODE_SECTEUR_NAF2','CODE_COMMUNE']])  # Création d'un MultiIndex
    df_sdes.set_index(index_bis,inplace=True)
    df_sdes.sort_index(inplace=True)
    
    df_sdes['CONSO']= df_sdes['CONSO'].str.replace(',', '.')
    df_sdes['CONSO']=pd.to_numeric(df_sdes['CONSO'])
    
    # On ne garde que la valeur de consommation par commune. Le groupby permet de sommer les éventuels doublons qui peuvent exister
    df_conso=df_sdes[['CONSO']]
    df_conso=df_conso.groupby(['CODE_SECTEUR_NAF2','CODE_COMMUNE']).sum()
    
    
#CLAP

    # Importation de la base CLAP et suppression des lignes et colonnes inutiles
    df_clap_poste=pd.read_excel(CLAP_path +"/TD_CLAP2015_NA88_NBSAL.xls")
    df_clap_poste=df_clap_poste.drop([0,1,2,3])
    df_clap_poste.rename(columns=df_clap_poste.iloc[0,:],inplace=True)
    df_clap_poste=df_clap_poste.drop([4])
    df_clap_poste.set_index('CODGEO',inplace=True)
    df_clap_poste.drop(['LIBGEO','DEP','REG','EFF_TOT'],axis=1,inplace=True)
    
    # Création d'un dictionnaire afin d'avoir une correspondance entre les codes NAF de la base SDES (1.0, 2.0, ...) et ceux de la base CLAP (EFF_1.0, EFF_2.0, ...)
    NAF=df_sdes['CODE_SECTEUR_NAF2'].unique()
    NAF_CLAP=np.array(df_clap_poste.columns)
    d=dict((NAF_CLAP[i],NAF[i]) for i in range(len(NAF)))
    
    df_clap_poste.rename(columns=d,inplace=True)
    
    # Transformation de la base de données en une série avec MultiIndex pour retrouver le même index que pour la base df_conso
    s_clap=df_clap_poste.transpose().stack()
    
    
    # Ajout des valeurs d'effectifs, suppression des effectifs nuls, ajout de la valeur de consommation par effectifs X nécessaire pour l'élaboration des densités de probabilité
    df_conso['EFFECTIF']=s_clap
    df_conso_bis=df_conso[(df_conso != 0).all(1)]
    df_conso_bis['X']=df_conso_bis['CONSO']/df_conso_bis['EFFECTIF']
    
    return df_conso_bis


df_conso_commune=df_conso_commune()



## Création des densités

# On obtient l'allure des densités sous forme d'histogrammes

bins=np.arange(0.25,50.25,0.5)
bins_hist=np.arange(0,50.5,0.5)


def dens():
    n=len(NAF)
    Tab=[np.array([]) for i in range(100)]
    for i in range(n):
        j=NAF[i]
        plt.figure(f'{j}')
        plt.title(f'{j}')
        try:
            a=plt.hist(df_conso_commune.loc[(j,)]['X'],bins=bins_hist)
            plt.plot(np.arange(0.25,50.25,0.5),a[0])
            Tab[int(j)]=a[0]
        except:
            None
        plt.savefig(f'figure/NAF2/{j}.png')
    return Tab

Tab = dens()
    

# On modélise les densités par une fonction statistique qui minimise l'erreur quadratique pour approximer les allures précédentes. Les fonctions statistiques sont choisies parmi la liste ci-dessous

dist_names = ['norm', 'beta','gamma', 'pareto', 't', 'lognorm', 'invgamma', 'invgauss',  'loggamma', 'alpha', 'chi', 'chi2']


def model(dist_names):

    model=[np.array([]) for i in range(100)]
    
    n=len(NAF)
    
    for i in range(n):
        j=NAF[i]
        print(j)
        if len(Tab[int(j)]) != 100:
            continue
        try:
            data=df_conso_commune.loc[df_conso_commune['X']<50].loc[(j,),'X'].values.astype(int)
        except:
            continue
        x=bins
        y=2*Tab[int(j)]/len(data)
        
        sse = np.inf
        sse_thr = 0.0010
    
        # Pour chaque distribution
        for name in dist_names:
    
            # Modéliser
            dist = getattr(scipy.stats, name)
            param = dist.fit(data)
    
            # Paramètres
            loc = param[-2]
            scale = param[-1]
            arg = param[:-2]
    
            # PDF
            pdf = dist.pdf(x, *arg, loc=loc, scale=scale)
            # SSE
            model_sse = np.sum((y - pdf)**2)
    
            # Si le SSE est ddiminué, enregistrer la loi
            if model_sse < sse :
                best_pdf = pdf
                sse = model_sse
                best_loc = loc
                best_scale = scale
                best_arg = arg
                best_name = name
    
            # Si en dessous du seuil, quitter la boucle
            if model_sse < sse_thr :
                break
                
        plt.figure(figsize=(12,8))
        plt.plot(x, y, label="Données")
        plt.plot(x, best_pdf, label=best_name, linewidth=3)
        plt.legend(loc='upper right')
        plt.show()
    
        # Détails sur la loi sélectionnée
        print("Selected Model : ", best_name)
        print("Loc. param. : ", best_loc)
        print("Scale param. : ", best_scale)
        print("Other arguments : ", best_arg)
        print("SSE : ", sse)
        
        model[int(j)]=(best_name,best_loc,best_scale,best_arg)
        
    return model


model=model(dist_names)
    


# On ajoute aux paramètres de la modélisation certaines informations comme la valeur du maximum et son argument

def argmax_max_model():
    global model
    n=len(NAF)   
    for i in range(n):
        j=int(NAF[i])
        stat=model[j]
        try:
            dist = getattr(scipy.stats, stat[0])
        except:
            continue
        arr=dist.pdf(bins_hist,*stat[3], loc=stat[1], scale=stat[2])
        y=max(arr)
        ind=np.argmax(arr)
        model[j]=model[j]+(y,ind,)
        
        

## Optimisation pour obtenir les valeurs de consommation

# On cherche à minimiser la valeur de la norme du vecteur contenant les valeurs de consommation de chaque entreprise de l'IRIS

def func_opti(iris_nb):
    
    def fun(X):
        s=0
        for i in range(len(X)):
            ind=df.loc[(iris_nb,)].index[i]
            act=int(ind[0][:2])
            effec=df.iloc[i,5]
            stat=model[act]
            dist = getattr(scipy.stats, stat[0])
            s-=dist.pdf(X[i]/effec,*stat[3],loc=stat[1],scale=stat[2])/stat[4]   # On ajoute ici l'opposé de la densité de probabilité. De plus, on divise par le maximum stat[4] afin de normaliser pour que toutes les entreprises aient la même importance dans l'optimisation
        return s
        
    return fun
    


# On définit les contraintes à respecter


def somme(X):
    return X.sum()
    
def cons(iris_nb):                                                                   # La contrainte principale : l'égalité entre la somme de toutes les consommations des entreprises de l'IRIS et la consommation totale de l'IRIS
    cons = [{'type': 'eq', 'fun': lambda x: somme(x)-df_elec.loc[iris_nb,'CONSO']}]
    return cons
    
def bnds(iris_nb):                                                                   # Une contrainte permettant de respecter le fait que les consommations sont positives
    bndtest=((0,None),)
    bnds=bndtest*len(df.loc[(iris_nb,)])
    return bnds
    

# Finalement, on aboutit à une fonction qui renvoie le résultat de consommation électrique optimisé


def result_opti(iris_nb):


    # On commence par trouver une valeur initiale qui est assez proche des maximums de probabilité
    X0=np.ones(len(df.loc[(iris_nb,)]))
    for i in range(len(df.loc[(iris_nb,)])):
            ind=df.loc[(iris_nb,)].index[i]
            act=int(ind[0][:2])
            effec=df.iloc[i,5]
            stat=model[act]
            X0[i]=max(1,bins_hist[stat[5]]*effec)   # On prend des valeursqui ne sont pas trop proches de 0 pour s'assurer de la positivité
            
    # On normalise cette valeur pour respecter la contrainte d'égalité                   
    X0=(df_elec.loc[iris_nb,'CONSO']/somme(X0))*X0
    
    print(X0)
    print(X0.sum())
    
            
    x=scipy.optimize.minimize(func_opti(iris_nb),X0,method='SLSQP',constraints=cons(iris_nb), bounds=bnds(iris_nb))
    return x




# On définit une fonction pour visualiser les résultats par rapport aux probabilités

def result_plot(nb_iris,x):
    
    for i in range(len(x['x'])):
        
        ind=df.loc[(iris_nb,)].index[i]
        act=int(ind[0][:2])
        effec=df.iloc[i,5]
        stat=model[act]
        dist = getattr(scipy.stats, stat[0])
        y=dist.pdf(bins_hist,*stat[3], loc=stat[1], scale=stat[2])/stat[4]
        plt.plot(bins_84,y)
        plt.scatter(x['x'][i]/effec,dist.pdf(x['x'][i]/effec,*stat[3], loc=stat[1], scale=stat[2])/stat[4])
        plt.show()
        
        
 
# Fonction pour exporter le modèle de densité de probabilité       

def model_export():
    
    dic={'abscisse':bins}
    for i in range(len(NAF)):
        j=int(NAF[i])
        stat=model[j]
        try:
            dist = getattr(scipy.stats, stat[0])
        except:
            continue
        arr=dist.pdf(bins,*stat[3], loc=stat[1], scale=stat[2])
        dic[f'{j}']=arr
    df_saved_naf=pd.DataFrame(data=dic)
    df_saved_naf.to_csv(f'densites/naf_model.csv')




## Prise en compte des différences départementales 

def df_conso_commune_dpt():

    global REG

    df_conso=df_conso_commune()

    def reg(a):         # On ajoute une colonne région à la base précédemment créée pour élaborer les modèles
        return a[:2]
    df_conso.reset_index(inplace=True)
    df_conso['REGION']=np.vectorize(reg)(df_conso['CODE_COMMUNE'])

    REG=df_conso['REGION'].unique() # On récupère la liste des régions

    df_conso.set_index(['REGION','CODE_SECTEUR_NAF2','CODE_COMMUNE'], inplace=True)
    df_conso.sort_index(inplace=True)
    
    return df_conso

df_conso_commune_dpt=df_conso_commune_dpt()


# On obtient l'allure des densités sous forme d'histogrammes


def dens_dpt():

    n=len(NAF)
    m=len(REG)
    Tab=np.zeros((95,100,100))
    for i in range(m):
        
        reg=REG[i]
        print(reg)
        
        for j in range(n):
            
            naf=NAF[j]
            print(naf)
            try:
                a=np.histogram(df_conso_commune_dpt.loc[(reg,naf,)]['X'],bins=bins_hist)
                Tab[int(reg),int(naf)]=a[0]
            except:
                None
    
    return Tab

tab_dpt=dens_dpt()


# Puis on trouve une loi statistique qui correspond à chaque distribution


def model_dpt(dist_names):

    model_area=np.empty((95,100,4), dtype=object)


    n=len(NAF)
    m=len(REG)

    for i in range(m):
        
        reg=REG[i]
        print(reg)
        
        for j in range(n):
            
            naf=NAF[j]
            print(naf)
            
            
            try:
                data=df_conso_commune_dpt.loc[df_conso_commune_dpt['X']<50].loc[(reg,naf,),'X'].values.astype(int)
            except:
                continue
            x=bins
            y=2*Tab_dpt[int(reg),int(naf)]/len(data)

            sse = np.inf

            # Pour chaque distribution
            for name in dist_names:

                # Modéliser
                dist = getattr(scipy.stats, name)
                param = dist.fit(data)

                # Paramètres
                loc = param[-2]
                scale = param[-1]
                arg = param[:-2]

                # PDF
                pdf = dist.pdf(x, *arg, loc=loc, scale=scale)
                # SSE
                model_sse = np.sum((y - pdf)**2)

                # Si le SSE est ddiminué, enregistrer la loi
                if model_sse < sse :
                    best_pdf = pdf
                    sse = model_sse
                    best_loc = loc
                    best_scale = scale
                    best_arg = arg
                    best_name = name


            model_area[int(reg),int(naf)]=np.array([best_name,best_loc,best_scale,best_arg])
    
    return model_area