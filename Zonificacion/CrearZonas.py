# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 00:17:00 2020

@author: juanp_schamun
"""


import Zonificacion_Numpy as zonif
import pandas as pd

zonasCart = zonif.armarZonas(-40000, 10, 'cartesianas')
zonasPol = zonif.armarZonas(9500, 10, 'polares')

zonas = zonasCart #+ zonasPol

zonasDfExp = pd.DataFrame(zonas)

cols = ['Nombre', 'tipo', 'Xmin', 'Xmax', 'Ymin', 'Ymax', 'Zmin', 'Zmax'] #, 'Rmin', 'Rmax', 'THETAmin', 'THETAmax']

zonasDfExp = zonasDfExp[cols]


zonasDfExp.to_csv('zonasTest.dat', sep='\t',index=False, na_rep=0)

