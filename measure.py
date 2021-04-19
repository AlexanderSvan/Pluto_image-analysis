from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import (QApplication, QPushButton, QWidget, 
                               QVBoxLayout, QShortcut)
import sys
import numpy as np
import imutils 

class measure_wid(QWidget):
 
   def __init__(self, parentData=None):
      QWidget.__init__(self)
      self.data=parentData
      self.setup_ui()
      self.shortcuts()
      self.setWindowTitle('Measure')
      
   def shortcuts(self):
      self.quit =QShortcut(QKeySequence("Ctrl+q"), self)
      self.quit.activated.connect(self.close)
      
   def setup_ui(self):
      """Initialize widgets.
      """
      layout=QVBoxLayout()
      measure_button=QPushButton('Measure')
      measure_button.clicked.connect(self.analyse)
      layout.addWidget(measure_button)
      self.setLayout(layout)
      
   def analyse(self):
      def normalize(f):
         lmin = float(f.min())
         lmax = float(f.max())
         return np.floor((f-lmin)/(lmax-lmin)*255.)
      
      length=self.data.image.sizes['t']
      ints={}
      for field in self.data.roi.keys():
          
         ints[field]={}
         for roi in self.data.roi[field].keys():
             ints[field][roi]={}
             for i,img in enumerate(self.data.image):
                img=normalize(imutils.resize(img, width=500, height=500))
                ints[field][roi][i]=np.mean(img[self.data.roi[field][roi]==255])
                print(roi,":",i,"/",length)
      self.data.results=ints
      print(ints)
      print(self.data.roi)
      print('finished')

if __name__ == "__main__":
   app = QApplication(sys.argv)
   win = measure_wid()
   win.show()
   sys.exit(app.exec_())