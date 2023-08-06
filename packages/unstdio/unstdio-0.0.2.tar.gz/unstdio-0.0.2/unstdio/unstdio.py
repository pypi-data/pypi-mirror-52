import io
import sys
from .tee import Tee
import threading


class Inp(io.StringIO):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def read(self, *args, **kwargs):
        super().read(self, *args, **kwargs)

    def write(self, *args, **kwargs):
        super().write(*args, **kwargs)


class Out(io.StringIO):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def read(self, *args, **kwargs):
        super().read(self, *args, **kwargs)

    def write(self, *args, **kwargs):
        super().write(*args, **kwargs)


class Err(io.StringIO):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def read(self, *args, **kwargs):
        super().read(self, *args, **kwargs)

    def write(self, *args, **kwargs):
        super().write(*args, **kwargs)


class Environment(object):
    def __init__(
        self,
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr,
    ):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr


class Unstdio(object):
    rlock = threading.RLock()

    def __init__(
        self,
        stdin_file=None,
        stdout_file=None,
        stderr_file=None,
    ):
        self.stdin = Inp()
        self.stdout = Out()
        self.stderr = Err()
        self.old_stdin = sys.stdin
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr

    def __enter__(self):
        if Unstdio.rlock.acquire():
            sys.stdin = self.stdin
            sys.stdout = self.stdout
            sys.stderr = self.stderr
            return Environment(
                self.stdin, self.stdout, self.stderr
            )

    def __exit__(self, *args):
        sys.stdin = self.old_stdin
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        Unstdio.rlock.release()
