import logging
import typing

from assetbrowser import houhelper

from assetbrowser import createAsset
try:
    from typing import TypedDict
except ImportError:
    from .typing_extensions import TypedDict
from enum import Enum
from os import path as opath
import os
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from .createAsset import Payload, PayloadType, processCreateAssetPayload
from . import asset
from . import config
from . import util
from .ui_editAsset import Ui_EditAsset
from .ui_assetInfo import Ui_AssetInfo
from .model import AssetFileModel, FilterAssetDir
import time
import datetime

try:
    import hou
except ImportError:
    logging.warning('running without hou module')
    from . import shimhou as hou


def alert(parent, title: str, text: str, buttons=QMessageBox.Ok):
    msg = QMessageBox(parent)
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setStandardButtons(buttons)
    msg.exec_()


def warnConfirm(parent, title: str, text: str):
    msg = QMessageBox(parent)
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
    msg.setIcon(QMessageBox.Warning)
    button = msg.exec_()
    return button == QMessageBox.Yes


class AssetItem(QStyledItemDelegate):
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        return super().paint(painter, option, index)


class AssetBrowser(QWidget):
    def __init__(self, show_debug=False) -> None:
        super().__init__()

        self._show_debug = show_debug

        parent_of_root = opath.dirname(config.root_path)

        # model
        model = AssetFileModel()
        model.setRootPath(parent_of_root)
        filtered = FilterAssetDir(model, config.root_path)
        self.model = model
        self.filteredModel = filtered

        # directory tree
        tree = QTreeView()
        tree.setHeaderHidden(True)
        tree.setModel(filtered)
        tree.setRootIndex(filtered.mapFromSource(model.index(parent_of_root)))
        root_index = filtered.mapFromSource(model.index(config.root_path))
        tree.setCurrentIndex(root_index)
        tree.setExpanded(root_index, True)
        tree.setIndentation(12)
        # show only first column
        for i in range(1, model.columnCount()):
            tree.hideColumn(i)
        # connect selection change
        tree.selectionModel().selectionChanged.connect(self.handleTreeSelectionChanged)
        self.treeWidget = tree

        # file list
        list = QListView()
        list.setModel(model)
        list.setViewMode(QListView.IconMode)
        list.setMovement(QListView.Static)
        list.setRootIndex(model.index(config.root_path))
        list.setUniformItemSizes(False)
        list.setGridSize(QSize(65, 85))
        list.setSpacing(10)
        list.setIconSize(QSize(60, 60))
        list.setItemDelegate(AssetItem())
        list.setResizeMode(QListView.Adjust)
        list.setDragEnabled(True)
        list.setDragDropMode(QAbstractItemView.InternalMove)

        # wiring signals
        list.selectionModel().selectionChanged.connect(self.handleListSelectionChanged)
        list.doubleClicked.connect(self.handleListDoubleClicked)

        self.listWidget = list

        # info
        info = AssetInfoWidget(file_model=model)
        self.infoWidget = info

        # laying out
        layout = QVBoxLayout()
        splitter = QSplitter()
        splitter.addWidget(tree)
        splitter.addWidget(list)
        splitter.addWidget(info)
        splitter.setSizes(config.init_panel_sizes)
        layout.addWidget(splitter)

        # debug
        if self._show_debug:
            debug_widget = QWidget()
            debug_layout = QHBoxLayout()
            debug_widget.setLayout(debug_layout)
            layout.addWidget(debug_widget)

            btn = QPushButton('show form')
            btn.clicked.connect(self.handleShowPress)
            load_btn = QPushButton('load asset')
            load_btn.clicked.connect(self.handleLoadPress)
            debug_layout.addWidget(btn)
            debug_layout.addWidget(load_btn)

        self.setLayout(layout)

        # drag and drop
        self.setAcceptDrops(True)

    def updateFileView(self, index: QModelIndex):
        self.listWidget.setRootIndex(index.siblingAtColumn(0))

    def getCurrentAsset(self):
        index = self.listWidget.currentIndex()
        asset_path = self.model.filePath(index)
        asset_obj = asset.getAsset(asset_path)
        return asset_obj

    def updateInfoView(self, asset_path: str):
        info = asset.getAsset(asset_path)
        # houhelper.loadAsset(info, None)
        self.infoWidget.setAsset(info)

    def handleTreeSelectionChanged(self, selected: QItemSelection, deselected):
        self.updateFileView(self.getCurrentFileModelIndex())

    def handleListSelectionChanged(self, selected: QItemSelection, deselected):
        index = self.listWidget.currentIndex()
        path = self.model.filePath(index)
        self.updateInfoView(path)

    def handleListDoubleClicked(self, index: QModelIndex):
        model = self.model
        info = model.fileInfo(index)
        path = info.filePath()
        if asset.isAssetFolder(path):
            return
        elif info.isDir():
            self.setCurrentDirectory(path)

    def getCurrentFileModelIndex(self) -> QModelIndex:
        index = self.treeWidget.currentIndex()
        return self.filteredModel.mapToSource(index)

    def getCurrentDirectory(self) -> str:
        return self.model.filePath(self.getCurrentFileModelIndex().siblingAtColumn(0))

    def setCurrentDirectory(self, path: str):
        file_index = self.model.index(path)
        filtered_index = self.filteredModel.mapFromSource(file_index)
        self.treeWidget.setCurrentIndex(filtered_index)
        self.listWidget.setRootIndex(file_index)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        # do not accept drop from list view itself
        if event.source() is self.listWidget:
            return
        else:
            event.acceptProposedAction()

    @staticmethod
    def printMimeData(event: QDropEvent):
        formats = event.mimeData().formats()
        d = [(f, event.mimeData().data(f)) for f in formats]
        print('data', d)

    def dropEvent(self, event: QDropEvent) -> None:
        item_data = event.mimeData().data(hou.qt._itemPathMimeType())
        if item_data.isEmpty():
            return

        items = str(item_data, 'utf-8').split('\t')
        payload = {
            'type': PayloadType.NetworkItems,
            'data': items
        }

        if self.listWidget.geometry().contains(event.pos()):
            # drop inside list widget
            self.beginCreateAsset(payload, self.getCurrentDirectory())
        elif self.infoWidget.geometry().contains(event.pos()):
            # drop inside info widget
            self.beginEditAsset(payload)

    def reloadCurrentAsset(self):
        index = self.listWidget.currentIndex()
        path = self.model.filePath(index)
        self.updateInfoView(path)

