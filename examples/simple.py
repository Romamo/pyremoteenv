import os
import remoteenv

remote_env = remoteenv.Env('zk')
try:
    with remote_env:

        # Write to remote config
        remote_env.set('TEST', 'test')

        # Read from remote config and set environment variables
        remote_env.read_to_os()
        print(os.environ['TEST'])

        remote_env.delete('TEST')
except remoteenv.exceptions.CannotStartBackend:
    print("Cannot use remote env")
