from os import path as opath
from PySide2.QtWidgets import QFileSystemModel
from PySide2.QtCore import *
from PySide2.QtGui import *
from . import asset, config

mimeTypes = {
    'assetItem': 'application/assetbrowser.asset-item'
}


class AssetFileModel(QFileSystemModel):
    def __init__(self, parent=None):
        self._selectedVersion = {}
        super(AssetFileModel, self).__init__(parent)

    def hasChildren(self, parent):
        """
        If parent is an asset folder, do not show its content
        """
        path = self.filePath(parent)
        if asset.isAssetFolder(path):
            return False
        return super(AssetFileModel, self).hasChildren(parent)

    def data(self, index, role):
        path = self.filePath(index)

        if not asset.isAssetFolder(path):
            return super(AssetFileModel, self).data(index, role)

        if role == Qt.ForegroundRole:
            return QColor(*config.asset_label_color)
        elif role == Qt.DecorationRole:
            # return latest version thumnail or default thumbnail
            ref = asset.Ref.fromAbsPath(path)
            assetObj = ref.getAsset()
            latestDef = assetObj.resolveVersion(
                self.getSelectedVersion(path) or assetObj.latestVersion())

            if latestDef:
                thumbpath = asset.findThumbnail(latestDef)
                if thumbpath:
                    return QIcon(thumbpath)

            return QIcon(asset.resource_filename('assetbrowser', "icons/asset.png"))
        else:
            return super(AssetFileModel, self).data(index, role)

    def mimeTypes(self):
        return [mimeTypes['assetItem']]

    def setSelectedVersion(self, abs_assetDir, version):
        k = opath.normpath(abs_assetDir)
        self._selectedVersion[k] = version
        index = self.index(k)
        self.dataChanged.emit(index, index, [Qt.DisplayRole])

    def getSelectedVersion(self, abs_assetDir):
        k = opath.normpath(abs_assetDir)
        return self._selectedVersion.get(k, None)

    def mimeData(self, indexes):
        item_paths = []
        for index in indexes:
            if not index.isValid():
                continue
            path = self.filePath(index)
            if not asset.isAssetFolder(path):
                continue

            item_paths.append(path)

        mimeData = QMimeData()

        if not len(item_paths):
            mimeData.setUrls([])
            return mimeData

        path_str = '\t'.join(item_paths)
        data = QByteArray(path_str.encode('UTF-8'))

        # mark drag drop data as coming from asset browser.
        # the actual data does not matter as houdini cannot read it anyway
        mimeData.setData(mimeTypes['assetItem'], data)

        # set url to [path@version]
        path = item_paths[0]
        ver = self.getSelectedVersion(path)

        if ver:
            path = path + '?version=%s' % ver

        mimeData.setUrls([path])
        return mimeData


class FilterAssetDir(QSortFilterProxyModel):
    def __init__(self, fileModel, root_path):
        super(FilterAssetDir, self).__init__()
        self.fileModel = fileModel
        self.root_path = root_path
        self.setSourceModel(fileModel)

    def filterAcceptsRow(self, source_row, source_parent):
        # hide asset folder
        index = source_parent.child(source_row, 0)
        path = self.fileModel.filePath(index)
        if asset.isAssetFolder(path):
            return False
        # hide root path siblings
        if not self.samefile(path, self.root_path) and self.samefile(opath.dirname(path), opath.dirname(self.root_path)):
            return False
        return super(FilterAssetDir, self).filterAcceptsRow(source_row, source_parent)

    def filePath(self, index):
        src_index = self.mapToSource(index)
        return self.fileModel.filePath(src_index.siblingAtColumn(0))

    def indexFromPath(self, path):
        src_index = self.fileModel.index(path)
        return self.mapFromSource(src_index)
        

    @staticmethod
    def samefile(pathA, pathB):
        # return opath.samefile(pathA, pathB)
        np1 = opath.normpath(pathA)
        np2 = opath.normpath(pathB)
        return np1 == np2