# region Debug

    def handleLoadPress(self):
        asset_obj = self.getCurrentAsset()
        print('loading', asset_obj.title())
        houhelper.loadAsset(asset_obj, node=hou.Node())
        pass
# endregion

    def handleShowPress(self):
        payload: Payload = {
            'type': PayloadType.Debug,
            'data': ['']
        }
        self.beginCreateAsset(payload, self.getCurrentDirectory())

    def beginCreateAsset(self, payload: Payload, path_to_create_in: str):
        def onSavePress(data: EditAssetFormData):
            asset_folder = asset.Asset.toAssetName(data['title'])
            if not asset_folder:
                raise Exception("Invalid Asset Name")

            p = opath.join(path_to_create_in, asset_folder)

            ref = asset.Ref.fromAbsPath(p)
            version = data['version']
            defRef = ref.toDef(version)

            if ref.existAsset():
                raise Exception("Asset already exists")
            if defRef.existDef():
                raise Exception("Asset definition already exists")

            assetObj = asset.Asset(ref)
            assetObj.setData(type=data['type'],
                             title=data['title'], tags=data['tags'])
            assetObj.setOrAddVersion(version, version)

            # create asset def
            assetDefObj = asset.AssetDef(defRef)
            content = processCreateAssetPayload(payload, assetDefObj)
            assetDefObj.setData(
                description=data['description'], createdOn=time.time(), content=content)

            # save assetObj and asset def
            asset.setAsset(assetObj)
            asset.setDef(assetDefObj)

            # copy preview image to thumbnail
            if data['previewImage']:
                target_dir = assetDefObj.ref().absDefDir()
                util.copyFile(data['previewImage'],
                              target_dir, config.thumbnail_filename)

            alert(self, 'Asset Saved', 'Asset save', QMessageBox.Ok)
            self.editAsset.close()

        try:
            asset_type = asset_type = createAsset.determineAssetTypeFromPayload(
                payload)
        except Exception as e:
            alert(self, 'Cannot Create Asset', str(e))
            return

        w = EditAssetWindow(mode=EditAssetWindow.Mode.New,
                            onSavePress=onSavePress,
                            asset_type=asset_type)
        # maintain reference so it's not destroyed immediately
        self.editAsset = w
        if 'qt' in dir(hou):
            w.setParent(hou.qt.mainWindow(), Qt.Window)

        w.show()

    def beginEditAsset(self, payload: Payload):

        current_asset = self.infoWidget.getCurrentAsset()
        current_def = self.infoWidget.getCurrentAssetDef()

        # guard no asset to edit
        if current_asset is None:
            alert(self, 'Cannot Edit Asset', 'No current asset selected')
            return

        # get asset type from payload
        try:
            asset_type = createAsset.determineAssetTypeFromPayload(
                payload)
        except Exception as e:
            alert(self, 'Cannot edit asset', str(e))
            return

        # guard mismatch asset type
        if current_asset.assetType() != asset_type:
            print(current_asset)
            alert(self, 'Cannot Edit Asset', 'Asset type mismatch %s != %s' %
                  (current_asset.assetType(), asset_type))
            return

        # save callback
        def onSavePress(data: EditAssetFormData):
            version = data['version']
            defRef = current_asset.ref().toDef(version)

            if defRef.existDef():
                if not warnConfirm(self, 'Warning', 'The entered version already exists. Do you want to replace?'):
                    return

            current_asset.setOrAddVersion(version, version)

            # create asset def
            assetDefObj = asset.AssetDef(defRef)
            content = processCreateAssetPayload(payload, assetDefObj)
            assetDefObj.setData(
                description=data['description'],
                createdOn=time.time(),
                content=content,
                changes=data['changes'])

            # save assetObj and asset def
            asset.setAsset(current_asset)
            asset.setDef(assetDefObj)

            # copy preview image to thumbnail
            if data['previewImage']:
                target_dir = assetDefObj.ref().absDefDir()
                util.copyFile(data['previewImage'],
                              target_dir, config.thumbnail_filename)

            alert(self, 'Asset Updated', 'Asset Updated', QMessageBox.Ok)
            self.editAsset.close()

            # reload asset
            self.reloadCurrentAsset()

        try:
            asset_type = asset_type = createAsset.determineAssetTypeFromPayload(
                payload)
        except Exception as e:
            alert(self, 'Cannot Create Asset', str(e))
            return

        w = EditAssetWindow(mode=EditAssetWindow.Mode.Edit,
                            asset_type=asset_type,

                            onSavePress=onSavePress)
        w.setIntialData(assetObj=current_asset, version=self.infoWidget.getSelectedVersion(
        ), asset_def=current_def)
        # maintain reference so it's not destroyed immediately
        self.editAsset = w
        if 'qt' in dir(hou):
            w.setParent(hou.qt.mainWindow(), Qt.Window)

        w.show()


