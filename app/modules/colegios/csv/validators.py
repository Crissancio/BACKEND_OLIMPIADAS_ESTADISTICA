import re

from app.modules.colegios.csv.exceptions import (
    InvalidCodigoError,
    InvalidNombreError,
    InvalidTelefonoError,
)

def validar_codigo(codigo):
    if not str(codigo).isdigit():
        raise InvalidCodigoError(f"Código inválido: '{codigo}'")


def validar_nombre(nombre):
    if not nombre:
        raise InvalidNombreError("Nombre vacío")

def validar_telefono(phone):
    if phone is None:
        return
    pattern = r"^[0-9+\-\s]+$"
    if not re.fullmatch(pattern, phone):
        raise InvalidTelefonoError(f"Telefono inválido: '{phone}'")