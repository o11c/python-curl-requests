from collections import OrderedDict
import unittest
from urllib.parse import urljoin
import warnings

import werkzeug.serving

slow_tests = 1
use_curl_requests = 1
if not use_curl_requests:
    import requests
else:
    import curl_requests as requests

from .common import Anything, Convertible, Set
from .common import HttpBinMixin

server_version = object.__new__(werkzeug.serving.WSGIRequestHandler).version_string()

def munge(orig_dct):
    dct = orig_dct['headers']
    assert isinstance(dct, dict)
    bad_keys = []
    keys = list(dct)
    for k, v in dct.items():
        if v == '':
            assert k in ['Content-Length', 'Content-Type']
            bad_keys.append(k)
    for k in bad_keys:
        del dct[k]
    return orig_dct


class TestHttpBin(HttpBinMixin, unittest.TestCase):
    def test_delete(self):
        with requests.Session() as sess:
            for rs in [requests, sess]:
                for data in [None, '', 'abc', b'', b'abc']:
                    resp = rs.delete(urljoin(self.url, 'delete'), data=data)
                    assert resp.status_code == 200
                    if isinstance(data, bytes):
                        data = data.decode('ascii')
                    assert munge(resp.json()) == {
                        'args': {},
                        'data': data or '',
                        'files': {},
                        'form': {},
                        'headers': {
                            'Accept': '*/*',
                            'Accept-Encoding': 'gzip, deflate',
                            'Connection': 'keep-alive',
                            'Content-Length': '%d' % len(data or ''),
                            'Host': 'localhost:%s' % self.server_port,
                            'User-Agent': requests.utils.default_user_agent(),
                        },
                        'json': None,
                        'origin': '127.0.0.1',
                        'url': 'http://localhost:%d/delete' % self.server_port,
                    }, data
                    assert resp.headers == {
                        'Access-Control-Allow-Credentials': 'true',
                        'Access-Control-Allow-Origin': '*',
                        'Content-Length': Convertible(int),
                        'Content-Type': 'application/json',
                        'Date': Anything(str),
                        'Server': server_version,
                    }

    def test_get(self):
        with requests.Session() as sess:
            for rs in [requests, sess]:
                for data in [None, '', 'abc', b'', b'abc']:
                    if use_curl_requests and data:
                        with warnings.catch_warnings(record=True) as w:
                            warnings.simplefilter('always')
                            resp = rs.get(urljoin(self.url, 'get'), data=data)
                        assert len(w) == 1
                        assert w[0].category is requests.RequestWarning
                        assert w[0].message.args[0] == 'Payload with a GET is unspecified'
                    else:
                        resp = rs.get(urljoin(self.url, 'get'), data=data)
                    assert resp.status_code == 200
                    if isinstance(data, bytes):
                        data = data.decode('ascii')
                    assert munge(resp.json()) == munge({
                        'args': {},
                        'headers': {
                            'Accept': '*/*',
                            'Accept-Encoding': 'gzip, deflate',
                            'Connection': 'keep-alive',
                            'Content-Length': '%d' % len(data) if data else '',
                            'Host': 'localhost:%s' % self.server_port,
                            'User-Agent': requests.utils.default_user_agent(),
                        },
                        'origin': '127.0.0.1',
                        'url': 'http://localhost:%d/get' % self.server_port,
                    }), data
                    assert resp.headers == {
                        'Access-Control-Allow-Credentials': 'true',
                        'Access-Control-Allow-Origin': '*',
                        'Content-Length': Convertible(int),
                        'Content-Type': 'application/json',
                        'Date': Anything(str),
                        'Server': server_version,
                    }

    def test_head(self):
        with requests.Session() as sess:
            for rs in [requests, sess]:
                for data in [None, '', 'abc', b'', b'abc']:
                    if use_curl_requests and data:
                        with warnings.catch_warnings(record=True) as w:
                            warnings.simplefilter('always')
                            resp = rs.head(urljoin(self.url, 'get'), data=data)
                        assert len(w) == 1
                        assert w[0].category is requests.RequestWarning
                        assert w[0].message.args[0] == 'Payload with a HEAD is unspecified'
                    else:
                        resp = rs.head(urljoin(self.url, 'get'), data=data)
                    assert resp.status_code == 200
                    assert resp.content == b''
                    assert resp.text == u''
                    assert resp.headers == {
                        'Access-Control-Allow-Credentials': 'true',
                        'Access-Control-Allow-Origin': '*',
                        'Content-Length': Convertible(int),
                        'Content-Type': 'application/json',
                        'Date': Anything(str),
                        'Server': server_version,
                    }

    def test_options(self):
        with requests.Session() as sess:
            for rs in [requests, sess]:
                for data in [None, '', 'abc', b'', b'abc']:
                    resp = rs.options(urljoin(self.url, 'get'), data=data)
                    assert resp.status_code == 200
                    assert resp.content == b''
                    assert resp.text == u''
                    assert resp.headers == {
                        'Access-Control-Allow-Credentials': 'true',
                        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Max-Age': '3600',
                        'Allow': Set({'GET', 'HEAD', 'OPTIONS'}),
                        'Content-Length': '0',
                        'Content-Type': 'text/html; charset=utf-8',
                        'Date': Anything(str),
                        'Server': server_version,
                    }

    def test_patch(self):
        with requests.Session() as sess:
            for rs in [requests, sess]:
                for data in [None, '', 'abc', b'', b'abc']:
                    resp = rs.patch(urljoin(self.url, 'patch'), data=data)
                    assert resp.status_code == 200
                    if isinstance(data, bytes):
                        data = data.decode('ascii')
                    assert munge(resp.json()) == {
                        'args': {},
                        'data': data or '',
                        'files': {},
                        'form': {},
                        'headers': {
                            'Accept': '*/*',
                            'Accept-Encoding': 'gzip, deflate',
                            'Connection': 'keep-alive',
                            'Content-Length': '%d' % len(data or ''),
                            'Host': 'localhost:%s' % self.server_port,
                            'User-Agent': requests.utils.default_user_agent(),
                        },
                        'json': None,
                        'origin': '127.0.0.1',
                        'url': 'http://localhost:%d/patch' % self.server_port,
                    }, data
                    assert resp.headers == {
                        'Access-Control-Allow-Credentials': 'true',
                        'Access-Control-Allow-Origin': '*',
                        'Content-Length': Convertible(int),
                        'Content-Type': 'application/json',
                        'Date': Anything(str),
                        'Server': server_version,
                    }

    def test_post(self):
        with requests.Session() as sess:
            for rs in [requests, sess]:
                for data in [None, '', 'abc', b'', b'abc']:
                    resp = rs.post(urljoin(self.url, 'post'), data=data)
                    assert resp.status_code == 200
                    if isinstance(data, bytes):
                        data = data.decode('ascii')
                    assert munge(resp.json()) == {
                        'args': {},
                        'data': data or '',
                        'files': {},
                        'form': {},
                        'headers': {
                            'Accept': '*/*',
                            'Accept-Encoding': 'gzip, deflate',
                            'Connection': 'keep-alive',
                            'Content-Length': '%d' % len(data or ''),
                            'Host': 'localhost:%s' % self.server_port,
                            'User-Agent': requests.utils.default_user_agent(),
                        },
                        'json': None,
                        'origin': '127.0.0.1',
                        'url': 'http://localhost:%d/post' % self.server_port,
                    }, data
                    assert resp.headers == {
                        'Access-Control-Allow-Credentials': 'true',
                        'Access-Control-Allow-Origin': '*',
                        'Content-Length': Convertible(int),
                        'Content-Type': 'application/json',
                        'Date': Anything(str),
                        'Server': server_version,
                    }

    def test_put(self):
        with requests.Session() as sess:
            for rs in [requests, sess]:
                for data in [None, '', 'abc', b'', b'abc']:
                    resp = rs.put(urljoin(self.url, 'put'), data=data)
                    assert resp.status_code == 200
                    if isinstance(data, bytes):
                        data = data.decode('ascii')
                    assert munge(resp.json()) == {
                        'args': {},
                        'data': data or '',
                        'files': {},
                        'form': {},
                        'headers': {
                            'Accept': '*/*',
                            'Accept-Encoding': 'gzip, deflate',
                            'Connection': 'keep-alive',
                            'Content-Length': '%d' % len(data or ''),
                            'Host': 'localhost:%s' % self.server_port,
                            'User-Agent': requests.utils.default_user_agent(),
                        },
                        'json': None,
                        'origin': '127.0.0.1',
                        'url': 'http://localhost:%d/put' % self.server_port,
                    }, data
                    assert resp.headers == {
                        'Access-Control-Allow-Credentials': 'true',
                        'Access-Control-Allow-Origin': '*',
                        'Content-Length': Convertible(int),
                        'Content-Type': 'application/json',
                        'Date': Anything(str),
                        'Server': server_version,
                    }

    def test_404(self):
        with requests.Session() as sess:
            for method in ['delete', 'get', 'head', 'options', 'patch', 'post', 'put']:
                resp = sess.request(method, urljoin(self.url, 'status/404'))
                if method == 'options':
                    assert resp.status_code == 200
                    continue
                assert resp.status_code == 404
                assert resp.content == b''
                assert resp.text == u''
                assert resp.headers == {
                    'Access-Control-Allow-Credentials': 'true',
                    'Access-Control-Allow-Origin': '*',
                    'Content-Length': '0',
                    'Content-Type': 'text/html; charset=utf-8',
                    'Date': Anything(str),
                    'Server': server_version,
                }

    @unittest.skipIf(not slow_tests, 'test is slow')
    def test_status_1xx(self):
        with requests.Session() as sess:
            for i in range(100, 200):
                url = urljoin(self.url, 'status/%d' % i)
                for method in ['delete', 'get', 'head', 'options', 'patch', 'post', 'put']:
                    if use_curl_requests or i == 100:
                        with self.assertRaises(requests.RequestException):
                            _ = sess.get(url, allow_redirects=False)
                    else:
                        resp = sess.get(url, allow_redirects=False)
                        assert resp.status_code == i, (resp.status_code, i)
                        assert resp.text == u'', (resp.status_code, resp.text)

    @unittest.skipIf(not slow_tests, 'test is slow')
    def test_status_2xx(self):
        with requests.Session() as sess:
            for i in range(200, 300):
                url = urljoin(self.url, 'status/%d' % i)
                for method in ['delete', 'get', 'head', 'options', 'patch', 'post', 'put']:
                    resp = sess.get(url, allow_redirects=False)
                    assert resp.status_code == i, (resp.status_code, i)
                    assert resp.text == u'', (resp.status_code, resp.text)

    @unittest.skipIf(not slow_tests, 'test is slow')
    def test_status_3xx(self):
        with requests.Session() as sess:
            for i in range(300, 400):
                url = urljoin(self.url, 'status/%d' % i)
                for method in ['delete', 'get', 'head', 'options', 'patch', 'post', 'put']:
                    resp = sess.get(url, allow_redirects=False)
                    assert resp.status_code == i, (resp.status_code, i)
                    assert resp.text == u'', (resp.status_code, resp.text)

    @unittest.skipIf(not slow_tests, 'test is slow')
    def test_status_4xx(self):
        with requests.Session() as sess:
            for i in range(400, 500):
                text = {
                    402: u'Fuck you, pay me!',
                    406: {"message": "Client did not request a supported media type.", "accept": ["image/webp", "image/svg+xml", "image/jpeg", "image/png", "image/*"]},
                    418: u'\n    -=[ teapot ]=-\n\n       _...._\n     .\'  _ _ `.\n    | ."` ^ `". _,\n    \\_;`"---"`|//\n      |       ;/\n      \\_     _/\n        `"""`\n',
                }.get(i, u'')
                url = urljoin(self.url, 'status/%d' % i)
                for method in ['delete', 'get', 'head', 'options', 'patch', 'post', 'put']:
                    resp = sess.request(method, url, allow_redirects=False)
                    if method == 'options':
                        assert resp.status_code == 200
                        continue
                    assert resp.status_code == i, (resp.status_code, i)
                    if method == 'head':
                        assert resp.text == u''
                        continue
                    if isinstance(text, dict):
                        assert resp.json() == text, (resp.status_code, resp.text)
                    else:
                        assert resp.text == text, (resp.status_code, resp.text)

    @unittest.skipIf(not slow_tests, 'test is slow')
    def test_status_5xx(self):
        with requests.Session() as sess:
            for i in range(500, 600):
                url = urljoin(self.url, 'status/%d' % i)
                for method in ['delete', 'get', 'head', 'options', 'patch', 'post', 'put']:
                    resp = sess.get(url, allow_redirects=False)
                    assert resp.status_code == i, (resp.status_code, i)
                    assert resp.text == u'', (resp.status_code, resp.text)

    def test_params(self):
        with requests.Session() as sess:
            url = urljoin(self.url, 'get?a=b&c=d')
            for params in [
                'e=f&a=c&g=h&g=i',
                [('e', 'f'), ('a', 'c'), ('g', 'h'), ('g', 'i')],
                [('e', 'f'), ('a', 'c'), ('g', ['h', 'i'])],
                OrderedDict([('e', 'f'), ('a', 'c'), ('g', ['h', 'i'])]),
            ]:
                resp = sess.get(url, params=params)
                assert resp.status_code == 200
                assert munge(resp.json()) == {
                    'args': {'a': ['b', 'c'], 'c': 'd', 'e': 'f', 'g': ['h', 'i']},
                    'headers': {
                        'Accept': '*/*',
                        'Accept-Encoding': 'gzip, deflate',
                        'Connection': 'keep-alive',
                        'Host': 'localhost:%s' % self.server_port,
                        'User-Agent': requests.utils.default_user_agent(),
                    },
                    'origin': '127.0.0.1',
                    'url': 'http://localhost:%d/get?a=b&c=d&e=f&a=c&g=h&g=i' % self.server_port,
                }
