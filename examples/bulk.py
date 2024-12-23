from typing import Tuple, List

from remoteenv import Env


def split_text(text: str) -> List[Tuple[str, str]]:
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        yield tuple(line.split('=', 1))

# Set var DATABASE_DEFAULT_HOST variable of different paths suitable by different services
s = """
DATABASE_DEFAULT_HOST=h2
service_1/DATABASE_DEFAULT_HOST=h3
service_1/host_4/DATABASE_DEFAULT_HOST=h1
"""

variables = list(split_text(s))
env = Env('zk', settings={'prefix': 'test', 'hosts':'h4:2181'})
with env:
    # Set variables
    env.set_many(variables)
    # Remove all others
    env.delete_many(exclude_paths=[k[0] for k in variables])

    print("Dumping with paths...")
    for k, v in env.dump():
        print(f"{k}={v}")

    print("Read using name")
    path = 'DATABASE_DEFAULT_HOST'
    v = env.get(path)
    print(f"{path}={v}")

    print("Reading with path filters...")
    variables_remote = {}
    for k, v in env.get_many('service_1/host_4/DATABASE_DEFAULT_HOST', 'service_1/*', 'host_4/*',
                             'service_1/host_4/*'):
        variables_remote[k] = v
    print(variables_remote)

    # Clear everything
    env.delete_many()
    print("Dumping with paths...")
    for k, v in env.dump():
        print(f"{k}={v}")
