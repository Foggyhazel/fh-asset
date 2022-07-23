import typing
from os import path as opath
from PySide2.QtWidgets import QFileSystemModel
from PySide2.QtCore import QModelIndex, Qt, QSortFilterProxyModel, QMimeData, QByteArray
from PySide2.QtGui import QColor, QIcon
from . import asset, config

mimeTypes = {
    'assetItem': 'application/assetbrowser.asset-item'
}


class AssetFileModel(QFileSystemModel):
    def hasChildren(self, parent: QModelIndex = ...) -> bool:
        """
        If parent is an asset folder, do not show its content
        """
        path = self.filePath(parent)
        if asset.isAssetFolder(path):
            return False
        return super().hasChildren(parent)

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        path = self.filePath(index)

        if not asset.isAssetFolder(path):
            return super().data(index, role)

        if role == Qt.ForegroundRole:
            return QColor(*config.asset_label_color)
        elif role == Qt.DecorationRole:
            return QIcon(asset.resource_filename('assetbrowser', "icons/asset.png"))
        else:
            return super().data(index, role)

    def mimeTypes(self) -> typing.List:
        return [mimeTypes['assetItem']]

    def mimeData(self, indexes: typing.List[QModelIndex]) -> QMimeData:
        item_paths = []
        for index in indexes:
            if not index.isValid():
                continue
            path = self.filePath(index)
            if not asset.isAssetFolder(path):
                continue

            item_paths.append(path)

        path_str = '\t'.join(item_paths)
        data = QByteArray(bytes(path_str, 'utf-8'))
        mimeData = QMimeData()
        mimeData.setData(mimeTypes['assetItem'], data)
        mimeData.setUrls(item_paths)
        return mimeData
        return super().mimeData(indexes)


class FilterAssetDir(QSortFilterProxyModel):
    def __init__(self, fileModel: QFileSystemModel, root_path: str) -> None:
        super().__init__()
        self.fileModel = fileModel
        self.root_path = root_path
        self.setSourceModel(fileModel)

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        # hide asset folder
        index = source_parent.child(source_row, 0)
        path = self.fileModel.filePath(index)
        if asset.isAssetFolder(path):
            return False
        # hide root path siblings
        if not self.samefile(path, self.root_path) and self.samefile(opath.dirname(path), opath.dirname(self.root_path)):
            return False
        return super().filterAcceptsRow(source_row, source_parent)

    @staticmethod
    def samefile(pathA: str, pathB: str):
        # return opath.samefile(pathA, pathB)
        np1 = opath.normpath(pathA)
        np2 = opath.normpath(pathB)
        return np1 == np2
