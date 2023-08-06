from abc import ABC, abstractmethod
from contextlib import contextmanager


class AbstractStore(ABC):
    """
    Interface for data stores.  Allows reading and writing file-like object by
    path.
    """

    @abstractmethod
    @contextmanager
    def open(self, path, mode, *args, **kwargs):
        """Context manager that provides a handle to a file-like object.
        Attempts to mimic the ``open`` built-in as much as possible.

        :param path: The (relative) location of the file backing the stream.
        :param mode: The open mode of for the file.

        :returns: A file-like object.
        """
        pass

    @contextmanager
    def read(self, path, mode="", **kwargs):
        with self.open(path, "r" + mode, **kwargs) as handle:
            yield handle

    @contextmanager
    def write(self, path, mode="", **kwargs):
        with self.open(path, "w" + mode, **kwargs) as handle:
            yield handle

    @abstractmethod
    def substore(self, path):
        pass
