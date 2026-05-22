import os
import uuid

import pandas as pd


TMP_DIR = "tmp/csv_errors"

os.makedirs(
    TMP_DIR,
    exist_ok=True
)


def generar_csv_errores(
    filas_error_csv: list[dict]
):

    if not filas_error_csv:
        return None

    df = pd.DataFrame(
        filas_error_csv
    )

    filename = (
        f"errores_"
        f"{uuid.uuid4().hex}.csv"
    )

    filepath = os.path.join(
        TMP_DIR,
        filename
    )

    df.to_csv(
        filepath,
        index=False,
        encoding="utf-8-sig"
    )

    return filepath

def obtener_csv_error_path(
    filename: str
):

    return os.path.join(
        TMP_DIR,
        filename
    )