#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 13:53:40 2020

@author: lcadmin
"""
import imutils
import numpy as np
import pandas as pd



def normalize(f):
         lmin = float(f.min())
         lmax = float(f.max())
         return np.floor((f-lmin)/(lmax-lmin)*255.)

def intensity_timeline(imgset, roiset):
   length=imgset.sizes['t']
   ints={}
   for field, subdict in roiset.items():
       ints[field]={}
       imgset.default_coords['v']=int(field.split(' ')[-1])
       print(field)
       for roi, item in subdict.items():
         if roi != 'Background':   
            ints[field][roi]={}
            for i,img in enumerate(imgset):
               img=normalize(imutils.resize(img, width=500, height=500))
               # ints[field][roi][i]=np.mean(img[roiset[field][roi]==255])-np.mean(img[roiset[field]['Background']==255])
               ints[field][roi][i]=np.mean(img[roiset[field][roi]==255])
               print(field+" :"+str(i)+"/"+str(length))           
   print('finished') 
   

   
   return ints
           