import logging
import selectors
import socket
import socketserver
import threading
import types
import unittest

import httpbin
import werkzeug.serving


def maybe_bound_method(maybe_cls, function):
    if isinstance(maybe_cls, type):
        return function
    return types.MethodType(function, maybe_cls)


def monkeypatch_socketserver(what=None):
    ''' Replace serve_forever() and shutdown() with correct implementations.

        Either an instance or a class can be patched. But beware of MROs!
        Honestly, the sanest thing to do is just patch BaseServer once.
    '''
    if what is None:
        what = socketserver.BaseServer
    what.serve_forever = maybe_bound_method(what, _sane_serve_forever)
    what.shutdown = maybe_bound_method(what, _sane_shutdown)
    what.shutdown_pipe = None


def _sane_serve_forever(self, poll_interval='ignored'):
    assert self.shutdown_pipe is None
    try:
        read_sock, write_sock = socket.socketpair()
        with read_sock, write_sock:
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
        self.shutdown_pipe = None
        #self.server_close()


def _sane_shutdown(self):
    assert self.shutdown_pipe is not None
    self.shutdown_pipe.send(b'\0')
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
        #monkeypatch_socketserver(server)
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
