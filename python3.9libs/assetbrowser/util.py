import shutil
import os
import tempfile


def getTempFilePath(ext=None, tempdir=None):
    tempdir = tempdir or tempfile.gettempdir()
    gen = tempfile._get_candidate_names()
    candidate = next(gen)

    def filepath(name):
        return os.path.join(tempdir, name + '.' + ext if ext else name)

    while os.path.isfile(filepath(candidate)):
        candidate = next(gen)

    return filepath(candidate)


def copyFile(src_file: str, target_file: str):
    target_dir = os.path.dirname()

    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)

    shutil.copy2(src_file, target_file)
