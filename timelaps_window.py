from PySide2.QtCore import QEvent, Qt
from PySide2.QtGui import QPixmap, QKeySequence
from PySide2.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QFileDialog,
                               QWidget, QVBoxLayout, QShortcut, QSlider, QComboBox)

from qimage2ndarray import array2qimage
import imutils
import numpy as np
import cv2
# import matplotlib.pyplot as plt

class timelaps(QWidget):
       
   def __init__(self, parentData, series):
      QWidget.__init__(self)
      self.data=parentData
      self.max=np.amax([np.amax(img) for img in self.data.image])
      self.min=np.amin([np.amin(img) for img in self.data.image])
      self.setup_ui()
      self.shortcuts()
      self.points=[]
      # self.setFixedSize(500, 500)
      self.set_img(self.data.image[0])
      self.canvas=self.data.image[0]
      self.drawing=np.zeros_like(imutils.resize(self.canvas, width=512, height=512))

      self.setWindowTitle('Image window Field {}'.format(self.data.field_name[self.data.field]))
      self.data.annot_signal.connect(self.toggel_annot)
      self.data.clear_signal.connect(self.clear)
      self.data.save_signal.connect(self.save)

   def shortcuts(self):
      self.quit =QShortcut(QKeySequence("Ctrl+q"), self)
      self.quit.activated.connect(self.close)

   def setup_ui(self):
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
      self.slider.setMaximum(self.data.image.sizes['t']-1)
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
          self.canvas=normalize(imutils.resize(frame, width=512, height=512))
          for coords in self.points:
             x,y=coords
             # cv2.circle(self.canvas, (int(x), int(y)), int(10), (255, 255, 255), 2)
             cv2.drawMarker(self.canvas,  (int(x), int(y)), (255,255,255), markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2)
          
          self.image_label.setPixmap(QPixmap.fromImage(array2qimage(self.canvas)))
      
      else:
          frame=normalize(imutils.resize(frame, width=512, height=512))
          self.image_label.setPixmap(QPixmap.fromImage(array2qimage(frame)))
         
  
   def eventFilter(self, obj, event):
             
      if self.data.pointer=='mouse':
         if obj is self.image_label and event.type() == QEvent.MouseButtonPress:
            self.points=[]

      elif self.data.pointer=='cross':
         if obj is self.image_label and event.type() == QEvent.MouseButtonPress:
            self.points.append((event.pos().x(),event.pos().y()))
            print(str((event.pos().x(),event.pos().y())))
            print(self.points)
            if self.data.show_annot:
               self.set_img(self.data.image[self.slider.value()])
   
      elif self.data.pointer=='brush' and event.type() == QEvent.MouseMove:
         if obj is self.image_label:
            self.points.append((event.pos().x(),event.pos().y()))
            if self.data.show_annot:
               self.set_img(self.data.image[self.slider.value()])

      elif self.data.pointer=='brush' and event.type() == QEvent.MouseButtonPress:         
         if obj is self.image_label:
            self.points.append([])
           
   def save_roi(self,name):
      field='field {}'.format(self.data.field)
      if field in self.data.roi:
         self.data.roi[field][name]=self.points
         self.clear()
      else:
         self.data.roi[field]={}
         self.data.roi[field][name]=self.points
         self.clear()
   
   def toggel_annot(self):
      self.set_img(self.data.image[self.slider.value()])
      
   def clear(self):
      self.canvas=self.data.image[self.slider.value()]
      self.drawing=np.zeros_like(self.data.image[self.slider.value()])
      self.points=[]
      self.set_img(self.data.image[self.slider.value()])
      
   def changedValue(self):
      # self.canvas=self.data.image[self.slider.value()]
      self.set_img(self.data.image[self.slider.value()])
      
   def next_field(self):
      if self.data.field+1 < self.data.image.sizes['v']:
         self.data.field=self.data.field+1
         self.data.image.default_coords['v']=self.data.field
         self.max=np.amax([np.amax(img) for img in self.data.image])
         self.min=np.amin([np.amin(img) for img in self.data.image])
         self.canvas=self.data.image[self.slider.value()]
         self.set_img(self.data.image[self.slider.value()])
         self.setWindowTitle('Image window Field {}'.format(self.data.field_name[self.data.field]))
      
   def prev_field(self):
      if self.data.field-1 >=0:
         self.data.field=self.data.field-1
         self.data.image.default_coords['v']=self.data.field
         self.max=np.amax([np.amax(img) for img in self.data.image])
         self.min=np.amin([np.amin(img) for img in self.data.image])
         self.canvas=self.data.image[self.slider.value()]
         self.set_img(self.data.image[self.slider.value()])
         self.setWindowTitle('Image window Field {}'.format(self.data.field_name[self.data.field]))
         
   def go_to_well(self):
         self.data.field=self.well_LUT[self.idx.currentText()]
         self.data.image.default_coords['v']=self.data.field
         self.max=np.amax([np.amax(img) for img in self.data.image])
         self.min=np.amin([np.amin(img) for img in self.data.image])
         self.canvas=self.data.image[self.slider.value()]
         self.set_img(self.data.image[self.slider.value()])
         self.setWindowTitle('Image window Field {}'.format(self.data.field_name[self.data.field]))
         
   def save(self):
         pass
        # path, ext = QFileDialog.getSaveFileName(self, 'Save File',filter="JPEG (*.jpg);;TIFF (*.tif);;PNG (*.png)")
        # ext=ext[ext.find("(")+1:ext.find(")")].strip("*")
        # if not path[-len(ext):]==ext:
        #    path=path+ext
        # plt.imsave(path, self.data.image[self.slider.value()], cmap='gray')
   