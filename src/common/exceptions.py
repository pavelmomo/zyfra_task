class AppException(Exception):
    def __init__(self, message="Произошла внутренная ошибка приложения") -> None:
        super().__init__(message)


class ServiceException(AppException):
    def __init__(self, message="Произошла ошибка в сервисном слое приложения") -> None:
        super().__init__(message)


class NotFoundException(ServiceException):
    def __init__(self, message="Ресурс не найден") -> None:
        super().__init__(message)


class InvalidCredentialException(ServiceException):
    def __init__(self, message="Учётные данные невалидны") -> None:
        super().__init__(message)


class CredentialExpiredException(ServiceException):
    def __init__(self, message="Срок действия учётных данных истёк") -> None:
        super().__init__(message)
