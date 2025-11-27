# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 20:39:39 2020

@author: juanp_schamun
"""

class employee:
    
    nInst = 0
    
    def __new__(cls):
        cls.nInst += 1
        print ("En total hay {} Instancias de la clase employee"
               .format(cls.nInst))
        inst = object.__new__(cls)
        return inst
    def __init__(self):
        print ("__init__ magic method is called")
        self.name='Satya'
        
class distance:
    def __init__(self, x=None,y=None):
        self.ft=x
        self.inch=y        
        
    def __add__(self,x):
        temp=distance()
        temp.ft=self.ft+x.ft
        temp.inch=self.inch+x.inch
        if temp.inch>=12:
            temp.ft+=1
            temp.inch-=12
        return temp
    
    def __str__(self):
        return 'ft:'+str(self.ft)+' in: '+str(self.inch)