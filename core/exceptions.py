class AppException(Exception):
    """Excepción base de la aplicación, de esta heredan todas"""
    def __init__(self, message: str, detail: str = None):
        self.message = message
        self.detail = detail
        super().__init__(self.message)

# Excepciones de negocio
class BusinessError(AppException):
    """Error de reglas de negocio Ej. No se puede eliminar un producto con stock disponible"""
    pass

class NotFoundError(BusinessError):
    """Recurso no encontrado"""
    pass

class ConflictError(BusinessError):
    """Conflicto con estado actual (ej: duplicado)"""
    pass

class ValidationError(BusinessError):
    """Error de validación de datos"""
    pass

# Excepciones técnicas
class DatabaseError(AppException):
    """Error en operación de base de datos"""
    pass

class ConfigurationError(AppException):
    """Error de configuración"""
    pass