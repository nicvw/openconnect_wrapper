"""Wrapper script for managing openconnect CLI client."""
import errno
import os
from signal import SIGKILL
from subprocess import call

import click
import psutil


class NoPidError(Exception):
    """Error type."""
    pass


class ExecutableNotFound(Exception):
    def __init__(self, msg):
        super(ExecutableNotFound, self).__init__("'{}' not found in path".format(msg))


def __work_dir():
    return os.path.join(os.getenv('HOME'), '.openconnect')


def __pid_file():
    return os.path.join(__work_dir(), 'openconnect.pid')


def __mkdir_p(path):
    try:
        os.mkdir(path)
    except OSError as err:
        if errno.EEXIST == err.errno:
            pass
        else:
            raise


def __get_pid():
    pid = None
    try:
        with open(__pid_file(), 'r') as pidfile:
            pid = int(pidfile.read())
    except IOError as err:
        if err.errno != errno.ENOENT:
            raise
    if pid is None:
        raise NoPidError
    return pid


def __is_running():
    try:
        pid = __get_pid()
    except NoPidError:
        return False
    return psutil.pid_exists(pid)


def __find_executable(executable):
    for path in os.getenv('PATH').split(':'):
        if os.path.isdir(path) and executable in os.listdir(path):
            return os.path.join(path, executable)
    raise ExecutableNotFound(executable)


@click.group()
def cli():
    """Entry point for CLI execution."""
    pass


@cli.command(context_settings=dict(ignore_unknown_options=True,))
@click.argument('openconnect_args', nargs=-1, type=click.UNPROCESSED)
def start(openconnect_args=None):
    """Connect to an OpenVPN supported endpoint."""
    if __is_running():
        click.echo('vpn: already connected')
        return

    __mkdir_p(__work_dir())
    try:
        command = [
            __find_executable('sudo'),
            __find_executable('openconnect'),
            '--setuid={}'.format(os.getlogin()),
            '--background',
            '--pid-file={}'.format(__pid_file()),
            '--quiet'
        ]
    except ExecutableNotFound as err:
        click.echo(str(err))
        exit(1)

    if openconnect_args is not None:
        command += list(openconnect_args)
    if call(command) == 0:
        click.echo('vpn: started')


@cli.command()
def stop():
    """Disconnect the VPN."""
    try:
        pid = __get_pid()
        psutil.Process(pid).send_signal(SIGKILL)
    except (psutil.NoSuchProcess, NoPidError):
        click.echo("vpn: was not running")
    else:
        click.echo("vpn: stopped")


@cli.command()
def status():
    """Is the VPN running."""
    if __is_running():
        click.echo("vpn: online")
    else:
        click.echo("vpn: offline")


if __name__ == '__main__':
    cli()
