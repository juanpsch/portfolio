# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:20:12 2020

@author: juanp_schamun
"""


import argparse
import Zonificacion_Numpy as zonif
import pandas as pd


import Zonificacion_Numpy as ZN
import Zonificacion_pandas as ZP


inputFiles = 'InputFiles_DDC.dat'
fileZonas = 'RecintosDB_DDC.dat'
    

# a = zonif.getZonas(fileZonas)
# b = zonif.armarZonas(9500, 10, 'polares')

dataDf_N, zonasDf_N, solapDf_N, dataFinalDf_N = ZN.concatenarData(inputFiles,zonasFile=fileZonas)

dataDf_P, zonasDf_P, solapDf_P, dataFinalDf_P = ZP.concatenarData(inputFiles,zonasFile=fileZonas)


# dataDf, zonasDf, solapDf, dataFinalDf = ZP.concatenarData(inputFiles,zonasFile=fileZonas)




