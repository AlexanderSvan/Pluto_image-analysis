from PySide2.QtCore import QSize, QEvent, Qt, Signal, Slot
from PySide2.QtGui import QPixmap, QKeySequence
from PySide2.QtWidgets import (QAction, QApplication, QHeaderView, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QPushButton, QTableWidget, QTableWidgetItem,QCheckBox,
                               QVBoxLayout, QHBoxLayout, QWidget, QVBoxLayout, QInputDialog, QSlider, QShortcut,
                               QLineEdit, QMessageBox, QDialog, QFormLayout, QFileDialog, QComboBox)
import sys
import imutils
import numpy as np
# from calculations import intensity_timeline

class int_tracker(QWidget):
   
   add_roi = Signal(str)
 
   def __init__(self, parentData=None):
      QWidget.__init__(self)
      self.data=parentData
      self.setup_ui()
      self.shortcuts()
      # self.setFixedSize(200, 150)
      self.setWindowTitle('Intensity Tracker')
      
   def shortcuts(self):
      self.quit =QShortcut(QKeySequence("Ctrl+q"), self)
      self.quit.activated.connect(self.close)
      
   def setup_ui(self):
      roi=QWidget()
      layout=QHBoxLayout()
      roi_layout=QVBoxLayout()
      buttons=QHBoxLayout()
      
      add_button=QPushButton('add')
      add_button.clicked.connect(self.init_add)
      
      rem_button=QPushButton('remove')
      
      self.roi_type=QComboBox()
      self.roi_type.addItem('RoI')
      self.roi_type.addItem('Background')
      self.roi_type.setFixedWidth(100)
      
      buttons.addWidget(add_button)
      buttons.addWidget(rem_button)
      
      self.table=QTableWidget()
      self.table.setRowCount(0)
      self.table.setColumnCount(1)
      self.table.setHorizontalHeaderLabels(['RoIs'])
      self.table.horizontalHeader().setSectionResizeMode(0,QHeaderView.Stretch)
      
      box=QCheckBox("Show RoIs")
      
      roi_layout.addLayout(buttons)
      roi_layout.addWidget(self.roi_type, alignment=Qt.AlignCenter)
      roi_layout.addWidget(self.table)
      roi_layout.addWidget(box)
      roi.setLayout(roi_layout)
      roi.setFixedSize(150, 250)
      layout.addWidget(roi)
      
      
      measure_wid=QWidget()
      right=QVBoxLayout()
      measure_button=QPushButton('Measure')
      measure_button.clicked.connect(self.analyse)
      measure_button.setFixedSize(60,25)
      
      graph=QLabel('graph')
      graph.setFixedSize(200,200)

      
      right.addWidget(measure_button,alignment=Qt.AlignCenter)
      right.addWidget(graph,alignment=Qt.AlignCenter)
      measure_wid.setLayout(right)
      layout.addWidget(measure_wid)
      self.setLayout(layout)
      

   def init_add(self):
      if self.roi_type.currentText() =='Background':
         label='Background'
      else:
         label="{} {}".format(self.roi_type.currentText(),self.table.rowCount())
      self.add_roi.emit(label)
      print(self.roi_type.currentText())

   def add_row(self):
      rowPosition = self.table.rowCount()
      self.table.insertRow(rowPosition)
      if self.roi_type.currentText() =='Background':
         label='Background'
      else:
         label="{} {}".format(self.roi_type.currentText(),rowPosition)
      self.table.setItem(rowPosition , 0, QTableWidgetItem(label))
      
   # def analyse(self):
   #    def normalize(f):
   #       lmin = float(f.min())
   #       lmax = float(f.max())
   #       return np.floor((f-lmin)/(lmax-lmin)*255.)
      
   #    length=self.data.image.sizes['t']
   #    ints={}
   #    for field,subdict in self.data.roi.items():
   #        ints[field]={}
   #        self.data.image.default_coords['v']=int(field.split(' ')[-1])
   #        print(field)
   #        for roi, item in subdict.items():
   #          if roi != 'Background':   
   #             ints[field][roi]={}
   #             for i,img in enumerate(self.data.image):
   #                img=normalize(imutils.resize(img, width=500, height=500))
   #                ints[field][roi][i]=np.mean(img[self.data.roi[field][roi]==255])-np.mean(img[self.data.roi[field]['Background']==255])
   #                print(field+" :"+str(i)+"/"+str(length))           
   #    self.data.results=ints
   #    print('finished')      
   # def analyse(self): 
   #    self.data.results=intensity_timeline(self.data.image,self.data.roi)


if __name__ == "__main__":
   app = QApplication(sys.argv)
   win = int_tracker()
   win.show()
   sys.exit(app.exec_())