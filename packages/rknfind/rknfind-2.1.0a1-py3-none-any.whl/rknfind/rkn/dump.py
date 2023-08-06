from abc import ABC, abstractmethod

from appdirs import AppDirs
from pathlib import Path

from rknfind.app import dirs


class DumpFileProvider(ABC):
    @property
    @abstractmethod
    def last_update(self):
        """Fetch datetime of last update of Rkn dump file.

        Returns
        -------
        datetime
            Datetime object representing last update date of the Rkn dump file.
        """

    @property
    @abstractmethod
    def url(self):
        """URL of the remote source of the dump file.

        Returns
        -------
        str
            URL of where Rkn dump file has been retrieved from.
        """

    @property
    @abstractmethod
    def file_path(self):
        """Path to the Rkn dump file.

        Returns
        -------
        Path
            Location of the Rkn dump file.
        """

    @abstractmethod
    def sync(self, *args, **kwargs):
        """Synchronize Rkn dump file with its remote source."""

    @abstractmethod
    def cleanup(self):
        """Cleanup Rkn dump file location."""


class GitProvider(DumpFileProvider):
    def __init__(self, url):
        """Initialize a new GitProvider.

        Parameters
        ----------
        url : str
            URL to clone Rkn dump repository from.
        """

        self.url = url
        self._git_workdir = Path(dirs.user_cache_dir, 'rknfind', 'rkndump')

    def last_update(self):
        from git import Repo
        path = Path(self._git_workdir)
        return Repo(path).head.commit.authored_datetime

    def url(self):
        return url

    def sync(self, *args, **kwargs):
        from git import Repo, InvalidGitRepositoryError
        import shutil

        path = Path(self._git_workdir)
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            repo = Repo.clone_from(
                self.url, self._git_workdir, *args, **kwargs)
        else:
            try:
                repo = Repo(path)
            except InvalidGitRepositoryError:
                shutil.rmtree(self._git_workdir)
                repo = Repo(path)
            repo.remotes.origin.fetch(*args, **kwargs)

    def file_path(self):
        return Path(self._git_workdir, 'dump.csv')

    def cleanup(self):
        import shutil
        shutil.rmtree(self._git_workdir)


class SimpleFileProvider(DumpFileProvider):
    def __init__(self, url):
        """Initialize a new SimpleFileProvider.

        Parameters
        ----------
        url : str
            URL to retrieve Rkn dump file from.
        """

        self.url = url
        self._dump_dir = Path(dirs.user_cache_dir, 'rknfind', 'rkndump')

    def last_update(self):
        from datetime import datetime
        fd = open(self.file_path(), 'r', encoding='windows-1251')
        dateline = fd.readline().strip()
        fd.close()
        return datetime.strptime(dateline, 'Updated: %Y-%m-%d %H:%M:%S %z')

    def url(self):
        return url

    def sync(self, *args, **kwargs):
        import os
        import requests

        path = Path(self.file_path())
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
        else:
            os.unlink(path)
        response = requests.get(self.url)

        fd = open(path, 'wb')
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                fd.write(chunk)
                fd.flush()
        fd.close()

    def file_path(self):
        return Path(self._dump_dir, 'dump.csv')

    def cleanup(self):
        import shutil
        shutil.rmtree(self._dump_dir)
