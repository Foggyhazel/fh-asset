from genericpath import isfile
from os import path as opath
import os
from pkg_resources import resource_filename
from . import config
from . import pkg_name
import logging
import json
import typing
from . import shimhou as hou
import string
import re
from functools import total_ordering


def resourcePath(relpath):
    return resource_filename(pkg_name, relpath)


def isAssetFolder(absolute_path):
    """
    A folder is considered an asset when it contains `asset_file`
    """
    return opath.isdir(absolute_path) and opath.isfile(_getAssetFilePath(absolute_path))


def _getAssetFilePath(asset_path):
    return opath.join(asset_path, config.asset_file)


def _writeJson(file_path, data):
    file_dir = opath.dirname(file_path)
    if not opath.isdir(file_dir):
        os.makedirs(file_dir)
    with open(file_path, 'w+') as f:
        json.dump(data, f, indent=2)


def _readJson(file_path):
    with open(file_path, 'r') as info_file:
        try:
            return json.load(info_file)
        except:
            # logging.warning('Invalid asset json: %s' % opath.normpath(asset_file))
            return {}


def createNodeAsset(items, path):
    if len(items) == 0 or not path:
        return
    first_item = hou.item(items[0])

    if not first_item:
        logging.warning('Cannot find item %s' % items[0])

    parent = first_item.parent()
    cat_name = parent.childTypeCategory().name()

    print(cat_name, path, items)


class Ref:
    def __init__(self, rel_asset_folder, rel_def_folder=None):
        """create new asset/asset path reference

        Args:
            rel_asset_folder (str): asset folder path relative to root directory
            rel_def_folder (str | None): asset definition path relative to asset folder. If none, this ref refer to asset
        """
        ra = rel_asset_folder.strip()
        rb = None

        if rel_def_folder is not None:
            rb = rel_def_folder.strip()
            if not rb:
                raise Exception('Asset def folder cannot be empty string')

        if not ra:
            raise Exception('Asset folder cannot be empty')
        self.asset_folder = ra
        self.def_folder = rb

    @staticmethod
    def fromAbsPath(abs_asset_folder):
        """Create Ref from absolute asset folder path

        Args:
            abs_asset_folder (_type_): absolute asset folder path
        """
        relpath = opath.relpath(abs_asset_folder, config.root_path)
        return Ref(relpath)

    def toDef(self, rel_def_folder):
        """Create new ref pointing to asset def of current asset

        Args:
            rel_def_folder (str): relative asset folder

        Raises:
            Exception: def folder is None

        Returns:
            Ref: def ref
        """
        if rel_def_folder is None:
            raise Exception("def folder cannot be None")

        return Ref(self.asset_folder, rel_def_folder)

    def absAssetFile(self):
        """Get absolute path to the asset json file

        Returns:
            str: absolute path to the asset json file
        """
        return opath.join(config.root_path, self.asset_folder, config.asset_file)

    def absAssetDir(self):
        return opath.join(config.root_path, self.asset_folder)

    def absDefFile(self):
        """Get absolute path to asset def json file. None if not set as asset def ref

        Returns:
            str | None: path or None
        """
        if not self.isAssetDef():
            raise Exception('Asset def folder not set.')

        return opath.join(config.root_path, self.asset_folder, self.def_folder, config.asset_def_file)

    def absDefDir(self):
        if not self.isAssetDef():
            raise Exception('Asset def folder not set.')
        return opath.join(config.root_path, self.asset_folder, self.def_folder)

    def isAssetDef(self):
        """Is this ref point to asset definition

        Returns:
            bool: true if this ref has asset def path
        """
        return bool(self.def_folder)

    def exist(self):
        """Check if asset/asset def json file already exist

        Returns:
            bool: True if exist
        """
        if self.isAssetDef():
            return opath.isfile(self.absDefFile())
        else:
            return opath.isfile(self.absAssetFile())

    def existAsset(self):
        return opath.isfile(self.absAssetFile())

    def existDef(self):
        return opath.isfile(self.absDefFile())

    def getAsset(self):
        """Get asset referenced by this ref, no matter if this is asset ref or def ref

        Returns:
            Asset: asset
        """
        if not self.existAsset():
            return None

        path = self.absAssetFile()
        data = _readJson(path)
        return Asset(self, data)

    def getDef(self):
        if not self.isAssetDef() or not self.exist():
            return None

        path = self.absDefFile()
        data = _readJson(path)
        return AssetDef(self, data)


