from .error_type import ErrorType


class BadRequestException(Exception):
    def __init__(self, error_type: ErrorType) -> None:
        super().__init__(error_type.message)
        self.code = error_type.code


class UnauthorizedException(Exception):
    def __init__(self, error_type: ErrorType) -> None:
        super().__init__(error_type.message)
        self.code = error_type.code
