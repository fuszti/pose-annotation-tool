import os
from collections import namedtuple
import yaml
from PySide2.QtWidgets import QMainWindow
from ui_mainwindow import Ui_MainWindow
from newprojectdialog import NewProjectDialog
from singleviewprojectmainwindow import SingleviewProjectMainWindow
from multiviewprojectmainwindow import MultiviewProjectMainWindow
from depthprojectmainwindow import DepthProjectMainWindow
from alert import Alert

class MainWindow(QMainWindow):    
	def __init__(self):
		self.projectWindowIdGenerator = 0
		self.openProjectWindows = {}
		super(MainWindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		
		self.ui.actionNew_Project.triggered.connect(self.startNewProject)
		
	def startNewProject(self):
		d = NewProjectDialog(self)
		d.exec_()
			
	def startOpenProject(self):
		pass
			
	def doOpenProject(self, projectPath):
		f = open(os.path.join(projectPath, 'cfg.yaml'), 'r')
		cfg = yaml.safe_load(f)
		# unnecessary, but feels cleaner to access the fields when it's a namedtuple
		cfg = namedtuple("cfg", cfg.keys())(*cfg.values())
		if cfg.mode == 'RGB Single View':
			w = SingleviewProjectMainWindow(cfg)
		elif cfg.mode == 'RGB Multi View':
			w = MultiviewProjectMainWindow(cfg)
		elif cfg.mode == 'RGB Depth':
			w = DepthProjectMainWindow(cfg)
		else:
			Alert('Project Mode must be "RGB Single View", "RGB Multi View", or "RGB Depth", but was %s'%str(cfg.mode)).exec_()
			return
		self.openProjectWindows[self.projectWindowIdGenerator] = w
		self.projectWindowIdGenerator += 1
		w.show()