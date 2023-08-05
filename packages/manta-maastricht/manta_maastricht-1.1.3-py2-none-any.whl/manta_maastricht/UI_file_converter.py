# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 17:09:20 2018

@author: Lian
"""
from PyQt5 import uic

fin = open('AADEvaluator.ui','r')
fout = open('AADEvaluatorUI.py','w')
uic.compileUi(fin,fout,execute=True)
fin.close()
fout.close()

