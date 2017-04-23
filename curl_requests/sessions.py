import io
import warnings

import pycurl

from .exceptions import RequestException, RequestWarning
from .models import Response
from .status_codes import codes
from .structures import CaseInsensitiveDict


class Session:
    __slots__ = ('curl',)

    def __enter__(self):
        self.curl = pycurl.Curl()
        return self

    def __exit__(self, ty, v, tb):
        self.curl.close()
        del self.curl

    def request(self, method, url, *, params=None, data=None, json=None, allow_redirects=True, stacklevel=1):
        c = self.curl
        try:
            c.reset()
            if 0: c.setopt(pycurl.VERBOSE, True)
            headers = []
            if isinstance(data, str):
                data = data.encode('ascii')
            headers.append('Connection: keep-alive')
            c.setopt(pycurl.ACCEPT_ENCODING, b'gzip, deflate')
            method = method.casefold().upper()
            if 0:
                pass
            elif method == 'GET':
                if 0: c.setopt(pycurl.HTTPGET, True)
                if data:
                    warnings.warn('Payload with a GET is unspecified', RequestWarning, stacklevel=stacklevel+1)
                    c.setopt(pycurl.UPLOAD, True)
                    c.setopt(pycurl.CUSTOMREQUEST, method)
            elif method == 'HEAD':
                c.setopt(pycurl.NOBODY, True)
                if data:
                    warnings.warn('Payload with a HEAD is unspecified', RequestWarning, stacklevel=stacklevel+1)
                    c.setopt(pycurl.UPLOAD, True)
                    c.setopt(pycurl.CUSTOMREQUEST, method)
                    headers[headers.index('Connection: keep-alive')] = 'Connection: close'
            elif method == 'POST':
                if data is None: data = b''
                c.setopt(pycurl.POST, True)
            elif method == 'PUT':
                if data is None: data = b''
                c.setopt(pycurl.UPLOAD, True)
            else:
                # OPTIONS goes here too.
                if method in {'DELETE', 'PATCH'}:
                    c.setopt(pycurl.UPLOAD, True)
                    if data is None: data = b''
                elif data:
                    c.setopt(pycurl.UPLOAD, True)
                c.setopt(pycurl.CUSTOMREQUEST, method)
            if data is not None:
                if method == 'POST':
                    c.setopt(pycurl.POSTFIELDSIZE_LARGE, len(data))
                    c.setopt(pycurl.COPYPOSTFIELDS, data)
                    headers.append('Content-Type:')
                else:
                    c.setopt(pycurl.READDATA, io.BytesIO(data))
                    c.setopt(pycurl.INFILESIZE_LARGE, len(data))
                    headers.append('Expect:')
            c.setopt(pycurl.FOLLOWLOCATION, allow_redirects)
            c.setopt(pycurl.URL, url.encode('ascii'))
            output_buffer = io.BytesIO()
            header_buffer = io.BytesIO()
            c.setopt(pycurl.WRITEFUNCTION, output_buffer.write)
            c.setopt(pycurl.HEADERFUNCTION, header_buffer.write)
            c.setopt(pycurl.HTTPHEADER, headers)
            try:
                c.perform()
            except pycurl.error as e:
                if method == 'HEAD' and data and e.args[0] == pycurl.E_PARTIAL_FILE:
                    pass # ignore the expected error when using this hack
                else:
                    raise RequestException('perform() failed') from e
            else:
                if method == 'HEAD' and data:
                    raise RequestException('Expected perform() to fail when using this hack (???)')
            resp = Response()
            resp.content = output_buffer.getvalue()
            resp.headers = CaseInsensitiveDict()
            for line in header_buffer.getvalue().decode('ascii').split('\r\n')[1:-2]:
                k, _, v = line.partition(': ')
                assert k not in resp.headers
                resp.headers[k] = v
            resp.status_code = codes(c.getinfo(pycurl.RESPONSE_CODE))
        finally:
            c.reset()
        return resp

    def delete(self, url, stacklevel=1, **kwargs):
        return self.request('delete', url, stacklevel=stacklevel+1, **kwargs)

    def get(self, url, params=None, stacklevel=1, **kwargs):
        return self.request('get', url, params=params, stacklevel=stacklevel+1, **kwargs)

    def head(self, url, stacklevel=1, **kwargs):
        kwargs.setdefault('allow_redirects', False)
        return self.request('head', url, stacklevel=stacklevel+1, **kwargs)

    def options(self, url, stacklevel=1, **kwargs):
        return self.request('options', url, stacklevel=stacklevel+1, **kwargs)

    def patch(self, url, data=None, stacklevel=1, **kwargs):
        return self.request('patch', url,  data=data, stacklevel=stacklevel+1, **kwargs)

    def post(self, url, data=None, json=None, stacklevel=1, **kwargs):
        return self.request('post', url, data=data, json=json, stacklevel=stacklevel+1, **kwargs)

    def put(self, url, data=None, stacklevel=1, **kwargs):
        return self.request('put', url, data=data, stacklevel=stacklevel+1, **kwargs)
