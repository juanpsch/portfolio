# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 00:15:24 2020

@author: juanp_schamun
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:20:12 2020

@author: juanp_schamun
"""

import pandas as pd
import re
import numpy as np
import ZonaClass


        
def _mejorarDatos(dfin):
    '''
    Optimiza los imputs mediante manipualcion de strings
    '''    
    
    for i in dfin:    
        try:    
            dfin[i] = dfin[i].str.split().str.join(' ')
            dfin[i] = dfin[i].str.replace('\*\*\*\*\*\*\*\*\*\*','')
        except AttributeError:
            pass
        
    dfin.replace(r'^\s*$', np.NaN, regex=True, inplace=True)  # Vacios y solo espacios son NaN
    dfin.dropna(how='all', inplace=True) # Eliminar filas vacias
    dfin.reset_index(drop=True, inplace=True)
    return dfin

def _agregarInfo(dfin):
    '''
    Agrega info a partir de los datos del imputs mediante
    manipulación de datos.
    '''

    dfin['CRA'] = dfin['CRA'].str.split(pat='.')[0]
    dfin['NumeroCorrelativo'] = dfin['NumeroCorrelativo'].str.split(pat='.')[0]
    dfin['SistemaOBS'] = dfin['Sistema']     
    dfin['Sistema'] = pd.Series(dfin.shape[0]*['SP']).str.cat(dfin['Owner'].str.findall('\d?\d\d\d').str[0])

    return dfin
    

def _cruceDataZonas(dfin, zonas=pd.DataFrame()):
    '''
    Cruza la info de data con las zonas y las completa a ambas:
    Es decir las zonas obtienen los componentes que quedan dentro
    y los componentes obtienen la zona a la que perteneces
    tipo:
        'cartesianas' hace la comparación según X, Y, Z min y max
        'cilíndricas' para x e y se hace según R y THETA. Para ello
        se transforman las coordenadas de los componentes
    '''

    X = dfin.LocationX
    Y = dfin.LocationY
    Z = dfin.LocationZ
    R, THETA = _cartesian2polar(X, Y)
    tipo='cartesianas'

    
    dfin['Zona'] = 'NA'
    zonas['comp'] = [[] for i in zonasDf.index]
    for j, k in zonas.iterrows():        
        if 'tipo' in k.keys():
            tipo = k['tipo']
        if tipo == 'cartesianas':
            aa = ((X >= k['Xmin']) & (X < k['Xmax']) &
                              (Y >= k['Ymin']) & (Y < k['Ymax']) &
                              (Z >= k['Zmin']) & (Z < k['Zmax']))
        elif tipo == 'polares':
            aa = ((R >= k['Rmin']) & (R < k['Rmax']) &
                              (ZonaClass.angulos.incluido(k['THETAmin'], k['THETAmax'], THETA)) &
                              (Z >= k['Zmin']) & (Z < k['Zmax']))
            
        zonas.at[j, 'comp'] = np.nonzero(aa.ravel())[0].tolist()        
#        for m in b:
#            data[m]['Zona']=zonas[j]['Nombre']

    return dfin, zonas


def concatenarData(dataDf, zonasDf):
    '''
    Devuelve los DataFrames resultado del procesamiento de los datos
    de componentes y de las zonas.
    Params:
        dataDf: DataFrame con los datos
        zonasDf: DataFrame con las zonas        
    Devuelve tres DF:
        zonasDf: sobre las zonas
        dataDf: sobre los componentes
        solapDf: sobre el solapamiento entre zonas
    '''

    _mejorarDatos(dataDf)
    _agregarInfo(dataDf)  # mejorar la info
    _cruceDataZonas(dataDf, zonasDf)  # cruzar data con zonas


    zonasDf.set_index('Nombre', inplace=True)  # Define el ìndice del Df Zonas
    zonasDf.comp = [pd.Index(i) for i in zonasDf.comp]  # Transforma comp en índices
    
    # Crea los objetos zona y los incorpora en el Df de Zonas
    zonasDf['OBJ'] = [ZonaClass.zona(**{zonasDf.index.name:i}, **dict(zip(zonasDf.columns, zonasDf.loc[i, :]))) for i in zonasDf.index]
    
    zonasDf['Ncomp'] = [len(i) for i in zonasDf.comp]  # Agrega el Ncomp al df

    solapDf = solapZonas(zonasDf)  # Crea el Df del solapamiento de las zonas

# =============================================================================
#      Asigna las zonas a los componentes
# =============================================================================
    dataDf['Zona'] = [[] for i in range(len(dataDf))]
    for i in zonasDf.index:
        zonaAdd = i
        for j in zonasDf.comp[i]:
            dataDf.loc[j, 'Zona'].append(zonaAdd)
#       Divide en columnas por zona asignada a componentes
    divZonas = pd.DataFrame(dataDf.Zona.values.tolist(), index=dataDf.index)
    divZonas.columns = ['Zona' + str(i) for i in divZonas.columns]
    dataDf = pd.concat([dataDf, divZonas], axis=1)
# =============================================================================
#
# =============================================================================
    dataFinalDf = _agrupByZone(dataDf)  # Armar la data final
    
# =============================================================================
#     
# =============================================================================
        # Dar Formato de numero a los locations del DF
    try:
        dataFinalDf[['LocationX','LocationY','LocationZ']] = dataFinalDf[['LocationX','LocationY','LocationZ']].apply(pd.to_numeric)    
    except KeyError:
        pass

# agregar R y THETA al DF

    dataFinalDf['R'], dataFinalDf['THETA'] = _cartesian2polar(dataFinalDf.LocationX, dataFinalDf.LocationY)

    return dataDf, zonasDf, solapDf, dataFinalDf


def solapZonas(zonasDf):
    '''
    Parte del DataFrame de zonas y corre la funcion solap
    todas contra todas y devuelve un DataFrame de doble Índice
    con las zonas que se solapan


    '''
    solapDic = {i: {j: zonasDf.loc[i, 'OBJ'].solap(zonasDf.loc[j, 'OBJ'])
                for j in zonasDf.index} for i in zonasDf.index}
    solapDf = pd.DataFrame(solapDic)
    solapDf = solapDf.stack()
    ix = pd.Index([(i[0], i[1]) for i in solapDf.index if i[0] != i[1]])
    solapDf = pd.DataFrame(solapDf.loc[ix])
    solapDf.columns = ['OBJ']
    solapDf['Nombre'] = [i.Nombre for i in solapDf['OBJ']]
    solapDf['Xmin'] = [i.Xmin for i in solapDf['OBJ']]
    solapDf['Xmax'] = [i.Xmax for i in solapDf['OBJ']]
    solapDf['Ymin'] = [i.Ymin for i in solapDf['OBJ']]
    solapDf['Ymax'] = [i.Ymax for i in solapDf['OBJ']]
    solapDf['Zmin'] = [i.Zmin for i in solapDf['OBJ']]
    solapDf['Zmax'] = [i.Zmax for i in solapDf['OBJ']]
    solapDf['vol'] = [i.vol for i in solapDf['OBJ']]
    solapDf['comp'] = [i.comp for i in solapDf['OBJ']]
    solapDf['Ncomp'] = [len(i.comp) for i in solapDf['OBJ']]

    return solapDf


def _agrupByZone(dataDf):
    '''
    A partir del Df dataDf crea un nuevo df
    igual al dataDf donde se individualizan los componentes
    por zona. Osea se crean columnas zona1, zona2, ... para indicar
    en todas las zonas donde aparece un componente
    '''
    nZonas = max([len(i) for i in dataDf.Zona])    
    df1 = dataDf
    if nZonas >1:
        for i in range(1, nZonas):
            df = pd.DataFrame(dataDf.loc[dataDf['Zona' + str(i)].notnull()])
            df.loc[:, 'Zona0'] = df.loc[:, 'Zona' + str(i)]
            df1 = pd.concat([df1, df])
        df1.sort_values(by=['Zona0'], inplace=True)
        df1.drop(columns=df1.columns[-(nZonas-1):], inplace=True)
    df1['Nivel'] = _getNivel(df1)

    return df1


def _getNivel(df1):
    '''
    Devuelve el nivel de la Zona de acuerdo a la codificación
    con el format "C25-PLM-4-2-05" con un split con '-' en la cuarta
    posición. Sólo funciona con la codificación con este formato.
    '''
    
    nivelSep = df1.Zona0.str.split(pat='-', expand=True)
    ubiq = min(len(nivelSep.columns)-1, 3)
    nivel = df1.Zona0.str.split(pat='-', expand=True)[ubiq]
    # nivel = 140

    return nivel

def _cartesian2polar(x,y):
        
    '''
    Devuelve las coordenadas polares según x e y en coordenadas catesianas
    parametros: x e y
    devuelve r y theta(en grados)
    
    '''
    r = np.sqrt(x**2 + y**2)
    theta = np.degrees(np.arctan2(y,x)) % 360
    
    return r, theta

inputFiles = 'InputFiles_DDC.dat'
fileZonas = 'RecintosDB_DDC.dat'


Reps = pd.read_csv(inputFiles, header=None, squeeze=True, dtype=str)
dfs = []
NA = ['**********','']
dataDf = pd.concat([pd.read_excel(i, header=1, na_values=NA, index=False) for i in Reps])
dataDf.reset_index(drop=True, inplace=True)
zonasDf = pd.read_csv(fileZonas, sep='\t')

concatenarData(dataDf, zonasDf)
