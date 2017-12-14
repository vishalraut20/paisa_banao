from http import HTTPStatus


class InvalidRequestException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.http_status_code = HTTPStatus.BAD_REQUEST