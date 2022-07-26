from genericpath import isfile
import logging
import typing
from os import path as opath
from . import asset
import os
try:
    import hou
except ImportError:
    from . import shimhou as hou
import tempfile


def getNetworkType(item_path: str):
    item = hou.item(item_path)
    if not item:
        raise Exception('item not found in path %s' % item_path)

    parent = item.parent()
    return parent.childTypeCategory().name()


def dumpNodeItemsToFile(items: typing.List[str], abs_file_path: str):
    """save items to file

    Args:
        items (typing.List[str]): network items
        abs_file_path (str): file to write to

    Raises:
        Exception: item not found
    """
    network_items = hou.items(items)

    if not len(network_items):
        raise Exception('No network items')

    parent = network_items[0].parent()

    path = opath.normpath(abs_file_path)
    dir = opath.dirname(path)

    if not opath.exists(dir):
        os.makedirs(dir, exist_ok=True)

    parent.saveItemsToFile(network_items, path)


def loadAsset(assetObj: asset.Asset, node: hou.Node, version_label=None):
    v = version_label or assetObj.latestVersion()
    defObj = assetObj.resolveVersion(v).getDef()
    if not defObj:
        logging.warning('Cannot load asset %s@%s' % (assetObj.title(), v))
        return

    # TODO: check asset type and matching loading method
    content = defObj.content()
    abs_path = opath.join(defObj.ref().absDefDir(), content)

    node.loadItemsFromFile(abs_path)


def sceneViewer() -> typing.Union[hou.SceneViewer, None]:
    curDesktop = hou.ui.curDesktop()
    return curDesktop.paneTabOfType(hou.paneTabType.SceneViewer)


def captureViewport(file=None, frame=None, size=(200, 200)):
    sv = sceneViewer()
    fbs: hou.FlipbookSettings = sv.flipbookSettings().stash()
    # use current frame if not specified
    frame = frame if frame is not None else hou.frame()
    fbs.frameRange((frame, frame))

    # output to mplay if file is not specified
    if not file:
        fbs.outputToMPlay(True)
    else:
        fbs.outputToMPlay(False)
        fbs.output(file)

    fbs.resolution(size)
    fbs.useResolution(True)

    # run flipbook on current viewport
    sv.flipbook(settings=fbs, open_dialog=False)


def getTempFilePath(ext=None, tempdir=None):
    tempdir = tempdir or tempfile.gettempdir()
    gen = tempfile._get_candidate_names()
    candidate = next(gen)

    def filepath(name):
        return os.path.join(tempdir, name + '.' + ext if ext else name)

    while os.path.isfile(filepath(candidate)):
        candidate = next(gen)

    return filepath(candidate)
