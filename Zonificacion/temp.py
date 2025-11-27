# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import ZonaClass as Z
import matplotlib.pyplot as plt



llavesCart = ['Nombre', 'tipo', 'Xmin', 'Xmax', 'Ymin', 'Ymax', 'Zmin', 'Zmax', 'comp']
llavesPol = ['Nombre', 'tipo', 'Rmin', 'Rmax', 'Thetamin', 'Thetamax','Zmin', 'Zmax',  'comp']
valoresCart = ['ZonaCart', 'cartesianas', 0, 1000, 0, 1000, 0, 1000, [1,2,3]]
valoresPol = ['ZonaPol', 'polares', 0, 1000, 0, 200, 0, 1000, [4,5,6]]
        
dC = Z.zona(**dict(zip(llavesCart, valoresCart)))
dP = Z.zona(**dict(zip(llavesPol, valoresPol)))
        
        
kk = Z.zona()
    

ff = {i: {j: i*j for j in range(5)} for i in range(5)}
df = pd.DataFrame(ff)
ix = pd.Index([(i[0], i[1]) for i in df.index if i[0] != i[1]])
df2 = pd.DataFrame(df.loc[ix])


X = dataDf['LocationX']
Y = dataDf['LocationY']
Z = dataDf['LocationZ']

plt.scatter(X,Y)
plt.show()


zonasDf['OBJ'] = [ZonaClass.zona(**dict(zip(zonasDf.columns, zonasDf.loc[i, :]))) for i in zonasDf.index]

a=dict(zip(zonasDf.columns, zonasDf.iloc[0, :]))

zonasDf.iloc[0, :]


for i in zonasDf.index:
    