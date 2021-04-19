from PySide2.QtCore import Signal
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton,QWidget, QVBoxLayout, QShortcut, QFileDialog, QComboBox)
import sys
import nd2reader as nd2 

class load_img(QWidget):
   
    switch_window = Signal()
       
    def __init__(self, parentData):
        QWidget.__init__(self)
        self.data=parentData
        self.file_open()
        self.setup_ui()
        self.shortcuts()
        self.setFixedSize(200, 150)
        self.setWindowTitle('Import timeseries')

    def shortcuts(self):
        self.quit =QShortcut(QKeySequence("Ctrl+q"), self)
        self.quit.activated.connect(self.close)
    
    def def_combobox_changed(self, value):
        self.def_val.clear()
        if self.def_lbl.currentText() != ' ':
            self.def_val.addItems([str(a) for a in range(self.dims[self.def_lbl.currentText()])])

    def setup_ui(self):
        """Initialize widgets.
        """
        layout=QVBoxLayout()
        label=QLabel('Dimensions: '+(' ').join(list(self.frame.sizes.keys())))
        
        iter_axis=QHBoxLayout()
        self.iter_lable=QLabel('Iter axis')
        self.iter_lbl=QComboBox()
        self.iter_lbl.addItems([a for a in self.dims.keys() if a not in ['x','y']])
        iter_axis.addWidget(self.iter_lable)
        iter_axis.addWidget(self.iter_lbl)
        
        def_axis=QHBoxLayout()
        self.def_lable=QLabel('Default coord')
        self.def_lbl=QComboBox()
        self.def_lbl.addItems([' ']+[a for a in self.dims.keys() if a not in ['x','y']])
        self.def_lbl.currentTextChanged.connect(self.def_combobox_changed)
        self.def_val=QComboBox()
        if self.def_lbl.currentText() == ' ':
            pass
        else:
            self.def_val.addItems([str(a) for a in range(self.dims[self.def_lbl.currentText()])])
        def_axis.addWidget(self.def_lable)
        def_axis.addWidget(self.def_lbl)
        def_axis.addWidget(self.def_val)
                
        load_button=QPushButton('Load')
        load_button.clicked.connect(self.load)
        close_button=QPushButton('Cancel')
        close_button.clicked.connect(self.close)
        
        buttons=QHBoxLayout()
        buttons.addWidget(load_button)
        buttons.addWidget(close_button)
        
        layout.addWidget(label)
        layout.addLayout(iter_axis)
        layout.addLayout(def_axis)
        layout.addLayout(buttons)
        self.setLayout(layout)
        
    def load(self):
        assigned=[self.def_lbl.currentText(), self.iter_lbl.currentText()]
        print(''.join([a for a in list(self.dims.keys()) if a not in assigned])[::-1])
        self.frame.bundle_axis=''.join([a for a in list(self.dims.keys()) if a not in assigned])[::-1]
        if self.def_lbl.currentText() != ' ':
            self.frame.default_coords[self.def_lbl.currentText()]=int(self.def_val.currentText())
        self.frame.iter_axis=self.iter_lbl.currentText()
        self.data.field=int(self.def_val.currentText())
        STORE=self.frame.parser._raw_metadata.image_metadata[b'SLxExperiment'][b'ppNextLevelEx'][b''][b'uLoopPars'][b'Points'][b'']
        self.data.field_name={i: point[b'dPosName'].decode("utf-8")  for i, point in enumerate(STORE)}
        self.data.image=self.frame
        self.switch_window.emit()
        self.close()

    def file_open(self):
        name=QFileDialog.getOpenFileName(self, 'Open File', filter="ND2 files (*.nd2);;TIFF (*.tif);;All files (*)")
        self.frame=nd2.ND2Reader(name[0])
        self.dims=self.frame.sizes


if __name__ == "__main__":
   app = QApplication(sys.argv)
   win = load_img()
   win.show()
   sys.exit(app.exec_())