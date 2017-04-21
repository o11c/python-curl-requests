import contextlib
import pycurl


def default_user_agent():
    return pycurl.version
