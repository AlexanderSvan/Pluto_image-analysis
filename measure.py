from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import (QApplication, QPushButton, QWidget, 
                               QVBoxLayout, QShortcut,QFileDialog)
import sys
import numpy as np
import imutils 
from skimage.morphology import convex_hull_image
import json
import pandas as pd

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
     
      def get_mask(points, img):
         mask=np.zeros_like(img)
         print(points)
         for point in points:
            mask[point[1],point[0]]=1
         return convex_hull_image(mask)
      
      length=self.data.image.sizes['t']
      ints={}
      for field in self.data.roi.keys():
         self.data.image.default_coords['v']=int(field.split(' ')[1])
         well_name=self.data.field_name[int(field.split(' ')[1])]

         for roi in self.data.roi[field].keys():
             ints[well_name+'_'+roi]={}
             mask=get_mask(self.data.roi[field][roi], self.data.image[0])
             for i,img in enumerate(self.data.image):
                img=imutils.resize(img, width=512, height=512)
                ints[well_name+'_'+roi][i]=np.mean(img[mask==1])
                print(roi,":",i,"/",length)

      # cb = QApplication.clipboard()
      # cb.clear(mode=cb.Clipboard )
      # cb.setText(json.dumps(ints)   , mode=cb.Clipboard)
      name = QFileDialog.getSaveFileName(self, 'Save File','',"Excel (*.xlsx)")
      df=pd.DataFrame.from_dict(ints, orient='index')
      df.to_excel(name[0])
      print('finished')

if __name__ == "__main__":
   app = QApplication(sys.argv)
   win = measure_wid()
   win.show()
   sys.exit(app.exec_())