import hou
from assetbrowser import model, houhelper, asset
import logging


def dropAccept(files):
    mimeType = model.mimeTypes['assetItem']
    # custom mime type can be checked if it exists but is not supported for reading from
    # so files argument is use instead
    if hou.ui.hasDragSourceData(mimeType):
        tryLoadAsset(files)
        return True
    return False


def tryLoadAsset(files):
    pane = hou.ui.paneTabUnderCursor()
    node = pane.pwd()
    if not len(files):
        return

    item_to_load = files[0]

    # drop on network view
    if (pane.type().name() == "NetworkEditor"):
        assetObj = asset.getAsset(item_to_load)
        if not assetObj:
            logging.warning('Asset %s not found' % item_to_load)
            return
        houhelper.loadAsset(assetObj=assetObj, node=node)
