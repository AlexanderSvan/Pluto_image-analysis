from PySide2.QtCore import QSize, Slot, Signal
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (QApplication, QMainWindow, QActionGroup,
                               QAction, QToolBar, QStatusBar)
import sys
from open_image import load_img
from timelaps_window import timelaps
from roi import def_roi
import numpy as np
from measure import measure_wid
from intensity_tracking import int_tracker

class MainApp(QMainWindow):
   
    annot_signal=Signal()
    clear_signal=Signal()
    save_signal=Signal()

    def __init__(self):
        super(MainApp, self).__init__()
        self.setGeometry(300,300,350,50)
        self.create_menu()
        self.toolbar()
        self.image=None
        self.pointer=None
        self.show_annot=False
        self.roi={}

    def toolbar(self):
        toolbar=QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16,16))
        self.addToolBar(toolbar)
        
        mouse=QAction(QIcon('./icons/icons-01.png'), 'mouse', self, checkable=True)
        mouse.setStatusTip('mouse')
        mouse.triggered.connect(lambda: self.set_pointer('mouse'))
        
        square=QAction(QIcon('./icons/icons_Square.png'), 'square', self, checkable=True)
        square.setStatusTip('square')
        square.triggered.connect(lambda: self.set_pointer('square'))
        
        circle=QAction(QIcon('./icons_Circle.png'), 'circle', self, checkable=True)
        circle.setStatusTip('circle')
        circle.triggered.connect(lambda: self.set_pointer('circle'))
        
        crosshair=QAction(QIcon('./icons/icons_Crosshair.png'), 'crosshair', self, checkable=True)
        crosshair.setStatusTip('crosshair')
        crosshair.triggered.connect(lambda: self.set_pointer('cross'))
        
        brush=QAction(QIcon('./icons/icons_Brush.png'), 'brush', self, checkable=True)
        brush.setStatusTip('crosshair')
        brush.triggered.connect(lambda: self.set_pointer('brush'))
         
        
        group = QActionGroup(self, exclusive=True)
        
        for action in (mouse,square, circle, crosshair, brush):
           toolbar.addAction(action)
           group.addAction(action)
           
        annotations=QAction(QIcon('./icons/icons_Circle.png'), 'Annot', self, checkable=True)
        annotations.setStatusTip('Toggle annotations')
        annotations.triggered.connect(self.toggel_annot)
        toolbar.addAction(annotations)
        
        clear=QAction(QIcon('./icons/icons_Square.png'), 'Clear', self)
        clear.setStatusTip('Clear annotations')
        clear.triggered.connect(self.clear_annot)
        toolbar.addAction(clear)        
        
        self.setStatusBar(QStatusBar(self))     
        
    def create_menu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        viewMenu = mainMenu.addMenu("View")
        editMenu = mainMenu.addMenu("Edit")
        analysisMenu = mainMenu.addMenu("Analysis")
        helpMenu = mainMenu.addMenu("Help")
 
        openAction = QAction("Open", self)
        openAction.triggered.connect(self.load)
        openAction.setShortcut("Ctrl+O")
        exportAction = QAction("Export", self)
        exportAction.setShortcut("Ctrl+e")
        exportAction.triggered.connect(self.export_img)
        exitAction = QAction("Exit", self)
        exitAction.triggered.connect(self.close)
        exitAction.setShortcut("Ctrl+q")
        
        membTransAction = QAction('Membrane Translocation', self)
        thresholdAction = QAction('Threshold', self)
        RoIAction = QAction('RoI', self)
        RoIAction.triggered.connect(self.set_roi)
        MeasureAction = QAction('Measure', self)
        MeasureAction.triggered.connect(self.measure)
        int_trackAction = QAction('Intensity Tracking', self)
        int_trackAction.triggered.connect(self.int_track)        
        
        
        analysisMenu.addAction(membTransAction)
        analysisMenu.addAction(thresholdAction)
        analysisMenu.addAction(RoIAction)
        analysisMenu.addAction(MeasureAction)
        analysisMenu.addAction(int_trackAction)        
        fileMenu.addAction(openAction)
        fileMenu.addAction(exportAction)
        fileMenu.addAction(exitAction)
    
    def load(self):
        self.win=load_img(self)
        self.win.show()
        self.win.switch_window.connect(self.display)
        
    def display(self):
        self.show_img=timelaps(self, self.image)
        self.show_img.show()
   
    def set_pointer(self, selection):
        self.pointer=selection
        
    def set_roi(self):
        self.roi_win=def_roi()
        self.roi_win.show()
        self.roi_win.add_roi.connect(self.get_roi)
    
    @Slot(str)
    def get_roi(self, name):
        self.show_img.save_roi(name)
        if hasattr(self, 'roi_win'):
           self.roi_win.add_row()
        elif hasattr(self, 'int_track_win'):
           self.int_track_win.add_row()
        
    def toggel_annot(self):
        self.show_annot=np.invert(self.show_annot)
        self.annot_signal.emit()
   
    def clear_annot(self):
        self.clear_signal.emit()
        
    def measure(self):
       self.measure_win=measure_wid(self)
       self.measure_win.show()
       
    def int_track(self):
       self.int_track_win=int_tracker(self)
       self.int_track_win.show() 
       self.int_track_win.add_roi.connect(self.get_roi)
      
    def export_img(self):
       self.save_signal.emit()
       
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainApp()
    win.show()
    sys.exit(app.exec_())