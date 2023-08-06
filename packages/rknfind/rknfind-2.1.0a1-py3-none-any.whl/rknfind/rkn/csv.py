from os import linesep as lsep

LIST_ELEMENT_SEPARATOR = ' | '


class RknBlockEntry(object):
    def __init__(self, addr, domain, url, issuer, decree, date):
        """Initialize new RknBlockEntry with its data.

        Parameters
        ----------
        addr : str
            String of IP-addresses, separated by LIST_ELEMENT_SEPARATOR.
        domain : str
            String of domains, separated by LIST_ELEMENT_SEPARATOR.
        url : str
            String of URLs, separated by LIST_ELEMENT_SEPARATOR.
        decree:
            String of block entry decree.
        date:
            String of DD-MM-YYYY formatted block entry date.
        """

        self.addr = addr
        self.decree = decree
        self.date = date
        self.issuer = issuer
        self.domain = domain
        self.url = url

        if type(addr) is str:
            self.addr = addr.split(LIST_ELEMENT_SEPARATOR)
        elif addr is None:
            self.addr = []

        if type(domain) is str:
            self.domain = domain.split(LIST_ELEMENT_SEPARATOR)
        elif domain is None:
            self.domain = []

        if type(url) is str:
            self.url = url.split(LIST_ELEMENT_SEPARATOR)
        elif url is None:
            self.url = []

    def __repr__(self):
        """Returns object representations as string.

        Returns
        ------
        str
            String representation of an object.
        """

        return (('RknBlockEntry(address={address!r}; domain={domains!r}; '
                 'url={url!r}; '
                 'issuer={issuer!r}; decree={decree!r}; date={date!r})')
                .format(address=self.addr, issuer=self.issuer,
                        decree=self.decree, date=self.date,
                        domains=self.domain, url=self.url))

    def __json__(self):
        """Returns object serialized in JSON.

        Returns
        ------
        str
            JSON-serialized object.
        """

        from json import dumps
        return(dumps({k: v for k, v in vars(self).items()
                      if not (k.startswith('_') or callable(v))}))

    def match(self, field, occurence, glob=False, regexp=False):
        """Matches entry's field against occurence.

        Parameters
        ----------
        field : str
            Field to match entry against. May be None, in this case any field
            will be used to match against.
        occurence : str
            Occurence to match in field.
        glob : bool
            Threat occurence as a glob expression if True.
            Cannot be True if regexp=True.
        regexp : bool
            Thread occurence as a regular expression if True.
            Cannot be True if glob=True.

        Returns
        -------
        bool
            True if entry is matching against occurence specified for field.
        """

        import re
        from fnmatch import fnmatch
        attrs = [
            attr for attr, value in vars(self).items()
            if not (attr.startswith('_') or callable(value))
        ]

        if glob and regexp:
            raise ValueError('glob and regexp are mutually exclusive')

        if field is not None:
            if field not in attrs:
                return False

            value = getattr(self, field)
            if not isinstance(value, list):
                value = repr(value)
                if glob:
                    return fnmatch(value, occurence)
                elif regexp:
                    return re.match(occurence, value)
                else:
                    return occurence in value
            else:
                for item in value:
                    item = repr(item)
                    if glob:
                        return fnmatch(item, occurence)
                    elif regexp:
                        return re.match(occurence, item)
                    else:
                        return occurence in item
        else:
            for attr in attrs:
                if self.match(attr, occurence, glob, regexp):
                    return True


def entries(fd, readbuf=1024):
    """Generator function to iterate over Rkn CSV dump file.

    Parameters
    ----------
    fd : TextIO
        File or file-like object to read from.
    readbuf : int
        File reading buffer.

    Yields
    ------
    RknBlockEntry
        Block entry read from Rkn dump file.
    """

    field_id = None
    in_field = False
    quoted = False

    while True:
        buffer = fd.read(readbuf)
        if not buffer:
            return

        for ch in buffer:
            if field_id is None:
                # Pre-populate entry values array
                entry = ['' for _ in range(6)]
                field_id = 0
                field = str()

            # Toggle field quoting
            if ch == '"':
                if not field or in_field:
                    in_field = not in_field

            if ch == ';' and not in_field:
                if len(field) > 0:
                    entry[field_id] = field
                else:
                    entry[field_id] = None
                field_id += 1
                field = str()
            elif ch == '\n' and not in_field:
                entry[field_id] = field
                field_id = None

                # Build RknBlockEntry from values array
                yield RknBlockEntry(*entry)
            else:
                field += ch
