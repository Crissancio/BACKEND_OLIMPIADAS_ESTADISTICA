from fastapi import Request
from fastapi.responses import JSONResponse


class NotFoundError(Exception):
    pass


class ValidationError(Exception):
    pass


class ConflictError(Exception):
    pass


class BusinessRuleError(Exception):
    pass


def _error_response(message: str, status_code: int) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"success": False, "error": message})


def register_exception_handlers(app):
    @app.exception_handler(NotFoundError)
    async def not_found_error_handler(request: Request, exc: NotFoundError):
        return _error_response(str(exc), 404)

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        return _error_response(str(exc), 400)

    @app.exception_handler(ConflictError)
    async def conflict_error_handler(request: Request, exc: ConflictError):
        return _error_response(str(exc), 409)

    @app.exception_handler(BusinessRuleError)
    async def business_rule_error_handler(request: Request, exc: BusinessRuleError):
        return _error_response(str(exc), 422)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        return _error_response("Error interno del servidor", 500)
