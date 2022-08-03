from PySide2.QtWidgets import QApplication
from assetbrowser import ui

app = QApplication()
browser = ui.AssetBrowser(True)
browser.show()
app.exec_()
