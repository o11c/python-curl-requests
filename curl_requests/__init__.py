''' A `requests`-like library built on libcurl
'''

from .api import delete, get, head, options, patch, post, put, request
from .exceptions import RequestException, RequestWarning
from .models import PreparedRequest, Request, Response
from .sessions import Session
from .status_codes import codes
from . import utils
