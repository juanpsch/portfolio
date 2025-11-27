# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:20:12 2020

@author: juanp_schamun
"""

import numpy as np
import pandas as pd


class zona:
    '''
    Define la clase Zona
    '''
    def __init__(self, Nombre='SN', Xmin=0, Xmax=0,
                 Ymin=0, Ymax=0, Zmin=0, Zmax=0, comp=[]):
        self.Nombre = Nombre
        self.Xmin = Xmin
        self.Xmax = Xmax
        self.Ymin = Ymin
        self.Ymax = Ymax
        self.Zmin = Zmin
        self.Zmax = Zmax
        self.comp = pd.Index(comp)
        self.Ncomp = len(self.comp)
        self.ah = self._areaHorizontal()
        self.vol = self._volumen()

    def getAtt(self, todos=False):
        '''Devuelve un Dict con todos los atributos necesarios
        para inicializar una zona. Si se usa la opción todos = True
        Entonces el diccionario tendrá todos los atributos de la zona
        '''
        attDict = {
            'Nombre': self.Nombre,
            'Xmin': self.Xmin,
            'Xmax': self.Xmax,
            'Ymin': self.Ymin,
            'Ymax': self.Ymax,
            'Zmin': self.Zmin,
            'Zmax': self.Zmax,
            'comp': self.comp,
         }
   
        if todos:
            attDict['ah'] = self.ah
            attDict['vol'] = self.vol
            attDict['Ncomp'] = self.Ncomp

        return attDict

    def __str__(self):
        string = '''
  Nombre = {}
  Xmin = {}
  Xmax = {}
  Ymin = {}
  Ymax = {}
  Zmin = {}
  Zmax = {}
  Area Horizontal(m2) = {}
  Volumen(m3) = {}
  Cantidad de Componentes = {}'''.format(self.Nombre, self.Xmin,
                                         self.Xmax, self.Ymin,
                                         self.Ymax, self.Zmin,
                                         self.Zmax, self.ah, self.vol,
                                         self.Ncomp)
        return string

    def getCoords(self):
        coords = np.array([self.Xmin, self.Xmax, self.Ymin, self.Ymax,
                           self.Zmin, self.Zmax])
        return coords

    def _areaHorizontal(self):
        '''Devuelve la superficie horizontal de la zona en m2'''
        return abs((self.Xmin-self.Xmax)*(self.Ymin-self.Ymax))/1e6

    def _volumen(self):
        '''Devuelve el volumen de la zona en m3'''
        return abs((self.Xmin - self.Xmax)*(self.Ymin - self.Ymax) *
                   (self.Zmin - self.Zmax)) / 1e9

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
        bound1 = self.getCoords()
        bound2 = other.getCoords()

        mins = np.maximum(bound1[::2], bound2[::2])
        maxs = np.minimum(bound1[1::2], bound2[1::2])
        diff = maxs - mins
        if np.any(diff <= 0):
            return None
        iCoords = [[mins[i], maxs[i]] for i in range(len(mins))]
        iCoords = np.array(iCoords).ravel()  # coordenadas de la intersección
        iName = self.Nombre + '_&_' + other.Nombre
        iZone = zona(iName, *iCoords)
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
       
        bound1 = self.getCoords()
        bound2 = other.getCoords()
        
        mins = np.minimum(bound1[::2], bound2[::2])
        maxs = np.maximum(bound1[1::2], bound2[1::2])
        sCoords = [[mins[i], maxs[i]] for i in range(len(mins))]
        sCoords = np.array(sCoords).ravel()  # coordenadas de la suma
        sName = self.Nombre + '_+_' + other.Nombre
        sZone = zona(sName, *sCoords)
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
        bound1 = self.getCoords()
        rCoords = bound1
        rName = self.Nombre + '_-_' + other.Nombre
        rZone = zona(rName, *rCoords)
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
