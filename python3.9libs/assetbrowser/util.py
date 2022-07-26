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


def copyFile(src_file: str, target_dir: str, new_name=None):

    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)

    if new_name:
        _, ext = os.path.splitext(src_file)
        target_file = os.path.join(target_dir, new_name + ext)
    else:
        target_file = os.path.join(target_dir, os.path.basename(src_file))

    shutil.copy2(src_file, target_file)
    return target_file
