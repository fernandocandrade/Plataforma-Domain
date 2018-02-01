import logging
import requests


def log(msg, *args, **kwargs):
    logger = logging.getLogger()
    logger.error(msg.format(*args, **kwargs))


class VERBS:
    """HTTP Verbs
    """
    GET = requests.get
    POST = requests.post


class ExecutionResult:
    """HTTP requests friendly result.
    """

    def __init__(self, status_code, has_error=False,
                 error_message=None, data=None):
        self.status_code = status_code
        self.has_error = has_error
        self.error_message = error_message
        self.data = data

    @classmethod
    def ok(cls, status_code=200, data=None):
        return cls(status_code=status_code, data=data)

    @classmethod
    def error(cls, message, status_code=None, data=None):
        log("""
            HTTP request error
            status code: {status_code}
            message: {message}
            """, status_code=status_code, message=message)

        return cls(
            status_code=status_code,
            has_error=True,
            error_message=message,
            data=data)


class HttpClient:
    """Simple client to interact with HTTP endpoints.
    """
    @staticmethod
    def _request(uri, verb, **kwargs):
        def _error(message, status_code=None):
            return ExecutionResult.error(
                status_code=status_code,
                message=message + f"""
                    host: {uri}
                    args: {kwargs}
                """
            )

        try:
            data = None
            response = verb(uri, **kwargs)
            response.raise_for_status()

            if response.text:
                data = response.json()

            return ExecutionResult.ok(
                status_code=response.status_code,
                data=data
            )
        except Exception as excpt:
            return ExecutionResult.error(
                message=excpt.args[0])

    @classmethod
    def get(cls, uri):
        return cls._request(uri=uri, verb=VERBS.GET)

    @classmethod
    def post(cls, uri, data=None):
        args = {}

        if data:
            args['json'] = data

        return cls._request(uri=uri, verb=VERBS.POST, **args)
