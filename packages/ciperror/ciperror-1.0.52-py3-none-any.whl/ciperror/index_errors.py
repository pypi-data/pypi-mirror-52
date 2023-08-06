from ciperror import BaseCipError


class IndexServiceRequestError(BaseCipError):
    def __init__(self, message):
        super().__init__(
            code="IDX001",
            message="Erro no request para o Index Service: {}".format(message),
            friendly_message="Erro no request para o Index Service.",
            http_status=500)
