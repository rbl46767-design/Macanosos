class MacanososError(Exception):
    """Excepción base del proyecto."""


class ConfigurationError(MacanososError):
    """Error de configuración."""


class StorageError(MacanososError):
    """Error de almacenamiento."""


class ActivityError(MacanososError):
    """Error relacionado con actividades."""


class ValidationError(MacanososError):
    """Error de validación."""