import hashlib
from distutils.version import LooseVersion
from glob import glob
from os import path

from scrapyd.config import Config


class FilesystemEggStorage(object):
    @staticmethod
    def list(project):
        eggdir = path.join(Config().get("eggs_dir"), project)
        versions = {path.splitext(path.basename(x))[0]: hashlib.md5(open(x, 'rb').read()).hexdigest() for x in
                    glob("%s/*.egg" % eggdir)}
        return [{"version": version, "checksum": versions[version]} for version in
                sorted(versions.keys(), key=LooseVersion)]
