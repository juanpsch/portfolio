# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 09:45:14 2020

@author: juanp_schamun
"""

import xlrd
import pandas as pd

path="D:\\Users\\juanp_schamun\\Documents\\Reportes\\DistribucionEspacial\\Pesos\\"
nombre='Pipe.xlsx'
file=path + nombre

hoja1='Pipe - Carbon Steel'
hoja2='Pipe - Stainless Steel'

columnas=['NS', 'WeightKg', 'Schedule']

df1 = pd.read_excel(file, sheet_name=hoja1, skiprows=4,
                   header=0)

df1=df1[columnas]
df1['Material'] = 'CS'


df2 = pd.read_excel(file, sheet_name=hoja2, skiprows=4,
                   header=0)

df2=df2[columnas]
df2['Material'] = 'SS'

pesosDf=df1.append(df2)
pesosDf['PartName']='Tuberia'

pesosDf.to_csv('Pesos.dat',sep='|',index=False)
