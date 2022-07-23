from PySide2.QtWidgets import QApplication
from assetbrowser import ui

app = QApplication()
browser = ui.AssetBrowser()
browser.show()
app.exec_()

