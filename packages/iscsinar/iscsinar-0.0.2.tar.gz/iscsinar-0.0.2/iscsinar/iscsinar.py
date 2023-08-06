#!/usr/bin/python
import os
import sys

import atexit
import signal

def daemonize(pidfile, stdin='/dev/null',
                          stdout='/dev/null',
                          stderr='/dev/null'):

    if os.path.exists(pidfile):
        raise RuntimeError('Already running')

    # First fork (detaches from parent)
    try:
        if os.fork() > 0:
            raise SystemExit(0)   # Parent exit
    except OSError as e:
        raise RuntimeError('fork #1 failed.')

    os.chdir('/')
    os.umask(0)
    os.setsid()
    # Second fork (relinquish session leadership)
    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError as e:
        raise RuntimeError('fork #2 failed.')

    # Flush I/O buffers
    sys.stdout.flush()
    sys.stderr.flush()

    # Replace file descriptors for stdin, stdout, and stderr
    with open(stdin, 'rb', 0) as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open(stdout, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
    with open(stderr, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stderr.fileno())

    # Write the PID file
    fd = open(pidfile, 'w')
    fd.write('{}\n'.format(os.getpid()))
    fd.close()
    # Arrange to have the PID file removed on exit/signal
    atexit.register(lambda: os.remove(pidfile))

    # Signal handler for termination (required)
    def sigterm_handler(signo, frame):
        raise SystemExit(1)

    signal.signal(signal.SIGTERM, sigterm_handler)

def main():
    import time , threading
    while True:
        fd = open('/root/daemon.log', 'a')
        fd.write('Daemon Alive! {}\n'.format(time.ctime()))
        fd.write('Daemon started with pid {}\n'.format(os.getpid()))
        fd.flush()
        time.sleep(3)
        fd.write('Daemon Alive! {}\n'.format(time.ctime()))
        fd.flush()
        sys.stdout.write('Daemon Alive! {}\n'.format(time.ctime()))
    fd.close()


if __name__ == '__main__':
    PIDFILE = '/root/daemon.pid'

    if len(sys.argv) != 2:
        try:
            daemonize(PIDFILE,
                      stdout='/root/daemon.log',
                      stderr='/root/daemon.log')
        except RuntimeError as e:
            raise SystemExit(1)

        main()

    if sys.argv[1] == 'start':
        try:
            daemonize(PIDFILE,
                      stdout='/root/daemon.log',
                      stderr='/root/daemon.log')
        except RuntimeError as e:
            raise SystemExit(1)

        main()

    elif sys.argv[1] == 'stop':
        if os.path.exists(PIDFILE):
            with open(PIDFILE) as f:
                os.kill(int(f.read()), signal.SIGTERM)
        else:
            print('Not running')
            raise SystemExit(1)

    else:
        try:
            daemonize(PIDFILE,
                      stdout='/root/daemon.log',
                      stderr='/root/daemon.log')
        except RuntimeError as e:
            raise SystemExit(1)

        main()
