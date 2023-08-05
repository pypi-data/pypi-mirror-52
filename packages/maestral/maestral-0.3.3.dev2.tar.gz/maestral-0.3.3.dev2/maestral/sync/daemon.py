# -*- coding: utf-8 -*-
"""
@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under a Creative Commons
Attribution-NonCommercial-NoDerivs 2.0 UK: England & Wales License.

"""
# system imports
import os
import time

# external packages
import Pyro4

URI = "PYRO:maestral.{0}@{1}"


def write_pid(config_name, socket_address):
    """
    Write the PID of the current process to the appropriate file for the given
    config name. If a socket_address is given, it will be appended after a '|'.
    """
    from maestral.config.base import get_conf_path
    pid_file = get_conf_path("maestral", config_name + ".pid")
    with open(pid_file, "w") as f:
        f.write(str(os.getpid()) + "|" + socket_address)


def read_pid(config_name):
    """
    Reads the PID of the current process to the appropriate file for the given
    config name.
    """
    from maestral.config.base import get_conf_path
    pid_file = get_conf_path("maestral", config_name + ".pid")
    with open(pid_file, "r") as f:
        pid, socket = f.read().split("|")
    pid = int(pid)

    return pid, socket


def delete_pid(config_name):
    """
    Reads the PID of the current process to the appropriate file for the given
    config name.
    """
    from maestral.config.base import get_conf_path
    pid_file = get_conf_path("maestral", config_name + ".pid")
    os.unlink(pid_file)


def start_maestral_daemon(config_name, run=True):
    """

    Wraps :class:`maestral.main.Maestral` as Pyro daemon object, creates a new instance
    and start Pyro's event loop to listen for requests on 'localhost'. This call will
    block until the event loop shuts down.

    This command will create a new daemon on each run. Take care not to sync the same
    directory with multiple instances of Meastral! You can use `get_maestral_process_info`
    to check if either a Meastral gui or daemon is already running for the given
    `config_name`.

    :param str config_name: The name of maestral configuration to use.
    :param bool run: If ``True``, start syncing automatically. Defaults to ``True``.
    """

    os.environ["MAESTRAL_CONFIG"] = config_name

    import sys
    from maestral.sync.main import Maestral

    daemon = Pyro4.Daemon()

    write_pid(config_name, daemon.locationStr)  # write PID to file

    try:
        # we wrap this in a try-except block to make sure that the PID file is always
        # removed, even when Maestral crashes for some reason

        ExposedMaestral = Pyro4.expose(Maestral)
        m = ExposedMaestral(run=run)

        daemon.register(m, "maestral.{}".format(config_name))
        daemon.requestLoop(loopCondition=m._loop_condition)
        daemon.close()
    except Exception:
        import traceback
        traceback.print_exc()
    finally:
        delete_pid(config_name)  # remove PID file


def start_maestral_daemon_thread(config_name):
    """Starts the Maestral daemon in a thread (by calling `start_maestral_daemon`).

    This command will create a new daemon on each run. Take care not to sync the same
    directory with multiple instances of Meastral! You can use `get_maestral_process_info`
    to check if either a Meastral gui or daemon is already running for the given
    `config_name`.

    :param str config_name: The name of maestral configuration to use.
    :returns: ``True`` if started, ``False`` otherwise.
    """
    import threading
    from maestral.sync.main import Maestral

    if Maestral.pending_link() or Maestral.pending_dropbox_folder():
        # run setup
        m = Maestral(run=False)
        m.create_dropbox_directory()
        m.set_excluded_folders()

    t = threading.Thread(
        target=start_maestral_daemon,
        args=(config_name, ),
        kwargs={"run": False},
        daemon=True,
        name="Maestral daemon",
    )
    t.start()

    time.sleep(0.2)
    if t.is_alive():
        return True
    else:
        return False


