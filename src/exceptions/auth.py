from .common import UnauthorizedException, ForbiddenException
from .error_type import ErrorType


class InvalidTokenException(UnauthorizedException):
    def __init__(self, error_type: ErrorType) -> None:
        super().__init__(error_type)


class RequiredTokenException(UnauthorizedException):
    def __init__(self, error_type: ErrorType) -> None:
        super().__init__(error_type)


class ForbiddenTokenException(ForbiddenException):
    def __init__(self, error_type: ErrorType) -> None:
        super().__init__(error_type)
