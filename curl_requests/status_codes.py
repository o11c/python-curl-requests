from . import _enum


class codes(_enum.ExtensibleEnum):
    pass


# See https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml
# but a handful of other names are added too, as marked.

# Informational
codes(100, 'Continue')
codes(101, 'Switching Protocols')
codes(102, 'Processing')
# Successful
codes(200, 'OK')
codes(201, 'Created')
codes(202, 'Accepted')
codes(203, 'Non-Authoritative Information')
codes(204, 'No Content')
codes(205, 'Reset Content')
codes(206, 'Partial Content')
codes(207, 'Multi-Status')
codes(208, 'Already Reported')
codes(226, 'IM Used')
# Redirection
codes(300, 'Multiple Choices')
codes(301, 'Moved Permanently')
codes(302, 'Found')
codes(303, 'See Other')
codes(304, 'Not Modified')
codes(305, 'Use Proxy')
codes(306, None)
codes(306, 'Switch Proxy') # withdrawn
codes(307, 'Temporary Redirect')
codes(308, 'Permanent Redirect')
# Client Error
codes(400, 'Bad Request')
codes(401, 'Unauthorized')
codes(402, 'Payment Required')
codes(403, 'Forbidden')
codes(404, 'Not Found')
codes(405, 'Method Not Allowed')
codes(406, 'Not Acceptable')
codes(407, 'Proxy Authentication Required')
codes(408, 'Request Timeout')
codes(409, 'Conflict')
codes(410, 'Gone')
codes(411, 'Length Required')
codes(412, 'Precondition Failed')
codes(413, 'Payload Too Large')
codes(414, 'URI Too Long')
codes(415, 'Unsupported Media Type')
codes(416, 'Range Not Satisfiable')
codes(417, 'Expectation Failed')
codes(418, None)
codes(418, 'I\'m a teapot') # RFC 2324
codes(421, 'Misdirected Request')
codes(422, 'Unprocessable Entity')
codes(423, 'Locked')
codes(424, 'Failed Dependency')
codes(426, 'Upgrade Required')
codes(428, 'Precondition Required')
codes(429, 'Too Many Requests')
codes(431, 'Request Header Fields Too Large')
codes(451, 'Unavailable For Legal Reasons')
# Server Error
codes(500, 'Internal Server Error')
codes(501, 'Not Implemented')
codes(502, 'Bad Gateway')
codes(503, 'Service Unavailable')
codes(504, 'Gateway Timeout')
codes(505, 'HTTP Version Not Supported')
codes(506, 'Variant Also Negotiates')
codes(507, 'Insufficient Storage')
codes(508, 'Loop Detected')
codes(510, 'Not Extended')
codes(511, 'Network Authentication Required')
for i in range(100, 600):
    codes(i)
del i
