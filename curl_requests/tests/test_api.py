import unittest
from urllib.parse import urljoin
import warnings

use_curl_requests = 1
if not use_curl_requests:
    import requests
else:
    import curl_requests as requests

from .common import HttpBinMixin


def munge(orig_dct):
    dct = orig_dct['headers']
    assert isinstance(dct, dict)
    bad_keys = []
    keys = list(dct)
    for k, v in dct.items():
        if v == '':
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

    def test_get_404(self):
        with requests.Session() as sess:
            for rs in [requests, sess]:
                resp = rs.get(urljoin(self.url, 'status/404'))
                assert resp.status_code == 404
                assert resp.content == b''
                assert resp.text == u''
