import logging
import selectors
import socket
import socketserver
import threading
import types
import unittest

import httpbin
import werkzeug.serving


def monkeypatch_socketserver():
    ''' Replace serve_forever() and shutdown() with correct implementations.

        Either an instance or a class can be patched. But beware of MROs!
        Honestly, the sanest thing to do is just patch BaseServer once.
    '''
    what = socketserver.BaseServer
    def _sane_init(self, *args, __orig_init=what.__init__, **kwargs):
        __orig_init(self, *args, **kwargs)
        self.shutdown_lock = threading.Lock()
        self.shutdown_pipe = None
    what.__init__ = _sane_init
    what.serve_forever = _sane_serve_forever
    what.shutdown = _sane_shutdown


def _sane_serve_forever(self, poll_interval='ignored'):
    assert self.shutdown_pipe is None
    write_sock = None
    try:
        read_sock, write_sock = socket.socketpair()
        with read_sock:
            self.shutdown_pipe = write_sock

            with selectors.DefaultSelector() as selector:
                selector.register(self, selectors.EVENT_READ)
                selector.register(read_sock, selectors.EVENT_READ)

                while True:
                    ready = selector.select(None)
                    for key, mask in ready:
                        assert isinstance(key, selectors.SelectorKey)
                        fo = key.fileobj
                        if fo is read_sock:
                            read_sock.recv(1)
                            read_sock.shutdown(socket.SHUT_WR)
                            return
                        else:
                            assert fo is self, fo
                    if ready:
                        self._handle_request_noblock()

                    self.service_actions()
    finally:
        with self.shutdown_lock:
            self.shutdown_pipe.close()
            self.shutdown_pipe = None


def _sane_shutdown(self):
    assert self.shutdown_pipe is not None
    self.shutdown_pipe.send(b'\0')
    with self.shutdown_lock:
        if self.shutdown_pipe is not None:
            self.shutdown_pipe.recv(1)


monkeypatch_socketserver()


def dummy_client(server_address):
    ''' Ensure that the server has entered the main loop (i.e. is accepting).
    '''
    with socket.socket() as c:
        c.connect(server_address)


logging.getLogger('werkzeug').setLevel(logging.ERROR)


class RunApp:
    def __init__(self, app):
        self.app = app
        server = self.server = werkzeug.serving.BaseWSGIServer('localhost', 0, app)
        self.url = 'http://%s:%s/' % (server.server_name, server.server_port)

    def __repr__(self):
        return '<RunApp on %s >' % self.url

    def __enter__(self):
        server = self.server
        # This doesn't *need* to be a daemon, but exit is faster this way.
        threading.Thread(target=server.serve_forever, daemon=True).start()
        dummy_client(self.server.server_address)
        return self

    def __exit__(self, ty, v, tb):
        self.server.shutdown()


class HttpBinMixin:
    run_app = None
    server_name = None
    server_port = None
    url = None

    def setUp(self):
        super().setUp()
        self.run_app = RunApp(httpbin.app)
        self.run_app.__enter__()
        self.server_name = self.run_app.server.server_name
        self.server_port = self.run_app.server.server_port
        self.url = self.run_app.url

    def tearDown(self):
        super().tearDown()
        self.run_app.__exit__(None, None, None)
        del self.run_app
        del self.server_name
        del self.server_port
        del self.url


class Anything:
    def __init__(self, type=object):
        self.type = type

    def __repr__(self):
        return '<%s type=%s>' % (self.__class__.__name__, self.type.__name__)

    def __eq__(self, other):
        return isinstance(other, self.type)


class Convertible(Anything):
    def __eq__(self, other):
        try:
            self.type(other)
        except (TypeError, ValueError):
            return False
        else:
            return True


class Set(Anything):
    def __init__(self, set, split=', '):
        self.set = set
        self.split = split

    def __repr__(self):
        return '<%s set=%r split=%r>' % (self.__class__.__name__, self.set, self.split)

    def __eq__(self, other):
        return isinstance(other, str) and set(other.split(self.split)) == self.set
