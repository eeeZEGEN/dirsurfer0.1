from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QLineEdit, QVBoxLayout, QWidget, QPushButton
from PyQt5.Qt import QStandardItemModel, QStandardItem
from PyQt5.QtGui import QFont, QColor
import sys as s
import os


class CommonItem(QStandardItem):
	'''
	Common item class
	'''
	def __init__(self, txt='', font_size=12, set_bold=False, color=QColor(0, 0, 0), path='home'):
		super().__init__()

		fnt = QFont('Open Sans', font_size)

		fnt.setBold(set_bold)
		self.setEditable(False)
		self.setForeground(color)
		self.setFont(fnt)
		self.setText(txt)


class Dirsurfer(QMainWindow):
	'''
	Main app class
	''' 
	def __init__(self, root_dir):
		super(Dirsurfer, self).__init__()
		self.setWindowTitle('Dirsurfer')
		self.resize(1920, 1080)
		self.current_path = root_dir
		self.root_item = CommonItem('~', 16, set_bold=True, color=QColor(1, 204, 67))

		self.makingUI()


	def makingUI(self):

		# Edit line
		self.qlineEdit = QLineEdit()
		self.qlineEdit.setFixedSize(400, 30)

		# Tree widget
		self.treeView = QTreeView()
		self.treeView.setHeaderHidden(True)
		treeModel = QStandardItemModel()
		rootNode = treeModel.invisibleRootItem()

		self.pathSurf(self.current_path, self.root_item)

		rootNode.appendRow(self.root_item)
		self.treeView.setModel(treeModel)
	

		# Create widget
		widget = QWidget()

		# Create button
		self.pushButton = QPushButton(text='Filter')
		self.pushButton.setFixedSize(100, 30)
		self.pushButton.clicked.connect(lambda: self.updateFilteredTree())

		# Create central box
		centralBox = QVBoxLayout()

		# Adding to layout
		centralBox.addWidget(self.qlineEdit)
		centralBox.addWidget(self.pushButton)
		centralBox.addWidget(self.treeView)

		# Setting layout
		widget.setLayout(centralBox)

		self.setCentralWidget(widget)


	def pathSurf(self, path, item: CommonItem):

		for i in os.listdir(path):
			if os.path.isdir(path + i):
				current_item = CommonItem(i, 14, set_bold=True, color=QColor(1, 204, 67))
				item.appendRow(current_item)
				self.pathSurf(path + i + '/', current_item)
			else:
				current_item = CommonItem(i, 12, set_bold=False)
				item.appendRow(current_item)


	def filterSurf(self, path, item: CommonItem):

		filter_name: str = self.qlineEdit.text()

		for i in os.listdir(path):
			if os.path.isdir(path + i):
				if i == filter_name:
					current_item = CommonItem(f'{i} path: {path}', 14, set_bold=True, color=QColor(1, 204, 67))
					item.appendRow(current_item)
					self.pathSurf(path + i + '/', current_item)
				else:
					self.filterSurf(path + i + '/', item)
			else:
				if i == filter_name:
					current_item = CommonItem(f'{i} path: {path}', 12, set_bold=False)
					item.appendRow(current_item)


	def updateFilteredTree(self):

		treeModel = QStandardItemModel()
		rootNode = treeModel.invisibleRootItem()
		self.root_item = CommonItem('Filtered', 16, set_bold=True, color=QColor(1, 204, 67))

		if self.qlineEdit.text() != '':
			self.filterSurf(self.current_path, self.root_item)
			rootNode.appendRow(self.root_item)
			self.treeView.setModel(treeModel)
			self.treeView.expandAll()
		else:
			self.root_item = CommonItem('~', 16, set_bold=True, color=QColor(1, 204, 67))
			self.pathSurf(self.current_path, self.root_item)
			rootNode.appendRow(self.root_item)
			self.treeView.setModel(treeModel)



if __name__ == "__main__":
	app = QApplication(s.argv)
	
	uname = os.popen('whoami').read().replace('\n', '')
	dirsurfer = Dirsurfer(f'/home/{uname}/')
	dirsurfer.show()
	
	s.exit(app.exec_())

'''
Начинает с /home/roman/
ПОлучает список имен например t1 t2 t3
сравнивает имя с фильтрационным и если совпадает то добавляем этот элемент в корневую ноду если нет
'''