def start_maestral_daemon_process(config_name):
    """Starts the Maestral daemon as a separate process (by calling
    `start_maestral_daemon`).

    This command will create a new daemon on each run. Take care not to sync the same
    directory with multiple instances of Meastral! You can use `get_maestral_process_info`
    to check if either a Meastral gui or daemon is already running for the given
    `config_name`.

    :param str config_name: The name of maestral configuration to use.
    :returns: ``True`` if started, ``False`` otherwise.
    """
    import subprocess
    from maestral.sync.main import Maestral

    if Maestral.pending_link() or Maestral.pending_dropbox_folder():
        # run setup
        m = Maestral(run=False)
        m.create_dropbox_directory()
        m.set_excluded_folders()

    subprocess.Popen(
        "maestral start -c {} --foreground".format(config_name),
        shell=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # wait until process is created, timeout after 1 sec

    t0 = time.time()
    location = None

    while not location and t0 - time.time() < 1:
        pid, location = get_maestral_process_info(config_name)

    if location:
        maestral_daemon = Pyro4.Proxy(URI.format(config_name, location))
    else:
        return False

    # wait until we can communicate with daemon, timeout after 1 sec
    t0 = time.time()
    while time.time() - t0 < 1:
        try:
            maestral_daemon._pyroBind()
            return True
        except Exception:
            maestral_daemon._pyroRelease()
            time.sleep(0.1)
        finally:
            maestral_daemon._pyroRelease()

    return False


def stop_maestral_daemon_process(config_name="maestral"):
    """Stops maestral by finding its PID and shutting it down.

    This function first tries to shut down Maestral gracefully. If this fails, it will
    send SIGTERM. If that fails as well, it will send SIGKILL.

    :param str config_name: The name of maestral configuration to use.
    :returns: ``True`` if terminated gracefully, ``False`` if killed and ``None`` if the
        daemon was not running.
    """
    import signal
    import time

    pid, socket = get_maestral_process_info(config_name)
    if pid:
        try:
            # try to shut down gracefully
            with MaestralProxy(config_name) as m:
                m.stop_sync()
                m.shutdown_daemon()
        except Pyro4.errors.CommunicationError:
            try:
                # send SIGTERM if failed
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                delete_pid(pid)
                return
        finally:
            t0 = time.time()
            while True:
                try:
                    os.kill(pid, 0)
                except OSError:
                    # process does not exist anymore
                    return True
                else:
                    time.sleep(0.2)
                    if time.time() - t0 > 5:
                        # send SIGKILL if still running
                        os.kill(pid, signal.SIGKILL)
                        return False


def get_maestral_daemon_proxy(config_name="maestral", fallback=False):
    """
    Returns a proxy of the running Maestral daemon. If fallback == True,
    a new instance of Maestral will be returned when the daemon cannot be reached.
    """

    pid, location = get_maestral_process_info(config_name)

    if pid:
        maestral_daemon = Pyro4.Proxy(URI.format(config_name, location))
        try:
            maestral_daemon._pyroBind()
            return maestral_daemon
        except Pyro4.errors.CommunicationError:
            maestral_daemon._pyroRelease()

    if fallback:
        from maestral.sync.main import Maestral
        m = Maestral(run=False)
        return m
    else:
        raise Pyro4.errors.CommunicationError


class MaestralProxy(object):
    """A context manager to open and close a Proxy to the Maestral daemon."""

    def __init__(self, config_name="maestral", fallback=False):
        self.m = get_maestral_daemon_proxy(config_name, fallback)

    def __enter__(self):
        return self.m

    def __exit__(self, exc_type, exc_value, traceback):
        if hasattr(self.m, "_pyroRelease"):
            self.m._pyroRelease()

        del self.m


def get_maestral_process_info(config_name):
    """
    Returns Maestral's PID and the socket location as tuple (pid, socket) if Maestral
    is running or (``None``, ``None``)  otherwise.

    If not ``None``, ``socket`` will be a string of the form "<network_address>:<port>".
    """
    import signal

    try:
        pid, socket = read_pid(config_name)
    except Exception:
        return None, None

    try:
        # test if the daemon process receives signals
        os.kill(pid, 0)
    except ProcessLookupError:
        # if the process does not exist, delete pid file
        try:
            delete_pid(config_name)
        except Exception:
            pass
        return None, None
    except OSError:
        # if the process does not respond, try to kill it
        os.kill(pid, signal.SIGKILL)
        try:
            delete_pid(config_name)
        except Exception:
            pass
        return None, None
    else:
        # everything ok, return process info
        return pid, socket
