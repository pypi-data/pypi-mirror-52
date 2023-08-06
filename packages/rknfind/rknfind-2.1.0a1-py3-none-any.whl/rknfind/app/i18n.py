import gettext
from rknfind.app import pkgdir
from pathlib import Path

gettext.bindtextdomain('rknfind', Path(pkgdir, 'i18n'))
gettext.textdomain('rknfind')
tl = gettext.gettext
