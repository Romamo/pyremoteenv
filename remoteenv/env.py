from remoteenv.backends import BackendBase, create_backend


class Env:
    _backend: BackendBase

    def __init__(self, backend: str, settings: dict = None):
        self._backend = create_backend(backend, settings)

    def __enter__(self):
        self._backend.start()
        return self

    def __exit__(self, *args):
        self._backend.stop()

    def dump(self) -> list[tuple[str, str]]:
        return self._backend.dump()

    def set(self, key: str, value: str):
        return self._backend.set(key, value)

    def set_many(self, pairs: list[tuple[str, str]]=None):
        return self._backend.set_many(pairs)

    def get(self, path: str) -> str:
        return self._backend.get(path)

    def get_many(self, *paths: str) -> list[tuple[str, str]]:
        return self._backend.get_many(*paths)

    def delete(self, path: str, recursive: bool = False):
        return self._backend.delete(path, recursive=recursive)

    def delete_many(self, *paths: str, exclude_paths: list[str] = None):
        return self._backend.delete_many(*paths, exclude_paths=exclude_paths)