class EditAssetFormData(TypedDict):
    type: str
    title: str
    version: str
    tags: typing.List[str]
    description: str
    changes: str
    previewImage: str


class EditAssetWindow(QWidget, Ui_EditAsset):
    class Mode(Enum):
        New = 0
        Edit = 1

    def __init__(self, parent: typing.Optional[QWidget] = None, mode=Mode.New, asset_type=None, onSavePress: typing.Callable[[EditAssetFormData], None] = None) -> None:
        super().__init__(parent)
        self.onSavePress = onSavePress
        self.setupUi(self)
        self.setTitle(mode)
        self.asset_type.setText(asset_type if asset_type is not None else '')
        self._previewPath = None
        self._tempfilePath = None

        # adjust ui base on mode
        if mode == self.Mode.New:
            self.asset_changes.hide()
            self.lb_changes.hide()
            self.asset_title.setReadOnly(False)
        elif mode == self.Mode.Edit:
            self.asset_changes.show()
            self.lb_changes.show()
            self.asset_title.setReadOnly(True)

        # setup signals
        self.form_buttons.accepted.connect(self.handleSave)
        self.form_buttons.rejected.connect(self.handleClose)
        self.btn_capture.clicked.connect(self.handleCaptureClicked)
        self.btn_clear.clicked.connect(self.clearPreviewImage)
        self.btn_plusMajor.clicked.connect(self.handlePlusMajorClicked)
        self.btn_plusMinor.clicked.connect(self.handlePlusMinorClicked)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.fitPreviewImage()
        return super().resizeEvent(event)

    def setTitle(self, mode):
        if mode == self.Mode.New:
            self.setWindowTitle('New Asset')
        elif mode == self.Mode.Edit:
            self.setWindowTitle('Edit Asset')
        else:
            print('Unknown mode: ', mode)

    def setIntialData(self, assetObj: asset.Asset, version: str = None, asset_def: asset.AssetDef = None):
        self.asset_title.setText(assetObj.title())
        self.asset_type.setText(assetObj.assetType())
        if version:
            ver = asset.Version(version)
            self.asset_major.setValue(ver.version[0])
            self.asset_minor.setValue(ver.version[1])
        if asset_def:
            self.asset_description.setText(asset_def.description())

    def data(self) -> EditAssetFormData:
        return {
            'type': self.asset_type.text(),
            'title': self.asset_title.text(),
            'tags': self.getTags(),
            'version': str(asset.Version(self.asset_major.value(), self.asset_minor.value())),
            'description': self.asset_description.toPlainText(),
            'changes': self.asset_changes.toPlainText(),
            'previewImage': self._previewPath
        }

    def getTags(self) -> typing.List[str]:
        tag_text = self.asset_tags.text()
        tags = asset.splitTags(tag_text)
        return tags

    def closeEvent(self, event: QCloseEvent) -> None:
        super().closeEvent(event)
        self.setParent(None)

    def handleSave(self):
        if self.onSavePress:
            try:
                self.onSavePress(self.data())
            except Exception as e:
                alert(self, 'An Error Occured', str(e))

    def handleClose(self):
        # clean up
        self._deleteTempFile()
        self.close()

    def setPreviewImage(self, filepath: str):
        self._previewPath = filepath
        pixmap = QPixmap(filepath)
        pixmap = pixmap.scaled(self.asset_preview.size(),
                               Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.asset_preview.setPixmap(pixmap)

    def clearPreviewImage(self):
        self.asset_preview.clear()
        self._pixmap = None
        self._previewPath = None

    def fitPreviewImage(self):
        if self._previewPath:
            self.setPreviewImage(self._previewPath)

    def _deleteTempFile(self):
        if not self._tempfilePath:
            return
        if os.path.isfile(self._tempfilePath):
            os.remove(self._tempfilePath)
        self._tempfilePath = None

    def _newTempFilePath(self) -> str:
        """
        delete current temp file if it exists and return new temp file path
        """
        self._deleteTempFile()
        path = util.getTempFilePath('jpg')
        self._tempfilePath = path
        return path

    def handleCaptureClicked(self):
        # capture viewport to a temporary file and display it
        path = self._newTempFilePath()
        houhelper.captureViewport(file=path, size=(200, 200))
        self.setPreviewImage(path)

    def handlePlusMajorClicked(self):
        self.asset_major.setValue(self.asset_major.value() + 1)
        self.asset_minor.setValue(0)

    def handlePlusMinorClicked(self):
        self.asset_minor.setValue(self.asset_minor.value() + 1)


class AssetInfoWidget(QWidget, Ui_AssetInfo):
    def __init__(self, file_model: AssetFileModel, parent: typing.Optional[QWidget] = None):
        super().__init__(parent)
        self.setupUi(self)
        self.clear()
        self._file_model = file_model

        # set signal
        self.asset_versionSelect.currentIndexChanged.connect(
            self.handleVersionChanged)

    def handleVersionChanged(self, index):
        if index < 0:
            # items are cleared
            return
        if not self._asset:
            return

        try:
            version = self._versions[index]
        except IndexError:
            print('index out of range')
            return

        defObj = self._asset.resolveVersion(version).getDef()
        self.setAssetDef(defObj)

        # set selected version to file model
        if self._asset:
            self._file_model.setSelectedVersion(
                self._asset.ref().absAssetDir(), version)

    def clear(self):
        self._asset = None
        self._assetDef = None
        self._versions = []
        self.asset_name.setText('-')
        self.asset_versionSelect.clear()
        self.asset_description.setText('-')
        self.asset_createdDate.setText('-')
        self.asset_tags.setText('-')
        self.asset_changes.setText('-')

    def setAsset(self, assetObj: typing.Union[asset.Asset, None]):
        if assetObj is None:
            self.clear()
        else:
            self._asset = assetObj
            versions = list(assetObj.versions())
            # sort starting from latest
            versions.sort(key=asset.Version, reverse=True)
            self._versions = versions

            self.asset_name.setText(assetObj.title())

            # fill version selector
            self.asset_versionSelect.clear()
            latest = assetObj.latestVersion()

            prev_selected_version = self._file_model.getSelectedVersion(
                assetObj.ref().absAssetDir())

            self.asset_versionSelect.addItems(
                ['%s (latest)' % v if v == latest else v for v in versions])
            # preserve selected version even after listview selection change
            if prev_selected_version:
                try:
                    index = versions.index(prev_selected_version)
                    self.asset_versionSelect.setCurrentIndex(index)
                except:
                    pass
            tags = assetObj.tags()
            self.asset_tags.setText(', '.join(tags) if len(tags) else '-')

    def clearDef(self):
        self.asset_description.setText('-')
        self.asset_createdDate.setText('-')
        self.asset_changes.setText('-')
        self._assetDef = None

    def setAssetDef(self, defObj: typing.Union[asset.AssetDef, None]):
        if defObj is None:
            # clear asset def fields
            self.clearDef()
        else:
            self._assetDef = defObj
            # fill description, createdDate, tags
            self.asset_description.setText(defObj.description() or '-')
            self.asset_createdDate.setText(self.formatDate(defObj.createdOn()))
            self.asset_changes.setText(defObj.changes())

    def getCurrentAsset(self):
        return self._asset

    def getCurrentAssetDef(self):
        return self._assetDef

    def getSelectedVersion(self):
        try:
            return self._versions[self.asset_versionSelect.currentIndex()]
        except:
            return None

    @staticmethod
    def formatDate(timestamp):
        date = datetime.date.fromtimestamp(timestamp)
        return date.strftime('%c')