class Asset:
    @staticmethod
    def toAssetName(name):
        return re.sub("[^0-9a-zA-Z]+", "_", name)

    def __init__(self, ref, data=None):
        self._ref = ref
        self._fillFromData(data)
        self._sortedVersions = None

    def ref(self):
        return self._ref

    def _fillFromData(self, data=None):
        """
        parse json data
        ```ts
        {
            _schemaVersion: number,
            id: string, // autogen uuid
            title: string,
            tags: string[],
            assetType: string,
            resolves: {
                [version: string]: string // rel path pointing to asset definition 
            }
        }
        ```
        """
        if not data:
            self._id = None
            self._title = None
            self._tags = []
            self._assetType = None
            self._resolves = {}
        else:
            if not '_schemaVersion' in data:
                logging.warning('Missing schema version in %s got %s' %
                                (self.ref().absAssetFile(), data))
            elif data['_schemaVersion'] != self.schemaVersion():
                logging.warning('Schema version mismatched. Expected %d but got %d'
                                % (self.schemaVersion(), data['_schemaVersion']))
            self._id = data.get('id')
            self._title = data.get('title')
            self._tags = ensureTagList(data.get('tags', []))
            self._assetType = data.get('assetType')
            res = data.get('resolves', {})
            newres = {}
            for k, v in res.items():
                try:
                    ver = str(Version(k))
                    newres[ver] = str(v)
                except ValueError:
                    continue
            self._resolves = newres

    @staticmethod
    def schemaVersion():
        return 1

    def data(self):
        """
        return data dict to be serialized and saved
        """
        return {
            '_schemaVersion': self.schemaVersion(),
            'id': self.id(),
            'title': self.title(),
            'tags': self.tags(),
            'assetType': self.assetType(),
            'resolves': self._resolves
        }

    def setData(self,
                type=None,
                title=None,
                tags=None):

        if type:
            self._assetType = type
        if title:
            self._title = title
        if tags:
            self._tags = tags

    def assetType(self):
        return self._assetType

    def id(self):
        return self._id

    def title(self):
        return self._title

    def tags(self):
        return self._tags

    def versions(self):
        return tuple(self._resolves.keys())

    def resolveVersion(self, version_label):
        version_path = self._resolves.get(version_label, None)
        if not version_path:
            return None

        return self._ref.toDef(version_path)

    def resolveLatestVersion(self):
        return self.resolveVersion(self.latestVersion())

    def sortedVersions(self):
        if self._sortedVersions is None:
            versions = list(self.versions())
            versions.sort(key=Version)
            self._sortedVersions = versions
        return self._sortedVersions

    def latestVersion(self):
        versions = self.sortedVersions()
        if not len(versions):
            return None
        return versions[-1]

    def setOrAddVersion(self, version, path):
        self._resolves[version] = path

    def __str__(self):
        return json.dumps(self.data(), indent=2)


