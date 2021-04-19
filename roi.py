from PySide2.QtCore import Signal
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import (QApplication, QHeaderView, QHBoxLayout,
                               QPushButton, QTableWidget, QTableWidgetItem,QCheckBox,
                               QWidget, QVBoxLayout, QShortcut)
import sys

class def_roi(QWidget):
   
   add_roi = Signal(str)
 
   def __init__(self, parentData=None):
      QWidget.__init__(self)
      self.parentdata=parentData
      self.setup_ui()
      self.shortcuts()
      # self.setFixedSize(200, 150)
      self.setWindowTitle('RoI')
      
   def shortcuts(self):
      self.quit =QShortcut(QKeySequence("Ctrl+q"), self)
      self.quit.activated.connect(self.close)
      
   def setup_ui(self):
      layout=QVBoxLayout()
      buttons=QHBoxLayout()
      add_button=QPushButton('add')
      add_button.clicked.connect(self.init_add)
      rem_button=QPushButton('remove')
      buttons.addWidget(add_button)
      buttons.addWidget(rem_button)
      self.table=QTableWidget()
      self.table.setRowCount(0)
      self.table.setColumnCount(1)
      self.table.horizontalHeader().setSectionResizeMode(0,QHeaderView.Stretch)
      box=QCheckBox("Show RoIs")
      layout.addLayout(buttons)
      layout.addWidget(self.table)
      layout.addWidget(box)
      self.setLayout(layout)

   def init_add(self):
      self.add_roi.emit("RoI {}".format(self.table.rowCount()))

   def add_row(self):
      rowPosition = self.table.rowCount()
      self.table.insertRow(rowPosition)
      self.table.setItem(rowPosition , 0, QTableWidgetItem("RoI {}".format(rowPosition)))


if __name__ == "__main__":
   app = QApplication(sys.argv)
   win = def_roi()
   win.show()
   sys.exit(app.exec_())