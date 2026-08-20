import pandas as pd


def validar_columnas(
    df: pd.DataFrame,
    columnas: list[str],
) -> None:
    """
    Verifica que existan las columnas requeridas.
    """

    faltantes = [
        col
        for col in columnas
        if col not in df.columns
    ]

    if faltantes:
        raise ValueError(
            f"Faltan columnas: {faltantes}"
        )