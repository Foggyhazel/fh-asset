from enum import Enum
import typing
from os import path as opath
from . import houhelper
from .asset import AssetDef


class PayloadType(Enum):
    NetworkItems = 0
    Debug = 1


class Payload(typing.TypedDict):
    type: PayloadType
    data: typing.Any


def formatNetworkAssetType(child_type: str):
    return 'network/%s' % child_type


def determineAssetTypeFromPayload(payload: Payload) -> str:
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


def processCreateAssetPayload(payload: Payload, asset_def: AssetDef) -> str:
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
