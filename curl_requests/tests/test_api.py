import unittest
from urllib.parse import urljoin

if 0:
    import requests
else:
    import curl_requests as requests

from .common import HttpBinMixin


class TestHttpBin(HttpBinMixin, unittest.TestCase):
    def test_delete(self):
        with requests.Session() as sess:
            for rs in [requests, sess]:
                for data in [None, '', 'abc', b'', b'abc']:
                    resp = rs.delete(urljoin(self.url, 'delete'), data=data)
                    assert resp.status_code == 200
                    if isinstance(data, bytes):
                        data = data.decode('ascii')
                    assert resp.json() == {
                        'args': {},
                        'data': data or '',
                        'files': {},
                        'form': {},
                        'headers': {
                            'Accept': '*/*',
                            'Accept-Encoding': 'gzip, deflate',
                            'Connection': 'keep-alive',
                            'Content-Length': '%d' % len(data or ''),
                            'Content-Type': '',
                            'Host': 'localhost:%s' % self.server_port,
                            'User-Agent': requests.utils.default_user_agent(),
                        },
                        'json': None,
                        'origin': '127.0.0.1',
                        'url': 'http://localhost:%d/delete' % self.server_port,
                    }, data

    def test_get(self):
        with requests.Session() as sess:
            for rs in [requests, sess]:
                for data in [None, '', 'abc', b'', b'abc']:
                    resp = rs.get(urljoin(self.url, 'get'), data=data)
                    assert resp.status_code == 200
                    if isinstance(data, bytes):
                        data = data.decode('ascii')
                    assert resp.json() == {
                        'args': {},
                        'headers': {
                            'Accept': '*/*',
                            'Accept-Encoding': 'gzip, deflate',
                            'Connection': 'keep-alive',
                            'Content-Length': '%d' % len(data) if data else '',
                            'Content-Type': '',
                            'Host': 'localhost:%s' % self.server_port,
                            'User-Agent': requests.utils.default_user_agent(),
                        },
                        'origin': '127.0.0.1',
                        'url': 'http://localhost:%d/get' % self.server_port,
                    }, data

    def test_head(self):
        with requests.Session() as sess:
            for rs in [requests, sess]:
                for data in [None, '', 'abc', b'', b'abc']:
                    resp = rs.head(urljoin(self.url, 'get'), data=data)
                    assert resp.status_code == 200
                    assert resp.content == b''
                    assert resp.text == u''

    def test_options(self):
        with requests.Session() as sess:
            for rs in [requests, sess]:
                for data in [None, '', 'abc', b'', b'abc']:
                    resp = rs.options(urljoin(self.url, 'get'), data=data)
                    assert resp.status_code == 200
                    assert resp.content == b''
                    assert resp.text == u''

    def test_patch(self):
        with requests.Session() as sess:
            for rs in [requests, sess]:
                for data in [None, '', 'abc', b'', b'abc']:
                    resp = rs.patch(urljoin(self.url, 'patch'), data=data)
                    assert resp.status_code == 200
                    if isinstance(data, bytes):
                        data = data.decode('ascii')
                    assert resp.json() == {
                        'args': {},
                        'data': data or '',
                        'files': {},
                        'form': {},
                        'headers': {
                            'Accept': '*/*',
                            'Accept-Encoding': 'gzip, deflate',
                            'Connection': 'keep-alive',
                            'Content-Length': '%d' % len(data or ''),
                            'Content-Type': '',
                            'Host': 'localhost:%s' % self.server_port,
                            'User-Agent': requests.utils.default_user_agent(),
                        },
                        'json': None,
                        'origin': '127.0.0.1',
                        'url': 'http://localhost:%d/patch' % self.server_port,
                    }, data

    def test_post(self):
        with requests.Session() as sess:
            for rs in [requests, sess]:
                for data in [None, '', 'abc', b'', b'abc']:
                    resp = rs.post(urljoin(self.url, 'post'), data=data)
                    assert resp.status_code == 200
                    if isinstance(data, bytes):
                        data = data.decode('ascii')
                    assert resp.json() == {
                        'args': {},
                        'data': data or '',
                        'files': {},
                        'form': {},
                        'headers': {
                            'Accept': '*/*',
                            'Accept-Encoding': 'gzip, deflate',
                            'Connection': 'keep-alive',
                            'Content-Length': '%d' % len(data or ''),
                            'Content-Type': '',
                            'Host': 'localhost:%s' % self.server_port,
                            'User-Agent': requests.utils.default_user_agent(),
                        },
                        'json': None,
                        'origin': '127.0.0.1',
                        'url': 'http://localhost:%d/post' % self.server_port,
                    }, data

    def test_put(self):
        with requests.Session() as sess:
            for rs in [requests, sess]:
                for data in [None, '', 'abc', b'', b'abc']:
                    resp = rs.put(urljoin(self.url, 'put'), data=data)
                    assert resp.status_code == 200
                    if isinstance(data, bytes):
                        data = data.decode('ascii')
                    assert resp.json() == {
                        'args': {},
                        'data': data or '',
                        'files': {},
                        'form': {},
                        'headers': {
                            'Accept': '*/*',
                            'Accept-Encoding': 'gzip, deflate',
                            'Connection': 'keep-alive',
                            'Content-Length': '%d' % len(data or ''),
                            'Content-Type': '',
                            'Host': 'localhost:%s' % self.server_port,
                            'User-Agent': requests.utils.default_user_agent(),
                        },
                        'json': None,
                        'origin': '127.0.0.1',
                        'url': 'http://localhost:%d/put' % self.server_port,
                    }, data

    def test_get_404(self):
        with requests.Session() as sess:
            for rs in [requests, sess]:
                for data in [None, '', 'abc', b'', b'abc']:
                    resp = rs.get(urljoin(self.url, 'status/404'), data=data)
                    assert resp.status_code == 404
                    assert resp.content == b''
                    assert resp.text == u''
