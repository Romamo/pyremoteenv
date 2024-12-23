# pyremoteenv

`pyremoteenv` is a lightweight Python library designed for managing and distributing environment variables across microservices using remote configurations. This makes it ideal for cloud-native distributed systems where environment consistency and synchronization across services are critical.

---

## Features

- **Centralized Environment Management**: Seamlessly distribute environment variables to microservices via ZooKeeper or other remote backends.
- **Improved Consistency**: Ensure distributed services share consistent configuration without manual intervention.
- **Bulk Operations**: Manage multiple environment variables at once with simple APIs.
- **Pluggable Backend**: Currently supports ZooKeeper, with potential for adding new backends.
- **Error Resilience**: Handles common errors like missing nodes or network splits gracefully.

---

## TODO

- **More backends**: plain text, json, firebase
- **Watching mechanism** to interact or inject new values immediately

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

- Python 3.8+
- [kazoo](https://kazoo.readthedocs.io/en/latest/) - For ZooKeeper support.

---

## Usage

### **Example 1: Upload your config to remote storeage**

This demonstrates how to push environment variables for multiple services to ZooKeeper.

```python
from remoteenv import Env


# Example set of variables to distribute across services
# Add path prefixes to customize separated services by name, host, etc
s = """
DATABASE_DEFAULT_HOST=h2
service_1/DATABASE_DEFAULT_HOST=h3
service_1/host_4/DATABASE_DEFAULT_HOST=h1
"""

# Split the variables into key-value pairs
def split_text(text):
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        yield tuple(line.split('=', 1))

variables = list(split_text(s))

env = Env('zk', settings={'prefix': 'test', 'hosts': 'zookeeper:2181'})
with env:
    env.set_many(variables)
```

---

### **Example 2: Read all remote variables including path prefixes**

Retrieve and display all stored variables, including their paths.

```python
with env:
    for k, v in env.dump():
        print(f"{k}={v}")
```

---

### **Example 3: Read remote config**

```python
with env:
    print("Read using variable name...")
    path = 'DATABASE_DEFAULT_HOST'
    v = env.get(path)
    print(f"{path}={v}")  # Example: DATABASE_DEFAULT_HOST=h2

    print("Reading with path filters...")
    variables_remote = {}
    for k, v in env.get_many('service_1/*', 'host_4/*', 'service_1/host_4/*'):
        # Find the most suitable key 
        variables_remote[k] = v
    print(variables_remote)
```

---

## Documentation

Full documentation and advanced usage examples are available at the [GitHub repository](https://github.com/Romamo/pyremoteenv).

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