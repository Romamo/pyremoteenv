from abc import ABC, abstractmethod

class BackendBase(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def dump(self) -> list[tuple[str, str]]:
        pass

    @abstractmethod
    def set(self, path: str, value: str):
        pass

    @abstractmethod
    def set_many(self, pairs: list[tuple[str, str]], delete_others=True):
        pass

    @abstractmethod
    def get(self, path: str, default: str = None) -> str:
        pass

    @abstractmethod
    def get_many(self, *paths: str, default: str = None) -> list[tuple[str, str]]:
        pass

    @abstractmethod
    def delete(self, path: str, recursive: bool = False):
        pass

    @abstractmethod
    def delete_many(self, *paths: str, exclude_paths: list[str] = None):
        pass
