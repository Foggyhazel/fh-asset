import hou
from assetbrowser import model, houhelper, asset, createAsset
import logging
from urllib import parse


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
    node: hou.Node = pane.pwd()
    if not len(files):
        return

    item_to_load = files[0]

    p = parseAssetUrl(item_to_load)

    # drop on network view
    if (pane.type().name() == "NetworkEditor"):
        neteditor: hou.NetworkEditor = pane
        assetObj = asset.getAsset(p['file'])
        if not assetObj:
            logging.warning('Asset %s not found' % item_to_load)
            return
        # check network type
        if not isNetworkCompatible(assetObj, neteditor.pwd()):
            neteditor.flashMessage(None, 'Wrong network type', 1)
            return
        # clear selection
        node.setSelected(False, True)
        # load content from file
        houhelper.loadAsset(assetObj=assetObj, node=node,
                            version_label=p['version'])

        moveSelectedToPosition(node, neteditor.cursorPosition())


def isNetworkCompatible(assetObj: asset.Asset, parent_node: hou.Node):
    child_type = parent_node.childTypeCategory().name()
    expected_type = createAsset.formatNetworkAssetType(child_type)
    return expected_type == assetObj.assetType()


def moveSelectedToPosition(container: hou.node, position: hou.Vector2):
    items = container.selectedItems()
    nodes = container.selectedChildren()

    if len(nodes):
        # use root node to calculate move position
        root_node = hou.sortedNodes(nodes)[0]
        curr_pos = root_node.position()
    elif len(items):
        # no node places, only some network items
        # use first item for positioning
        curr_pos = items[0].position()
    else:
        return

    delta = position - curr_pos

    # move all items by delta
    # do not use move/setPosition successively
    # as that will move nodes inside network box twice
    allPos = [item.position() for item in items]
    for (i, item) in enumerate(items):
        item.setPosition(allPos[i] + delta)


def parseAssetUrl(url: str):
    p = parse.urlparse(url)
    q = parse.parse_qs(p.query)
    try:
        pos = url.index('?')
        asset_path = url[:pos]
    except:
        asset_path = url

    version = q.get('version', [None])[0]

    return {
        'file': asset_path,
        'version': version
    }
