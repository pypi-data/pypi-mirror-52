import sys


class PianoError(Exception):

    def __init__(self, message=None, http_body=None, http_status=None,
                 json_body=None, headers=None):
        super(PianoError, self).__init__(message)

        self._message = message
        self.http_body = http_body
        self.http_status = http_status
        self.json_body = json_body
        self.headers = headers or {}
        self.request_id = self.headers.get('request-id', None)

    def __unicode__(self):
        if self.request_id is not None:
            msg = self._message or "<empty message>"
            return u"Request {0}: {1}".format(self.request_id, msg)
        else:
            return self._message

    if sys.version_info > (3, 0):
        def __str__(self):
            return self.__unicode__()
    else:
        def __str__(self):
            return unicode(self).encode('utf-8')


class APIError(PianoError):
    pass


class APIConnectionError(PianoError):
    pass


class InvalidRequestError(PianoError):

    def __init__(self, message, param, code=None, http_body=None,
                 http_status=None, json_body=None, headers=None):
        super(InvalidRequestError, self).__init__(
            message, http_body, http_status, json_body,
            headers)
        self.param = param
        self.code = code


class AuthenticationError(PianoError):
    pass


class PermissionError(PianoError):
    pass
