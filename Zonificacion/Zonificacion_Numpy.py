# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:20:12 2020

@author: juanp_schamun
"""

# Reading an excel file using Python
import xlrd
import numpy as np
import pandas as pd
import ZonaClass
import re

pd.set_option('precision', 2)

def armarZonas(lim=1000, size=10, tipo = 'cartesianas', limR = 1000):
    '''
    tipo = 'cartesianas' o 'polares'
    cartesianas:
            Divide el volumen dado por los límites para (x,y,z)
            entre -lim y lim en size^3 cubos.
    polares:
            Divide el volumen dado por los límites para (R lim = 0 a lim, THETA lim = 0 a 360, z lim = -lim a lim)
            entre porsiones de un cilindro
    '''

    if tipo == 'cartesianas':
        xZone = yZone = zZone = np.column_stack([np.linspace(-lim, lim, size + 1)[:-1],
                                                 np.linspace(-lim, lim, size + 1)[1:]])
        zonasArr = [(i, j, k) for i in xZone for j in yZone for k in zZone]
        zonasArr = np.reshape(zonasArr, [len(zonasArr), 6])
        zonasNames = [(i, j, k) for i, ii in enumerate(xZone) for j, jj
                      in enumerate(yZone) for k, kk in enumerate(zZone)]
        zonasNames = zonasNames
        zonasTit = ['Xmin', 'Xmax', 'Ymin', 'Ymax', 'Zmin', 'Zmax']
        zonasDic = [dict(zip(zonasTit, i)) for i in zonasArr]
        for j, i in enumerate(zonasDic):
            ints = [str(k) for k in zonasNames[j]]                    
            i['Nombre'] = '-'.join(ints)
            i['tipo'] = tipo
            
            
    elif tipo =='polares':
        R = np.linspace(0,limR, size + 1)
        Th = np.linspace(0,360, size +1)
        Z = np.linspace(-lim, lim, size +1)
        rZone = np.column_stack([R[:-1], R[1:]])
        thZone = np.column_stack([Th[:-1], Th[1:]])
        zZone = np.column_stack([Z[:-1], Z[1:]])
        polArr = [(i, j, k) for i in rZone for j in thZone for k in zZone]        
        polArr = np.array(polArr).reshape(len(polArr), 6)
        zonasNames = [(i, j, k) for i, ii in enumerate(rZone) for j, jj
                      in enumerate(thZone) for k, kk in enumerate(zZone)]
        zonasNames = zonasNames
        zonasTit = ['Rmin', 'Rmax', 'THETAmin', 'THETAmax', 'Zmin', 'Zmax']
        zonasDic = [dict(zip(zonasTit, i)) for i in polArr]
        for j, i in enumerate(zonasDic):
            ints = [str(k) for k in zonasNames[j]]                    
            i['Nombre'] = '-'.join(ints)
            i['tipo'] = tipo               
    
    return zonasDic


def getZonas(file):
    '''Obtiene las zonas de un archivo de texto
        con formato
        Nombre Xmin Xmax Ymin Ymax Zmin Zmax
                    '''

    zonas = np.loadtxt(file, dtype=str, delimiter='\t')
    zonasTitNom = zonas[0, 0]
    zonasTitDat = zonas[0, 2::]
    zonasNames = zonas[1::, 0]
    zonasTipo = zonas [1::,1]
    zonasDat = np.array(zonas[1::, 2::], dtype=float)
    zonasDic = [dict(zip(zonasTitDat, i)) for i in zonasDat]
    for j, i in enumerate(zonasDic):
        i['Nombre'] = zonasNames[j]
        i['tipo'] = zonasTipo[j]
    return zonasDic


def getData(file, sIndex=0, fTitulos=0, fDatos=0):
    '''
    Obtiene los datos a partir un archivo dado de excel:'loc',
    el índice de la hoja:'sIndex, la fila de los títulos: fTitulos y la fila
    donde comienzan los datos: dDatos'.
    '''
    if fDatos == 0:
        fDatos = fTitulos + 1
    wb = xlrd.open_workbook(file)  # To open Workbook
    sheet = wb.sheet_by_index(sIndex)
    dataTit = sheet.row_values(fTitulos)  # conseguir los títulos
    dataDat = [sheet.row_values(i) for i in range(sheet.nrows)[fDatos::]]  # conseguir los dats
    del wb  # cerrar el excel
    dataDat = [list(map(_mejorarDatos, i)) for i in dataDat]  # mejorar los datos
    for i in dataDat:  # remover filas vacias
        if len(i) == i.count(''):
            dataDat.remove(i)
    data = [dict(zip(dataTit, i)) for i in dataDat]  # crear lista de diccionarios
    data = np.array(data)  # transformar en array de diccionarios
    return(data)


def _mejorarDatos(datoIn):
    '''
    Optimiza los imputs mediante manipualcion de strings
    '''
    dataOut=' '.join(str(datoIn).split()) #quitar todos los espacios de más
    dataOut=dataOut.replace('**********','SinDato')
    return dataOut

def _agregarInfo(diccionario):
    '''
    Agrega info a partir de los datos del imputs mediante
    manipulación de datos.
    '''
    try:
        diccionario['CRA'] = diccionario['CRA'].split(sep='.')[0]
    except KeyError:
        pass
    try:
        diccionario['NumeroCorrelativo'] = diccionario['NumeroCorrelativo'].split(sep='.')[0]
    except KeyError:
        pass        
    try:
        diccionario['SistemaOBS'] = diccionario['Sistema'].split(sep='.')[0]
    except KeyError:
        pass
    try:        
        diccionario['Sistema'] = 'SP' + re.findall('\d?\d\d\d', diccionario['Owner'])[0]
    except KeyError:
        pass
    except IndexError:
        pass
    
#     return dataOut

def _cruceDataZonas(data, zonas={}):
    '''
    Cruza la info de data con las zonas y las completa a ambas:
    Es decir las zonas obtienen los componentes que quedan dentro
    y los componentes obtienen la zona a la que perteneces
    tipo:
        'cartesianas' hace la comparación según X, Y, Z min y max
        'cilíndricas' para x e y se hace según R y THETA. Para ello
        se transforman las coordenadas de los componentes
    '''

    X=np.array([i['LocationX'] for i in data], dtype=float)
    Y=np.array([i['LocationY'] for i in data], dtype=float)
    Z=np.array([i['LocationZ'] for i in data], dtype=float)
    R, THETA = _cartesian2polar(X, Y)
    tipo='cartesianas'

    for i in data:
        i['Zona'] = 'NA'
    for j, k in enumerate(zonas):
        if 'tipo' in k.keys():
            tipo = k['tipo']
        if tipo == 'cartesianas':
            a = ((X >= k['Xmin']) & (X < k['Xmax']) &
                              (Y >= k['Ymin']) & (Y < k['Ymax']) &
                              (Z >= k['Zmin']) & (Z < k['Zmax']))
        elif tipo == 'polares':
            a = ((R >= k['Rmin']) & (R < k['Rmax']) &
                              (ZonaClass.angulos.incluido(k['THETAmin'], k['THETAmax'], THETA)) &
                              (Z >= k['Zmin']) & (Z < k['Zmax']))
            
        b = zonas[j]['comp'] = list(np.nonzero(a)[0])
#        for m in b:
#            data[m]['Zona']=zonas[j]['Nombre']


def searchRecinto(zonasDf, string=''):
    '''
    Busca en las zonas    
    '''
    sInicial = '(?!C25-PLM-)'
    sBuscar = sInicial + string
    idx = zonasDf.index.str.contains(sBuscar, case=False, regex=True)
    cols =  ['Xmin', 'Xmax', 'Ymin', 'Ymax', 'Zmin', 'Zmax', 'Ncomp']
    return zonasDf.loc[idx, cols]



def concatenarData(dataFiles, zonasFile, sIndex=0, fTitulos=1, fDatos=2):
    '''
    Devuelve los DataFrames resultado del procesamiento de los datos
    de componentes y de las zonas.
    Params:
        dataFiles: archivo que mapea los archivos de datos
        zonasFile: archivo que define las zonas. Si no se pasa uno, se crearán las zonas
                    según una función. Puede ser en coord Cartesianas o Polares
                    Ahí aplican los params:
                        lim, size y tipo
        fTitulos y fDatos son las filas donde están los títulos y datos en los reportes
        tipo: también aplica para el cruce. Si será por coordenadas cartesianas o polares
    Devuelve tres DF:
        zonasDf: sobre las zonas
        dataDf: sobre los componentes
        solapDf: sobre el solapamiento entre zonas
    '''

    files = []
    with open(dataFiles) as f:
        for line in f:
            files.append(line.strip())

    # armar data completa a partir de todos los archivos de inputFiles
    data = np.concatenate([getData(i, sIndex, fTitulos, fDatos) for i in files], axis=0)
    

    # leer las zonas de un archivo
    zonas = getZonas(zonasFile)


    for i in data:
        _agregarInfo(i)  # mejorar la info de cada diccionario.
    _cruceDataZonas(data, zonas)  # cruzar data con zonas

    dataDf = pd.DataFrame.from_records(data)  # Arma el Df de los componentes
    zonasDf = pd.DataFrame.from_records(zonas)  # Arma el Df de las Zonas
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
    
    dataFinalDf.sort_values(by=['Sistema', 'Owner', 'Name'], inplace=True, ignore_index=True)

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
    
    
    
    
    
    
    
    
    
    
    