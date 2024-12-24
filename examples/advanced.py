import remoteenv

"""
How to use tree of znodes to set variables

Let's say your microservices have to use different database host.
First, set the default value:
    DATABASE_HOST=h1 

Set value for service_1:  
    service_1/DATABASE_HOST=h2

Set value for all services run on host_4:  
    host_4/DATABASE_HOST=h3

Set value for service_1 run on host_4:  
    service_1/host_4/DATABASE_HOST=h3

Read all variables set under each node starting from root
    variables_remote = remote_env.read_to_dict('service_1', 'host_4', 'service_1/host_4', use_last_assignment=True)
    {'DATABASE_HOST': 'h1'}
"""

# Use text to set variables
s = """
DATABASE_HOST=h2
service_1/DATABASE_HOST=h3
service_1/host_4/DATABASE_HOST=h1
"""

def split_text(text: str) -> list[tuple[str, str]]:
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        yield tuple(line.split('=', 1))

variables = list(split_text(s))
remote_env = remoteenv.Env('zk')
with remote_env:
    # Set variables
    remote_env.set_many(variables)

    # Remove all others
    remote_env.delete_many(exclude_paths=[k[0] for k in variables])

    print("Dumping with paths...")
    for k, v in remote_env.dump():
        print(f"{k}={v}")

    print("Reading with path filters...")
    variables_remote = remote_env.read_to_dict('service_1', 'host_4', 'service_1/host_4')
    print(variables_remote)

    # Clear everything
    remote_env.delete_many()
    print("Dumping with paths...")
    for k, v in remote_env.dump():
        print(f"{k}={v}")
