from ciperror import BaseCipError


class GenericConfigurationError(BaseCipError):
    def __init__(self, message):
        super().__init__(
            code="CONF001",
            message="Erro de configuração: MESSAGE: {}".format(message),
            friendly_message="Erro de configuração.",
            http_status=500)
