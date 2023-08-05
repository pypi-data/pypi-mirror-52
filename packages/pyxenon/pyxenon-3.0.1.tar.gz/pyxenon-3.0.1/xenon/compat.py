"""
Define cross-platform methods.
"""

from pathlib import Path
import logging
import subprocess
import os
import sys
import site
import signal

from .create_keys import create_self_signed_cert
from .version import xenon_grpc_version


def find_xenon_grpc_jar():
    """Find the Xenon-GRPC jar-file, windows version."""
    prefix = Path(sys.prefix)
    user_prefix = Path(site.USER_BASE)

    locations = [
        prefix / 'lib',
        prefix / 'local' / 'lib',
        user_prefix / 'lib',
        user_prefix / 'local' / 'lib',
    ]

    for location in locations:
        jar_file = location / 'xenon-grpc-{}.jar'.format(
                xenon_grpc_version)

        if not jar_file.exists():
            continue
        else:
            return str(jar_file)

    return None


def kill_process(process):
    """Kill the process group associated with the given process. (posix)"""
    logger = logging.getLogger('xenon')
    logger.info('Terminating Xenon-GRPC server.')
    os.kill(process.pid, signal.SIGINT)
    process.wait()


def start_xenon_server(port=50051, disable_tls=False):
    """Start the server."""
    jar_file = find_xenon_grpc_jar()
    if not jar_file:
        raise RuntimeError("Could not find 'xenon-grpc' jar file.")

    cmd = ['java', '-jar', jar_file, '-p', str(port)]

    if not disable_tls:
        crt_file, key_file = create_self_signed_cert()

        cmd.extend([
            '--server-cert-chain', str(crt_file),
            '--server-private-key', str(key_file),
            '--client-cert-chain', str(crt_file)])
    else:
        crt_file = key_file = None

    process = subprocess.Popen(
        cmd,
        bufsize=1,
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    return process, crt_file, key_file
