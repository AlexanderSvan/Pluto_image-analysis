from PySide2.QtCore import QEvent, Qt
from PySide2.QtGui import QPixmap, QKeySequence
from PySide2.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QFileDialog,
                               QWidget, QVBoxLayout, QShortcut, QSlider, QComboBox)

import qimage2ndarray
import imutils
import numpy as np
import cv2
import matplotlib.pyplot as plt

class timelaps(QWidget):
       
   def __init__(self, parentData, series):
      QWidget.__init__(self)
      self.data=parentData
      self.frame=series
      self.max=np.amax([np.amax(img) for img in self.frame])
      self.min=np.amin([np.amin(img) for img in self.frame])
      self.setup_ui()
      self.shortcuts()
      # self.setFixedSize(500, 500)
      self.set_img(self.frame[0])
      self.canvas=self.frame[0]
      self.drawing=np.zeros_like(imutils.resize(self.canvas, width=500, height=500))
      self.points=[]
      self.setWindowTitle('Image window Field {}'.format(self.data.field_name[self.data.field]))
      self.data.annot_signal.connect(self.toggel_annot)
      self.data.clear_signal.connect(self.clear)
      self.data.save_signal.connect(self.save)

   def shortcuts(self):
      self.quit =QShortcut(QKeySequence("Ctrl+q"), self)
      self.quit.activated.connect(self.close)

   def setup_ui(self):
      """Initialize widgets.
      """
      layout=QVBoxLayout()
      well=QHBoxLayout()
      prev_button=QPushButton('Previous Field')
      prev_button.clicked.connect(self.prev_field)
      select=QVBoxLayout()
      self.well_LUT={value[1].split('_')[0]:value[0] for value in self.data.field_name.items() if '0000' in value[1]}
      self.idx=QComboBox()
      self.idx.addItems(list(self.well_LUT.keys()))
      self.go_btn=QPushButton('Go to well')
      self.go_btn.clicked.connect(self.go_to_well)
      select.addWidget(self.idx)
      select.addWidget(self.go_btn)      
      next_button=QPushButton('Next Field')
      next_button.clicked.connect(self.next_field)
      well.addWidget(prev_button)
      well.addLayout(select)
      well.addWidget(next_button)
      
      self.image_label = QLabel(self)
      self.image_label.installEventFilter(self)
      controls=QHBoxLayout()
      self.slider = QSlider()
      self.slider.setOrientation(Qt.Horizontal)
      self.slider.setTickPosition(QSlider.TicksBelow)
      self.slider.setTickInterval(10)
      self.slider.setMinimum(0)
      self.slider.setMaximum(self.frame.sizes['t']-1)
      self.slider.valueChanged.connect(self.changedValue) 
      controls.addWidget(self.slider)
      layout.addLayout(well)
      layout.addWidget(self.image_label)
      layout.addLayout(controls)
      self.setLayout(layout)
  
   def set_img(self, frame):
    
      def normalize(f):
         lmin = float(self.min)
         lmax = float(self.max)
         return np.floor((f-lmin)/(lmax-lmin)*255.)
      
      if self.data.show_annot ==True:
         self.canvas=normalize(imutils.resize(self.canvas, width=500, height=500))
         self.drawing=normalize(imutils.resize(self.drawing, width=500, height=500))
         # if len(self.points)>1:
         #     x1,y1=self.points[-2]
         #     x,y=self.points[-1]
         #     cv2.line(self.canvas, (x1,y1),(x,y),color=(255,255,255),thickness=5)
         
         
         for stroke in self.points:
            prev=[]
            # for coords in stroke:
            #    if prev!=[]:
            #       x1,y1=prev
            #       x,y=coords
            #       cv2.line(self.canvas, (x1,y1),(x,y),color=(255,255,255),thickness=5)
            #       cv2.line(self.drawing, (x1,y1),(x,y),color=(255,255,255),thickness=5)
            #    else:
            #       pass
            #    prev=coords
               
            
            for coords in self.points:
                x,y=coords
                cv2.circle(self.canvas, (int(x), int(y)), int(10), (255, 255, 255), 2)
                cv2.drawMarker(self.canvas,  (int(x), int(y)), (255,255,255), markerType=cv2.MARKER_CROSS, markerSize=30, thickness=2)
         image = qimage2ndarray.array2qimage(self.canvas)
         self.image_label.setPixmap(QPixmap.fromImage(image))

      else:
         frame=normalize(imutils.resize(frame, width=500, height=500))
         image = qimage2ndarray.array2qimage(frame)
         self.image_label.setPixmap(QPixmap.fromImage(image))
         
  
   def changedValue(self):
      self.canvas=self.data.image[self.slider.value()]
      self.set_img(self.frame[self.slider.value()])
  
   def eventFilter(self, obj, event):
             
      if self.data.pointer=='mouse':
         if obj is self.image_label and event.type() == QEvent.MouseButtonPress:
            self.points=[]

      elif self.data.pointer=='cross':
         if obj is self.image_label and event.type() == QEvent.MouseButtonPress:
            self.points.append((event.pos().x(),event.pos().y()))
            print(str((event.pos().x(),event.pos().y())))
            if self.data.show_annot:
               self.set_img(self.frame[self.slider.value()])
   
      elif self.data.pointer=='brush' and event.type() == QEvent.MouseMove:
         if obj is self.image_label:
            self.points[-1].append((event.pos().x(),event.pos().y()))
            if self.data.show_annot:
               self.set_img(self.frame[self.slider.value()])
      
      # elif self.data.pointer=='brush' and event.type() == QEvent.MouseButtonRelease:         
      #    if obj is self.image_label:
      #       if self.stroke:
      #          self.points.append(self.stroke)
      #          self.stroke=None
      #          print('test')

      elif self.data.pointer=='brush' and event.type() == QEvent.MouseButtonPress:         
         if obj is self.image_label:
            self.points.append([])
            
   """
   currently the drawing function dows not draw from the 
   """
           
   def save_roi(self,name):
      field='field {}'.format(self.data.field)
      if field in self.data.roi:
         self.data.roi[field][name]=self.drawing
         self.clear()
      else:
         self.data.roi[field]={}
         self.data.roi[field][name]=self.drawing
         self.clear()
   
   def toggel_annot(self):
      self.set_img(self.frame[self.slider.value()])
      
   def clear(self):
      self.canvas=self.frame[self.slider.value()]
      self.drawing=np.zeros_like(self.frame[self.slider.value()])
      self.points=[]
      self.set_img(self.frame[self.slider.value()])
      
   def next_field(self):
      if self.data.field+1 < self.data.image.sizes['v']:
         self.data.field=self.data.field+1
         self.data.image.default_coords['v']=self.data.field
         self.frame=self.data.image
         self.canvas=self.data.image[self.slider.value()]
         self.set_img(self.frame[self.slider.value()])
         self.setWindowTitle('Image window Field {}'.format(self.data.field_name[self.data.field]))
      
   def prev_field(self):
      if self.data.field-1 >=0:
         self.data.field=self.data.field-1
         self.data.image.default_coords['v']=self.data.field
         self.frame=self.data.image
         self.canvas=self.data.image[self.slider.value()]
         self.set_img(self.frame[self.slider.value()])
         self.setWindowTitle('Image window Field {}'.format(self.data.field_name[self.data.field]))
         
   def go_to_well(self):
         self.data.field=self.well_LUT[self.idx.currentText()]
         self.data.image.default_coords['v']=self.data.field
         self.frame=self.data.image
         self.canvas=self.data.image[self.slider.value()]
         self.set_img(self.frame[self.slider.value()])
         self.setWindowTitle('Image window Field {}'.format(self.data.field_name[self.data.field]))
         
   def save(self):
       path, ext = QFileDialog.getSaveFileName(self, 'Save File',filter="JPEG (*.jpg);;TIFF (*.tif);;PNG (*.png)")
       ext=ext[ext.find("(")+1:ext.find(")")].strip("*")
       if not path[-len(ext):]==ext:
          path=path+ext
       plt.imsave(path, self.frame[self.slider.value()], cmap='gray')
   