class AssetDef:
    def __init__(self, ref, data=None):
        self._ref = ref
        self._fillFromData(data)

    def ref(self):
        return self._ref

    def _fillFromData(self, data=None):
        """
        parse json data
        ```ts
        {
            _schemaVersion: number,
            id: string, // asset unit id for tracking issues,
            author: string,
            description: string,
            createdOn: number,
            updatedOn: number,
            content: string, // file path, vex snippet, ramp etc
            changes: string
        }
        ```
        """
        if not data:
            self._id = None
            self._author = None
            self._description = ''
            self._createdOn = None
            self._updatedOn = None
            self._content = None
            self._changes = None
        else:
            if not '_schemaVersion' in data:
                logging.warning('Missing schema version in %s got asset def %s' % (
                    self.ref().absDefFile(), data))
            elif data['_schemaVersion'] != self.schemaVersion():
                logging.warning('Schema version mismatched. Expected %d but got %d'
                                % (self.schemaVersion(), data['_schemaVersion']))
            self._id = data.get('id')
            self._author = data.get('author')
            self._description = data.get('description')
            self._createdOn = data.get('createdOn')
            self._updatedOn = data.get('updatedOn')
            self._content = data.get('content')
            self._changes = data.get('changes')

    def setData(self, author=None, description=None, createdOn=None, updatedOn=None, content=None, changes=None):
        if author:
            self._author = author
        if description:
            self._description = description
        if createdOn:
            self._createdOn = createdOn
        if updatedOn:
            self._updatedOn = updatedOn
        if content:
            self._content = content
        if changes:
            self._changes = changes

    @staticmethod
    def schemaVersion():
        return 1

    def id(self):
        return self._id

    def author(self):
        return self._author

    def description(self):
        return self._description

    def createdOn(self):
        return self._createdOn

    def updatedOn(self):
        return self._updatedOn

    def content(self):
        return self._content

    def changes(self):
        return self._changes

    def data(self):
        return {
            '_schemaVersion': self.schemaVersion(),
            'id': self._id,
            'author': self._author,
            'description': self._description,
            'createdOn': self._createdOn,
            'updatedOn': self._updatedOn,
            'content': self._content,
            'changes': self._changes
        }

    def __str__(self):
        return json.dumps(self.data(), indent=2)

    def getThumbnail(self):
        """Try to find thumbnail image by searching for [thumbnail].* file
        with certain extensions

        Returns:
            typing.Union[str, None]: absolute thumbnail file path
        """
        return findThumbnail(self.ref())


def getAsset(abs_asset_folder):
    ref = Ref.fromAbsPath(abs_asset_folder)
    return ref.getAsset()


def setAsset(asset):
    _writeJson(asset.ref().absAssetFile(), asset.data())


def getDef(asset, rel_def_folder):
    ref = asset.ref().toDef(rel_def_folder)
    return ref.getDef()


def setDef(assetDef):
    _writeJson(assetDef.ref().absDefFile(), assetDef.data())


valid_chars = ".%s%s" % (string.ascii_letters, string.digits)


def cleanVersionString(version):
    return ''.join(c for c in version if c in valid_chars)


def findThumbnail(defRef):
    """Try to find thumbnail image by searching for [thumbnail].* file
    with certain extensions

    Returns:
        typing.Union[str, None]: absolute thumbnail file path
    """

    if not defRef.isAssetDef():
        raise ValueError(
            'find thumbnail need a ref pointing to an asset definition')

    thumbname = config.thumbnail_filename
    defdir = defRef.absDefDir()
    if not defdir:
        raise Exception('Cannot find thumbnail: asset def path is empty')
    thumbpath = None
    for ext in ['.jpg', '.png']:
        f = opath.join(defdir, thumbname + ext)
        if os.path.isfile(f):
            thumbpath = f
            break
    return thumbpath


@total_ordering
class Version:
    version_re = re.compile(r'^(\d+) \. (\d+)$',
                            re.VERBOSE | re.ASCII)

    def __init__(self, *args):
        self.version = tuple()
        if len(args) == 1:
            self.parse(str(args[0]))
        elif len(args) == 2:
            self.version = (int(args[0]), int(args[1]))
        else:
            raise Exception(
                'invalid argument to construct Version %s' % str(args))

    def parse(self, version):
        match = self.version_re.match(version)

        if not match:
            raise ValueError("invalid version number '%s'" % version)

        (major, minor) = match.group(1, 2)
        self.version = tuple(map(int, [major, minor]))

    def __str__(self):
        return '%s.%s' % self.version

    def __eq__(self, other):
        if isinstance(other, str):
            other = Version(other)
        return self.version == other.version

    def __lt__(self, other):
        if isinstance(other, str):
            other = Version(other)
        return self.version < other.version


def splitTags(text):
    return [s for s in re.split(r'\W+', text) if s]


def ensureTagList(input):
    if not isinstance(input, list):
        return splitTags(str(input))
    else:
        return input
