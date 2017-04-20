import os
import pycurl
from tqdm import tqdm


downloader = pycurl.Curl()


def sanitize(c):
    c.setopt(pycurl.UNRESTRICTED_AUTH, False)
    c.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_ANYSAFE)
    c.setopt(pycurl.ACCEPT_ENCODING, b'')
    c.setopt(pycurl.TRANSFER_ENCODING, True)
    c.setopt(pycurl.SSL_VERIFYPEER, True)
    c.setopt(pycurl.SSL_VERIFYHOST, 2)
    c.setopt(pycurl.SSLVERSION, pycurl.SSLVERSION_TLSv1)
    #c.setopt(pycurl.FOLLOWLOCATION, False)
    c.setopt(pycurl.FOLLOWLOCATION, True)


def do_download(url, local, *, safe=True):
    rv = False
    with tqdm(desc=url, total=1, unit='b', unit_scale=True) as progress:
        xfer = XferInfoDl(url, progress)
        if safe:
            local_tmp = local + '.tmp'
        else:
            local_tmp = local

        c = downloader
        c.reset()
        sanitize(c)

        c.setopt(pycurl.NOPROGRESS, False)
        c.setopt(pycurl.XFERINFOFUNCTION, xfer)

        c.setopt(pycurl.URL, url.encode('utf-8'))
        with open(local_tmp, 'wb') as out:
            c.setopt(pycurl.WRITEDATA, out)
            try:
                c.perform()
            except pycurl.error:
                os.unlink(local_tmp)
                return False
        if c.getinfo(pycurl.RESPONSE_CODE) >= 400:
            os.unlink(local_tmp)
        else:
            if safe:
                os.rename(local_tmp, local)
            rv = True
        progress.total = progress.n = progress.n - 1
        progress.update(1)
    return rv


class XferInfoDl:
    def __init__(self, url, progress):
        self._tqdm = progress

    def __call__(self, dltotal, dlnow, ultotal, ulnow):
        n = dlnow - self._tqdm.n
        self._tqdm.total = dltotal or guess_size(dlnow)
        if n:
            self._tqdm.update(n)


def guess_size(now):
    ''' Return a number that is strictly greater than `now`,
        but likely close to `approx`.
    '''
return 1 << now.bit_length()
