from importlib import import_module

from .base import BackendBase

BACKEND_REGISTRY = {
    'zk': 'remoteenv.backends.zk.ZooBackend',
}

def create_backend(backend_identifier: str, settings: dict = None) -> BackendBase:
    """
    Creates a backend instance from either a direct path or a shortcut.

    Args:
        backend_identifier (str): Either:
            - Fully qualified class path (e.g., 'remoteenv.backends.zk.ZooBackend')
            - A shortcut key registered in BACKEND_REGISTRY (e.g., 'zk')
        settings (dict): Optional settings to configure the backend.

    Returns:
        object: An instance of the specified backend.

    Raises:
        ValueError: If the path or shortcut is invalid.
    """
    try:
        # Resolve shortcut to a full backend path if necessary
        if backend_identifier in BACKEND_REGISTRY:
            backend_path = BACKEND_REGISTRY[backend_identifier]
        else:
            backend_path = backend_identifier  # Assume it's a full path

        # Split the backend path into module and class name
        module_path, class_name = backend_path.rsplit('.', 1)

        # Dynamically import the module
        module = import_module(module_path)

        # Get the backend class from the module
        backend_class = getattr(module, class_name)

        # Instantiate and return the backend
        return backend_class(**(settings or {}))
    except (ImportError, AttributeError, ValueError) as e:
        raise ValueError(f'Failed to create backend \'{backend_identifier}\': {e}')


__all__ = ['create_backend', 'BackendBase']
