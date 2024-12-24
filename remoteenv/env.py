import io
import os

from remoteenv.backends import BackendBase, create_backend
from remoteenv.exceptions import CannotStartBackend


class Env:
    _backend: BackendBase

    def __init__(self, backend: str, settings: dict = None):
        self._backend = create_backend(backend, settings)

    def __enter__(self):
        if not self._backend.start():
            raise CannotStartBackend
        return self

    def __exit__(self, *args):
        self._backend.stop()

    def dump(self) -> list[tuple[str, str]]:
        return self._backend.dump()

    def set(self, key: str, value: str):
        if not key:
            raise ValueError("Key cannot be an empty string.")
        if not value:
            raise ValueError("Value cannot be an empty string.")
        return self._backend.set(key, value)

    def set_many(self, pairs: list[tuple[str, str]]=None):
        return self._backend.set_many(pairs)

    def get(self, path: str, default: str = None) -> str:
        return self._backend.get(path)

    def get_many(self, *paths: str) -> list[tuple[str, str]]:
        return self._backend.get_many(*paths)

    def delete(self, path: str, recursive: bool = False):
        return self._backend.delete(path, recursive=recursive)

    def delete_many(self, *paths: str, exclude_paths: list[str] = None):
        return self._backend.delete_many(*paths, exclude_paths=exclude_paths)

    def read_to_dict(self, *paths: str, use_last_assignment=True) -> dict[str, str]:
        variables = {}
        for k, v in self.get_many(*paths):
            if use_last_assignment or k not in variables:
                variables[k] = v
        return variables

    def read_to_file(self, *paths: str, file: io.TextIOWrapper=None, use_last_assignment=True):
        variables = self.read_to_dict(*paths, use_last_assignment=use_last_assignment)

        text = "\n".join(f"{k}={v}" for k, v in variables.items())
        file.write(text)
        file.seek(0)

    def read_to_os(self, *paths: str, use_last_assignment=True):
        variables = self.read_to_dict(*paths, use_last_assignment=use_last_assignment)

        for k, v in variables.items():
            os.environ.setdefault(k, v)
