from .base import BackendBase

try:
    import kazoo
except ImportError:
    kazoo = None

from kazoo.client import KazooClient
import kazoo.exceptions
from kazoo.handlers.threading import KazooTimeoutError

class ZooBackend(BackendBase):
    def __init__(self, prefix, hosts):
        if not kazoo:
            raise RuntimeError(
                "The 'kazoo' library is required to use ZooBackend. Install it with 'pip install kazoo'.")

        self._prefix = prefix
        self._zk = KazooClient(hosts=hosts)

    def __enter__(self):
        """Enter the runtime context and start the Kazoo client."""
        if not self.start():
            raise RuntimeError("Failed to start ZooKeeper client")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the runtime context and stop the Kazoo client."""
        self.stop()

    def start(self) -> bool:
        if not self._zk.connected:
            try:
                self._zk.start()
            except KazooTimeoutError:
                return False
        return True

    def stop(self):
        if self._zk.connected:
            self._zk.stop()

    def _create_path(self, *path: str):
        if path:
            return f"/{self._prefix}/{'/'.join(path)}"
        return f"/{self._prefix}"
    
    def dump(self) -> list[tuple[str, str]]:
        # recursively dump all nodes
        def dump_node(fullpath) -> list[tuple[str, str]]:
            try:
                children = self._zk.get_children(fullpath)
            except kazoo.exceptions.NoNodeError:
                return
            for child in children:
                data, stat = self._zk.get(f"{fullpath}/{child}")
                if data != b'':
                    if fullpath == f"/{self._prefix}":
                        # print(f"{child}={data.decode()}, {stat.version}, {stat.numChildren} -> {path[2 + len(self._prefix):]}/{child} [{len(path)}")
                        yield child, data.decode()
                    else:
                        # print(f"{path}/{child}={data.decode()}, {stat.version}, {stat.numChildren} -> {path[2+len(self._prefix):]}/{child} [{len(path)}")
                        yield f"{fullpath[2+len(self._prefix):]}/{child}", data.decode()
                for t in dump_node(f"{fullpath}/{child}"):
                    yield t

        for k ,v in dump_node(self._create_path()):
            yield k, v

    def bulk_delete(self, exclude: list[str] = None):
        for k, v in self.dump():
            if k not in exclude:
                # print(f"delete {k}")
                self._zk.delete(self._create_path(k), recursive=True)

    def set(self, path: str, value: str):
        fullpath = self._create_path(path)

        try:
            current, stat = self._zk.get(fullpath)
            if current.decode() != value:
                self._zk.set(fullpath, value.encode())
        except kazoo.exceptions.NoNodeError:
            self._zk.create(fullpath, value.encode(), makepath=True)


    def set_many(self, pairs: list[tuple[str, str]]=None):
        for k, v in pairs:
            # print(f"{k}={v}")
            self.set(k, v)

    def get(self, path: str, default: str = None) -> str:
        try:
            data, stat = self._zk.get(self._create_path(path))
        except kazoo.exceptions.NoNodeError:
            return default
        return data.decode()

    @staticmethod
    def _iterate(paths) -> tuple[str, bool]:
        yield '', True
        for p in paths:
            if p.endswith('*'):
                yield p[:-1], True
            else:
                yield p, False

    def get_many(self, *paths: str, default: str = None) -> list[tuple[str, str]]:
        for path, with_children in self._iterate(paths):
            # print(path, with_children)
            if with_children:
                try:
                    children = self._zk.get_children(self._create_path(path))
                except kazoo.exceptions.NoNodeError:
                    continue
                for child in children:
                    data, stat = self._zk.get(self._create_path(path, child))
                    if data != b'':
                        # print(f"{path}: {child}={data.decode()}")
                        yield child, data.decode()
            else:
                yield path.split('/')[-1], self.get(path, default)

    def delete(self, path: str, recursive=False):
        self._zk.delete(self._create_path(path), recursive=recursive)

    def delete_many(self, *paths: str, exclude_paths: list[str] = None):
        if paths:
            for path in paths:
                self.delete(path)
                
        if exclude_paths:
            for k, v in self.dump():
                if k not in exclude_paths:
                    # print(f"delete {k}")
                    self.delete(k, recursive=True)
                    
