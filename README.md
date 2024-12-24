# pyremoteenv

---
`pyremoteenv` is a Python package that allows you to configure your application with environment variables loaded from a remote registry.

Currently, the supported backend is ZooKeeper, but it's easy to extend to support other backends.

---
## Installation

Install `pyremoteenv` using pip:

```bash
pip install pyremoteenv
```

The only supported backend is ZooKeeper. Install dependencies for it 
```bash
pip install pyremoteenv[zk]
```

---

## Requirements

- Python 3.9+
- [kazoo](https://kazoo.readthedocs.io/en/latest/) - For ZooKeeper support.

---

## Usage

```python
import os
import remoteenv

remote_env = remoteenv.Env('zk')
with remote_env:

     # Write to remote config
     remote_env.set('TEST', 'test')

     # Read from remote config and set environment variables
     remote_env.read_to_os()
     print(os.environ['TEST'])

     # Read from remote config and write to django-environ
     remote_env.read_to_file(file=buffer)
     environ.Env.read_env(buffer, overwrite=True)

     remote_env.delete('TEST')
     
     # Use znodes tree to find custom or default variable from remote config
     remote_env.get('DATABASE_HOST')
     remote_env.get('service_1/host_4/DATABASE_HOST')
     remote_env.read_to_os('service_1', 'service_1/host_4')
```

More examples can be found in the [examples](https://github.com/Romamo/pyremoteenv/tree/main/examples).

---

## TODO

- More backends: plain text, json, firebase
- Watching mechanism to interact or inject new values immediately on change

---

## Contributing

Contributions are welcome! If you'd like to enhance the functionality or fix issues, kindly follow these steps:

1. Fork the repository on GitHub.
2. Clone your fork:
   ```bash
   git clone https://github.com/Romamo/pyremoteenv.git
   ```
3. Make your changes and test them.
4. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Romamo/pyremoteenv/blob/main/LICENSE) file for more details.

---

## Support

If you encounter any issues or have questions, feel free to open an issue on the [GitHub Issues Page](https://github.com/username/pyremoteenv/issues).

Happy coding! 🚀