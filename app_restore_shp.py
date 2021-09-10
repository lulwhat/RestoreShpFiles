import sys
import os.path
from PyQt5.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout, 
	QLabel, QLineEdit, QProgressBar, QPushButton, QFileDialog, QMessageBox
		)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from restore_shp_functionality import *

class GuiFixShp(QDialog):
	def __init__(self, parent=None):
		super(GuiFixShp, self).__init__(parent)

		self.shp_path = os.path.expanduser("~/Documents")
		self.originalPalette = QApplication.palette()

		# create top horisontal layout for shp path
		labelShp = QLabel("Выберите шейпфайл:")
		self.textFieldShp = QLineEdit()
		browseShpButton = QPushButton("Обзор")
		browseShpButton.clicked.connect(self.chooseShpFileDialog)

		topLayout = QHBoxLayout()
		topLayout.addWidget(labelShp)
		topLayout.addWidget(self.textFieldShp)
		topLayout.addWidget(browseShpButton)

		#bottom layout with restore button
		restoreButton = QPushButton("Восстановить")
		restoreButton.clicked.connect(self.restoreButtonAction)
		self.progressBar = QProgressBar()
		self.progressBar.setValue(0)

		botLayout = QHBoxLayout()
		botLayout.addWidget(self.progressBar)
		botLayout.addWidget(restoreButton)


		# create main layout
		mainLayout = QGridLayout()        
		mainLayout.addLayout(topLayout, 0, 0, 1, 2)
		mainLayout.addLayout(botLayout, 1, 0, 1, 2)

		self.setLayout(mainLayout)
		self.setWindowTitle("Восстановка шейпфайла")
		self.setFixedSize(640, 150)
		self.setWindowIcon(QIcon("icons/logo_ug.png"))
		self.setWindowFlags(Qt.WindowFlags())
		

	def chooseShpFileDialog(self):
		self.progressBar.setValue(0)
		options = QFileDialog.Options()
		fileName, _ = QFileDialog.getOpenFileName(
			self,
			"Выберите шейпфайл",
			self.shp_path + "/*.shp",
			"ArcGIS шейпфайлы (*.shp);;Все файлы (*)",
			options=options
		)
		if fileName:
			self.shp_path = fileName
			# change forward slash to windows one
			self.textFieldShp.setText(fileName.replace("/", "\\"))

	def restoreButtonAction(self):
		self.progressBar.setValue(0)
		restoreShp = RestoreShp()
		try:
			restoreShp.restore(self.shp_path)
			self.progressBar.setValue(100)
			QMessageBox.about(self, "Восстановка шейпфайла", "Восстановленный шейпфайл создан")
		except WrongLayerNameError:
			msg = QMessageBox()
			msg.warning(self, "Ошибка", "Неверное имя слоя шейпфайла")
		except ShpNotFoundError:
			msg = QMessageBox()
			msg.warning(self, "Ошибка", "Неверный путь, шейпфайл не найден")
		except LayersStructureNotFoundError:
			msg = QMessageBox()
			msg.warning(self, "Ошибка", "Не найден файл структуры слоёв layers_structure.xlsx")
		except UtilityShpFilesError:
			msg = QMessageBox()
			msg.warning(self, "Ошибка", "Ошибка во вспомогательных файлах шейпа (.dbf, .shx, .cpg)")
		except Exception:
			msg = QMessageBox()
			msg.warning(self, "Ошибка", "Неизвестная ошибка приложения")


if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.setStyle("Fusion")
	gallery = GuiFixShp()
	gallery.show()
	sys.exit(app.exec_())