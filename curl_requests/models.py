import json


class Request:
    __slots__ = ()


class PreparedRequest:
    __slots__ = ()


class Response:
    __slots__ = ('content', 'status_code')

    @property
    def text(self):
        return self.content.decode('utf-8')

    def json(self):
        return json.loads(self.text)
