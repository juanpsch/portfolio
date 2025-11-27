# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:20:12 2020

@author: juanp_schamun
"""

import numpy as np
import pandas as pd
from math import radians


class zona:
    '''
    Define la clase Zona
    '''
    def __init__(self, **kwargs):
        
        self.Nombre = 'SN'
        self.tipo = 'cartesianas'
        self.Xmin = 0
        self.Xmax = 0
        self.Ymin = 0
        self.Ymax = 0
        self.Zmin = 0
        self.Zmax = 0        
        self.Rmin = 0
        self.Rmax = 0
        self.THETAmin = 0
        self.THETAmax = 0
        self.comp=[]

        if 'Nombre' in kwargs:
            self.Nombre = kwargs['Nombre']
        if 'tipo' in kwargs:
            self.tipo = kwargs['tipo']
        if 'Xmin' in kwargs:
            self.Xmin = kwargs['Xmin']
        if 'Xmax' in kwargs:
            self.Xmax = kwargs['Xmax']
        if 'Ymin' in kwargs:
            self.Ymin = kwargs['Ymin']
        if 'Ymax' in kwargs:
            self.Ymax = kwargs['Ymax']
        if 'Zmin' in kwargs:
            self.Zmin = kwargs['Zmin']
        if 'Zmax' in kwargs:
            self.Zmax = kwargs['Zmax']
        if 'Rmin' in kwargs:
            self.Rmin = kwargs['Rmin']
        if 'Rmax' in kwargs:
            self.Rmax = kwargs['Rmax']
        if 'THETAmin' in kwargs:
            self.THETAmin = kwargs['THETAmin']
        if 'THETAmax' in kwargs:
            self.THETAmax = kwargs['THETAmax']
        if 'comp' in kwargs:
            self.comp = pd.Index(kwargs['comp'])
        
        self.THETAmin, self.THETAmax = angulos.convertir(self.THETAmin, self.THETAmax)

        if self.tipo not in ['cartesianas', 'polares']: 
            raise ValueError
                
        self.Ncomp = len(self.comp)
        self.ah = self._areaHorizontal()
        self.vol = self._volumen()
        
        
        
    

    def getAtt(self, todos=False):
        '''Devuelve un Dict con todos los atributos necesarios
        para inicializar una zona. Si se usa la opción todos = True
        Entonces el diccionario tendrá todos los atributos de la zona
        '''
        
        attDict = dict(self.__dict__)
        extras = ['ah','vol','comp']
        
        if self.tipo == 'polares':
            extras2 = ['Xmin', 'Xmax', 'Ymin', 'Ymax']
        elif self.tipo == 'cartesianas':
            extras2 = ['Rmin', 'Rmax', 'THETAmin', 'THETAmax']
       
        if not todos:            
            for i in (extras + extras2):
                attDict.pop(i, '_')
                
        return attDict

    def __str__(self):
        
        string = str(self.getAtt(todos=False))
        
        return string

    def getCoords(self, tipo=None):
        
        if tipo == None: tipo = self.tipo
        
        if tipo == 'cartesianas':
            coords = np.array([self.Xmin, self.Xmax, self.Ymin, self.Ymax,
                               self.Zmin, self.Zmax])
        elif tipo == 'polares':
            coords = np.array([self.Rmin, self.Rmax, self.THETAmin, self.THETAmax,
                               self.Zmin, self.Zmax])
        return coords

    def _areaHorizontal(self):
        '''Devuelve la superficie horizontal de la zona en m2'''
        if self.tipo == 'cartesianas':
            area = abs((self.Xmin-self.Xmax)*(self.Ymin-self.Ymax))/1e6
        elif self.tipo == 'polares':
            area = (radians(self.THETAmax)-radians(self.THETAmin))*(self.Rmax**2-self.Rmin**2)/2/1e6
        
        return area

    def _volumen(self):
        '''Devuelve el volumen de la zona en m3'''
        return abs(self.ah *(self.Zmin - self.Zmax)) / 1e3

    def incluida(self, other):
        '''
        Devuelve True si la zona self está completamente incluída en
        la zona other con lógica >=
        '''
        return self.solap(other).vol == self.vol

    def _solapComp(self, other):
        '''
        Realiza la intersección de componentes entre
        la zona self y la zona other
        '''
        inx1 = pd.Index(self.comp)
        inx2 = pd.Index(other.comp)
        inter = inx1.intersection(inx2)

        return inter

    def solap(self, other):
        '''
        Devuelve un objeto zona resultado de la
        intersección entre la
        zona self y la zona other
        '''
        if (self is None) | (other is None):
            return None
        if (self.vol == 0) | (other.vol == 0):
            return None        
        
        if self.tipo == other.tipo:             
            tipo = self.tipo
        else: tipo = 'cartesianas'
        
        bound1 = self.getCoords(tipo=tipo)
        bound2 = other.getCoords(tipo=tipo)

        mins = np.maximum(bound1[::2], bound2[::2])
        maxs = np.minimum(bound1[1::2], bound2[1::2])
        diff = maxs - mins
        if np.any(diff <= 0):
            return None
        iCoords = [[mins[i], maxs[i]] for i in range(len(mins))]
        iCoords = np.array(iCoords).ravel()  # coordenadas de la intersección
        iName = self.Nombre + '_&_' + other.Nombre
        k = ['tipo', 'Nombre']            
        if tipo =='polares':
            k += ['Rmin', 'Rmax', 'THETAmin', 'THETAmax', 'Zmin', 'Zmax']
        else:
            k += ['Xmin', 'Xmax', 'Ymin', 'Ymax', 'Zmin', 'Zmax']
        v = [tipo, iName] + list(iCoords)
        iZone = zona(**dict(zip(k,v)))
        iZone.comp = self._solapComp(other)
        iZone.Ncomp = len(iZone.comp)

        return iZone
#        return p1, p2

    def sumarZonas(self, other):
        '''
        Devuelve una zona cuyos límites min y max representan
        el bounding box total de las dos zonas (puede exceder
        por mucho ambas zonas), pero el volumen
        es la Union del volumen de las zonas y los componentes
        que contiene son la union de los componentes de ambas.
        '''
        if self is None:
            return other
        if other is None:
            return self
        
        iZone = self.solap(other)
       
        if self.tipo == other.tipo:             
            tipo = self.tipo
        else: tipo = 'cartesianas' 
       
        bound1 = self.getCoords(tipo=tipo)
        bound2 = other.getCoords(tipo=tipo)
        
        mins = np.minimum(bound1[::2], bound2[::2])
        maxs = np.maximum(bound1[1::2], bound2[1::2])
        sCoords = [[mins[i], maxs[i]] for i in range(len(mins))]
        sCoords = np.array(sCoords).ravel()  # coordenadas de la suma
        sName = self.Nombre + '_+_' + other.Nombre        
        k = ['tipo', 'Nombre']            
        if tipo =='polares':
            k += ['Rmin', 'Rmax', 'THETAmin', 'THETAmax', 'Zmin', 'Zmax']
        else:
            k += ['Xmin', 'Xmax', 'Ymin', 'Ymax', 'Zmin', 'Zmax']
        v = [tipo, sName] + list(sCoords)
        sZone = zona(**dict(zip(k,v)))
        ivol = 0 if iZone is None else iZone.vol
        iah = 0 if iZone is None else iZone.ah
        sZone.vol = self.vol + other.vol - ivol
        sZone.ah = self.ah + other.ah - iah
        sZone.comp = pd.Index(set(self.comp.to_list()).union(
                              set(other.comp.to_list())))
        sZone.Ncomp = len(sZone.comp)

        return sZone

    def restarZonas(self, other):
        '''
        Devuelve una zona cuyos límites son los mismos zona self
        El volumen es igual al volumen
        de self restando el volumen del solap.self(other).
        Los componentes son los de self quitando los
        de self.solap(other).
        '''
        iZone = self.solap(other)

        if (iZone is None):
            return self
        if (iZone.vol == 0):
            return self        
        if self.tipo == other.tipo:             
            tipo = self.tipo
        else: tipo = 'cartesianas'
        bound1 = self.getCoords(tipo=tipo)
        rCoords = bound1
        rName = self.Nombre + '_-_' + other.Nombre
        k = ['tipo', 'Nombre']
        if tipo =='polares':
            k += ['Rmin', 'Rmax', 'THETAmin', 'THETAmax', 'Zmin', 'Zmax']
        else:
            k += ['Xmin', 'Xmax', 'Ymin', 'Ymax', 'Zmin', 'Zmax']
        v = [tipo, rName] + list(rCoords)
        rZone = zona(**dict(zip(k,v)))
        rZone.vol = self.vol - iZone.vol
        rZone.ah = self.ah - iZone.ah
        rZone.comp = pd.Index(set(self.comp.to_list()) -
                              set(other.comp.to_list()))
        rZone.Ncomp = len(rZone.comp)

        return rZone

    def __add__(self, other):
        return self.sumarZonas(other)

    def __sub__(self, other):
        return self.restarZonas(other)



class angulos():
    
    def __init__(self, a, b):
        
        self.a, self.b = self.convertir(a, b)
        
    @staticmethod
    def convertir(a, b):
        
        # para el caso justo del círculo completo denotado con a=0 y b=360
        # No serán considerados otros casos de círculo completo ej: a=-180 b=180
        # En ese caso se considerará arco nulo
        if (a == 0) & (b == 360):
            return a, b
        
        a1 = a % 360
        b1 = b % 360
        
        if a1 > b1:
            a1 = a1 % -360
            
        return a1, b1
              

    def __str__(self):
        
        string = '{}, {}'.format(self.a, self.b)
        return string
        
    def dentro(self, c):
        
        result = False
        
        c1 = c % 360
        c2 = c % -360        

        result = (((c1 >= self.a)  & (c1 <= self.b)) | ((c2 >= self.a)  & (c2 <= self.b)))   
            
        return result
    
    @staticmethod
    def incluido(a, b, c):
        
        arco = angulos(a, b)
        return arco.dentro(c)
         
    
        

