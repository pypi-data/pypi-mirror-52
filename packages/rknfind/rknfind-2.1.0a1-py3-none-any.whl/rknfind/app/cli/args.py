from rknfind.app.i18n import tl
from rknfind.app import distrib
from argparse import ArgumentParser, ArgumentTypeError
from pathlib import Path


def gt(t, gt):
    """Argparse argument value check function.

    Parameters
    ----------
    type : callable
        Callable to convert argparse argument value.
    gt : object
        Object to compare value using >

    Returns
    -------
    function
        Argparse argument type adapter function.
    """

    def checkfun(s):
        if not t(s) > gt:
            raise ArgumentTypeError(
                tl('expected {type} greater than {gt}')
                .format(gt=gt, type=t.__name__))
    return checkfun


# ArgParse init
_parser = ArgumentParser(prog=distrib.project_name)


# $ rknfind dump
_options = _parser.add_argument_group(tl('options'))
_options.add_argument('-f', '--filter', nargs=2,
                      type=str, action='append', default=[],
                      metavar=(tl('FIELD'), tl('OCCURENCE')),
                      help=tl('Accept entry only if '
                              'OCCURENCE matches FIELD'))
_options.add_argument('-l', '--limit', type=gt(int, 0),
                      metavar=tl('AMOUNT'),
                      help=tl('Limit search results '
                              'by AMOUNT of entries'))
_options.add_argument('-o', '--offset', type=gt(int, 0),
                      metavar=tl('OFFSET'),
                      help=tl('Skip first OFFSET entries'))
_options.add_argument('-e', '--export', type=Path,
                      metavar=tl('PATH'),
                      help=tl('SQLite database file to '
                              'export results to'))

_flags = _parser.add_argument_group(tl('flags'))
_flags_exg = _flags.add_mutually_exclusive_group()
_flags.add_argument('-j', '--json', action='store_true',
                    help=tl('Print output in JSON format'))
# Can't allow both glob and RegExp - make them mutually exclusive
_flags_exg.add_argument('-g', '--glob', action='store_true',
                        help=tl('Consider search OCCURENCEs '
                                'glob expressions'))
_flags_exg.add_argument('-r', '--regexp', action='store_true',
                        help=tl('Consider search OCCURENCEs regular '
                                'expressions'))


def get_args():
    return _parser.parse_args()
