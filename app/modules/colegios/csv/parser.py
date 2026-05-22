import pandas as pd

from app.modules.colegios.colegio_schema import (
    CSVImportErrorDTO,
    CSVImportResultDTO,
    ColegioCSVImportDTO,
    DirectorCSVImportDTO,
)

from app.modules.colegios.csv.constants import (
    COLUMNAS_REQUERIDAS,
)

from app.modules.colegios.csv.exceptions import (
    InvalidDirectorError,
    MissingColumnsError,
)

from app.modules.colegios.csv.normalizers import (
    limpiar_telefono,
    normalizar_dependencia,
    normalizar_turno,
    normalize_column,
    normalize_text,
)

from app.modules.colegios.csv.validators import (
    validar_codigo,
    validar_nombre,
    validar_telefono,
)


# =========================================================
# PARSEAR DIRECTORES
# =========================================================

def parsear_directores(
    nombres_raw,
    telefono_1,
    telefono_2
):

    directores = []
    lista = nombres_raw.split(";")
    for director in lista:
        director = normalize_text(
            director
        )
        if not director:
            continue

        partes = director.split()

        # =================================================
        # CASO:
        # PATERNO + NOMBRE
        # =================================================

        if len(partes) == 2:
            paterno = partes[0]
            materno = ""
            nombres = partes[1]

        # =================================================
        # CASO:
        # PATERNO + MATERNO + NOMBRES
        # =================================================

        elif len(partes) >= 3:
            paterno = partes[0]
            materno = partes[1]
            nombres = " ".join(
                partes[2:]
            )

        # =================================================
        # ERROR
        # =================================================

        else:
            raise InvalidDirectorError(
                f"No se pudo dividir correctamente "
                f"el nombre del director: '{director}'"
            )

        directores.append(

            DirectorCSVImportDTO(
                telefono_1=telefono_1,
                telefono_2=telefono_2,
                nombres=nombres,
                paterno=paterno,
                materno=materno
            )
        )

    # =====================================================
    # VALIDAR DIRECTORES
    # =====================================================

    if not directores:
        raise InvalidDirectorError(
            "No se encontraron directores válidos"
        )
    return directores


# =========================================================
# PARSE CSV
# =========================================================

def parse_csv_colegios(
    file,
    departamento: str
):
    # =====================================================
    # LEER CSV
    # =====================================================

    try:
        df = pd.read_csv(
            file,
            dtype=str
        )

    except Exception as e:
        raise Exception(
            f"Error leyendo CSV: {str(e)}"
        )

    # =====================================================
    # NORMALIZAR COLUMNAS
    # =====================================================

    df.columns = [
        normalize_column(c)
        for c in df.columns
    ]

    # =====================================================
    # VALIDAR COLUMNAS
    # =====================================================

    faltantes = [
        c
        for c in COLUMNAS_REQUERIDAS
        if c not in df.columns
    ]

    if faltantes:
        raise MissingColumnsError(
            f"Faltan columnas requeridas: "
            f"{faltantes}"
        )

    # =====================================================
    # RESULTADOS
    # =====================================================

    validos = []
    errores = []
    filas_error_csv = []
    codigos_vistos = set()

    # =====================================================
    # ITERAR FILAS
    # =====================================================

    for index, row in df.iterrows():

        fila_excel = index + 2

        try:
            # =================================================
            # CODIGO
            # =================================================

            codigo = normalize_text(
                row["codigo"]
            )
            validar_codigo(codigo)
            
            if codigo in codigos_vistos:
                raise Exception(
                    f"Código duplicado en CSV: '{codigo}'"
                )
            codigos_vistos.add(codigo)

            # =================================================
            # NOMBRE
            # =================================================

            nombre = str(
                row["nombre"]
            ).strip()
            validar_nombre(nombre)

            # =================================================
            # DEPENDENCIA
            # =================================================

            tipo = normalizar_dependencia(
                row["dependencia"]
            )

            # =================================================
            # TURNO
            # =================================================

            turno = normalizar_turno(
                row["turno"]
            )

            # =================================================
            # TELEFONOS
            # =================================================

            telefono_1 = limpiar_telefono(
                row["telefono_1"]
            )
            telefono_2 = limpiar_telefono(
                row["telefono_2"]
            )
            validar_telefono(
                telefono_1
            )
            validar_telefono(
                telefono_2
            )

            # =================================================
            # DIRECTORES
            # =================================================

            directores = parsear_directores(
                str(
                    row[
                        "apellidos_y_nombres_del_director"
                    ]
                ).strip(),
                telefono_1,
                telefono_2
            )

            # =================================================
            # DTO FINAL
            # =================================================

            colegio = ColegioCSVImportDTO(
                codigo=int(codigo),
                nombre=nombre,
                tipo=tipo,
                turno=turno,
                departamento=departamento,
                municipio=str(
                    row["municipio"]
                ).strip(),
                calle=str(
                    row["direccion"]
                ).strip(),
                estado="REVISADO",
                directores=directores
            )

            validos.append(
                colegio
            )

        # =====================================================
        # ERRORES
        # =====================================================

        except Exception as e:
            error = CSVImportErrorDTO(

                fila=fila_excel,
                codigo=row.get(
                    "codigo",
                    None
                ),

                nombre=row.get(
                    "nombre",
                    None
                ),

                error=str(e)
            )

            errores.append(error)
            fila_error = row.to_dict()
            fila_error["fila_error"] = fila_excel
            fila_error["detalle_error"] = str(e)

            filas_error_csv.append(
                fila_error
            )

            

    return CSVImportResultDTO(
        validos=validos,
        errores=errores,
        filas_error_csv=filas_error_csv
    )