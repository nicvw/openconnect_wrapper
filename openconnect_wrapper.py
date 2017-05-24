"""Wrapper script for managing openconnect CLI client."""
import errno
import os
from signal import SIGKILL
from subprocess import call

import click
import psutil

WORK_DIR = os.path.join(os.getenv('HOME'), '.openconnect')
PID_FILE = os.path.join(WORK_DIR, 'openconnect.pid')

SUDO = '/usr/bin/sudo'
OPENCONNECT = '/usr/local/bin/openconnect'


class NoPidError(Exception):
    """Error type."""
    pass


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
        with open(PID_FILE, 'r') as pidfile:
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

    __mkdir_p(WORK_DIR)
    command = [
        SUDO,
        OPENCONNECT,
        '--setuid={}'.format(os.getlogin()),
        '--background',
        '--pid-file={}'.format(PID_FILE),
        '--quiet'
    ]
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
