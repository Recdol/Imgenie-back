from enum import Enum


class ErrorType(Enum):
    NOT_AUTHENTICATED = (1001, "인증되지 않았습니다.")
    INVALID_USER = (1002, "유효하지 않은 유저입니다.")
    FORBIDDEN_USER = (1004, "권한이 없습니다")

    def __init__(self, code: int, message: str):
        # The variable "code" is not the http status code but the service error code
        self.code = code
        self.message = message
