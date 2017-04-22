from . import sessions


def request(method, url, stacklevel=1, **kwargs):
    with sessions.Session() as session:
        return session.request(method=method, url=url, stacklevel=stacklevel+1, **kwargs)


def delete(url, stacklevel=1, **kwargs):
    return request('delete', url, stacklevel=stacklevel+1, **kwargs)


def get(url, params=None, stacklevel=1, **kwargs):
    return request('get', url, params=params, stacklevel=stacklevel+1, **kwargs)


def head(url, stacklevel=1, **kwargs):
    kwargs.setdefault('allow_redirects', False)
    return request('head', url, stacklevel=stacklevel+1, **kwargs)


def options(url, stacklevel=1, **kwargs):
    return request('options', url, stacklevel=stacklevel+1, **kwargs)


def patch(url, data=None, stacklevel=1, **kwargs):
    return request('patch', url,  data=data, stacklevel=stacklevel+1, **kwargs)


def post(url, data=None, json=None, stacklevel=1, **kwargs):
    return request('post', url, data=data, json=json, stacklevel=stacklevel+1, **kwargs)


def put(url, data=None, stacklevel=1, **kwargs):
    return request('put', url, data=data, stacklevel=stacklevel+1, **kwargs)
