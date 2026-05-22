import re

import pandas as pd

from unidecode import unidecode

from app.modules.colegios.csv.constants import (
    DEPENDENCIA_MAP,
    TELEFONOS_NULOS,
    TURNO_MAP,
)

from app.modules.colegios.csv.exceptions import (
    InvalidDependenciaError,
    InvalidTurnoError,
)


def normalize_text(text):

    if pd.isna(text):
        return ""

    text = str(text).strip()

    text = unidecode(text.upper())

    text = re.sub(r"\s+", " ", text)

    return text


def normalize_column(col):

    col = normalize_text(col)

    replacements = {
        " ": "_",
        "-": "_"
    }

    for old, new in replacements.items():
        col = col.replace(old, new)

    return col.lower()


# =========================================================
# TELEFONOS
# =========================================================

def limpiar_telefono(phone):

    if pd.isna(phone):
        return None

    phone = normalize_text(phone)

    if phone in TELEFONOS_NULOS:
        return None

    if not re.search(r"\d", phone):
        return None

    phone = re.sub(r"\s+", " ", phone)

    return phone

def normalizar_dependencia(valor):
    valor = normalize_text(valor)
    if valor not in DEPENDENCIA_MAP:
        raise InvalidDependenciaError(
            f"Dependencia inválida: '{valor}'"
        )
    return DEPENDENCIA_MAP[valor]


def normalizar_turno(valor):
    valor_original = valor
    valor = normalize_text(valor)
    partes = re.split(
        r"[\/,\-\+; ]+",
        valor
    )
    turnos_detectados = set()

    for parte in partes:
        parte = parte.strip()
        if not parte:
            continue
        
        if parte in TURNO_MAP:
            turnos_detectados.add(
                TURNO_MAP[parte]
            )

    if len(turnos_detectados) > 1:
        return "MIXTO"
    if len(turnos_detectados) == 1:
        return list(turnos_detectados)[0]
    raise InvalidTurnoError(
        f"Turno inválido: '{valor_original}'"
    )