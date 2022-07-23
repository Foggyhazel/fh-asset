from enum import Enum
import typing
try:
    from typing import TypedDict
except ImportError:
    from .typing_extensions import TypedDict
from os import path as opath
from . import houhelper
from .asset import AssetDef


class PayloadType(Enum):
    NetworkItems = 0


class Payload(TypedDict):
    type: PayloadType
    data: typing.Any


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
    else:
        raise Exception('Unknown payload type %s' % t)
