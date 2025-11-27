# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:20:12 2020

@author: juanp_schamun
"""


import argparse
from Zonificacion_Numpy import concatenarData
import pandas as pd


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--datafiles=', action='store',
                        dest='inputFiles', type=str, default='InputFiles.dat',
                        help='input Data Files (Componentes) default = InputFiles_FDC.dat')
    parser.add_argument('-zf', '--zonasfiles=', action='store',
                        dest='fileZonas', type=str,
                        default='RecintosDB.dat',
                        help='input File (Zonas) default = RecintosDB.dat')
    parser.add_argument('-o', '--outfile=', action='store',
                        dest='out', type=str,
                        default=None,
                        help='Nombre archivo de salida default = None')
    result = parser.parse_args()

    inputFiles = result.inputFiles  # archivo de punteros a arhcivos con datos
#    inputFiles = 'InputFilesReducido.dat'
    fileZonas = result.fileZonas  # archivo de punteros a arhcivos con datos de zonas
#    fileZonas = 'RecintosDB.dat'
    out = result.out  # archivo donde se escriben los datos

    dataDf, zonasDf, solapDf, dataFinalDf = concatenarData(inputFiles, fileZonas)
    
    if out != None:
        writer = pd.ExcelWriter(out, engine='xlsxwriter')
        dataFinalDf.to_excel(writer, sheet_name='Comp')
        zonasDf.drop(columns=['comp','OBJ']).to_excel(writer, sheet_name='Zonas')
        writer.save()
    

    return dataDf, zonasDf, solapDf, dataFinalDf


if __name__ == '__main__':
    dataDf, zonasDf, solapDf, dataFinalDf = main()


# =============================================================================
# run ZonifMain.py -d InputFiles_DDC.dat -zf RecintosDB_DDC.dat -o ComponentesDDC.xlsx
# run ZonifMain.py -d InputFiles_FDC.dat -zf RecintosDB_FDC.dat -o ComponentesFDC.xlsx
# =============================================================================
