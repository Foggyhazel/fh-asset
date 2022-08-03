from os import path as opath
from . import houhelper


def enum(**enums):
    return type('Enum', (), enums)


PayloadType = enum(NetworkItems=0, Debug=1)


def formatNetworkAssetType(child_type):
    return 'network/%s' % child_type


def determineAssetTypeFromPayload(payload):
    t = payload['type']
    if t == PayloadType.NetworkItems:
        # get type from network type
        try:
            first_node = payload['data'][0]
            network_type = houhelper.getNetworkType(first_node)
            return formatNetworkAssetType(network_type)
        except Exception as e:
            raise Exception(
                'Cannot determine network type of node "%s"' % first_node)

    elif t == PayloadType.Debug:
        # for debug
        return 'debug'
    else:
        raise Exception('Unsupported asset type %s' % t)


def processCreateAssetPayload(payload, asset_def):
    """process asset creation payload of any type

    Args:
        payload (Payload): payload
        asset_def (AssetDef): asset def owning this asset

    Raises:
        Exception: unknow payload type

    Returns:
        str: str to be store as content inside asset def json
    """
    t = payload['type']

    if t == PayloadType.NetworkItems:
        defdir = asset_def.ref().absDefDir()
        path = opath.join(defdir, 'content.netitems')
        houhelper.dumpNodeItemsToFile(payload['data'], path)
        return opath.relpath(path, defdir)
    elif t == PayloadType.Debug:
        print('asset created')
    else:
        raise Exception('Unknown payload type %s' % t)
