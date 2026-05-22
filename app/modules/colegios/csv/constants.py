COLUMNAS_REQUERIDAS = [

    "municipio",

    "codigo",

    "nombre",

    "dependencia",

    "turno",

    "direccion",

    "apellidos_y_nombres_del_director",

    "telefono_1",

    "telefono_2"
]

# =========================================================
# DEPENDENCIAS
# =========================================================

DEPENDENCIA_MAP = {

    # PUBLICO
    "PUBLICA": "PUBLICO",
    "PUBLICO": "PUBLICO",
    "PUB": "PUBLICO",
    "FISCAL": "PUBLICO",

    # PRIVADO
    "PRIVADA": "PRIVADO",
    "PRIVADO": "PRIVADO",
    "PARTICULAR": "PRIVADO",

    # CONVENIO
    "CONVENIO": "CONVENIO",
    "DE CONVENIO": "CONVENIO",
    "CONV": "CONVENIO"
}

# =========================================================
# TURNOS
# =========================================================

TURNO_MAP = {

    # MAÑANA
    "MANANA": "MAÑANA",
    "M": "MAÑANA",
    "MATUTINO": "MAÑANA",
    "AM": "MAÑANA",

    # TARDE
    "TARDE": "TARDE",
    "T": "TARDE",
    "VESPERTINO": "TARDE",
    "PM": "TARDE",

    # NOCHE
    "NOCHE": "NOCHE",
    "N": "NOCHE",
    "NOCTURNO": "NOCHE"
}

# =========================================================
# TELEFONOS NULOS
# =========================================================

TELEFONOS_NULOS = {

    "",
    "-",
    "--",
    ".",
    "..",

    "N/S",
    "S/N",
    "SN",

    "NO",
    "NO TIENE",
    "SIN",
    "SIN NUMERO",
    "SIN TELEFONO",

    "NINGUNO",
    "NULL",
    "NULO",
    "VACIO",

    "0"
}