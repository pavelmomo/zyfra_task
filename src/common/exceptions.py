class AppException(Exception):
    def __init__(self, message="Произошла внутренная ошибка приложения") -> None:
        super().__init__(message)
