from pkg_resources import get_distribution, resource_filename
from appdirs import AppDirs
from pathlib import Path

distrib = get_distribution('rknfind')
dirs = AppDirs(appname=distrib.project_name, version=distrib.version)
pkgdir = Path(resource_filename('rknfind', ''))
