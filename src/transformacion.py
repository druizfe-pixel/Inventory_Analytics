import logging
import pandas as pd

from src.constants import (
    CODIGO,
    COSTO_ORDENAR,
    COSTO_ALMACENAR,
    VR_UNIT,
    INVENTARIO,
    PEDIDOS,
    WIP,
)

logger = logging.getLogger(__name__)


def convertir_codigo(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte el código del producto a texto y
    lo normaliza para garantizar una llave única.

    Se realizan las siguientes transformaciones:

    - Convierte a texto.
    - Elimina espacios al inicio y al final.
    - Elimina espacios múltiples.
    - Convierte a MAYÚSCULAS.
    """

    df = df.copy()

    df[CODIGO] = (
        df[CODIGO]
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
        .str.upper()
    )

    logger.info(
        "Código convertido y normalizado correctamente."
    )

    return df

def convertir_porcentaje(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte el costo de almacenamiento de porcentaje a decimal.
    """

    df[COSTO_ALMACENAR] = (
        df[COSTO_ALMACENAR]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
        / 100
    )

    logger.info("Costo de almacenamiento convertido a decimal.")

    return df


def limpiar_moneda(serie: pd.Series) -> pd.Series:
    """
    Convierte una serie monetaria a tipo float.
    Si ya es numérica, solo rellena nulos.
    """
    if pd.api.types.is_numeric_dtype(serie):
        return serie.fillna(0).astype(float)

    return (
        serie.fillna(0)
             .astype(str)
             .str.replace("$", "", regex=False)
             .str.replace(" ", "", regex=False)
             .str.replace(".", "", regex=False)
             .str.replace(",", ".", regex=False)
             .astype(float)
    )

def convertir_monedas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte las columnas monetarias del DataFrame.
    """

    df[COSTO_ORDENAR] = limpiar_moneda(df[COSTO_ORDENAR])
    df[VR_UNIT] = limpiar_moneda(df[VR_UNIT])

    logger.info("Columnas monetarias convertidas.")
    
    return df


import logging
import pandas as pd

logger = logging.getLogger(__name__)


def transformar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ejecuta todas las transformaciones del DataFrame.
    """

    df = convertir_codigo(df)

    df = convertir_porcentaje(df)

    df = convertir_monedas(df)

    logger.info("Transformación de datos completada.")

    return df


def transformar_ubicaciones(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza las transformaciones necesarias para
    el maestro de ubicaciones.
    """

    df = convertir_codigo(df)

    logger.info(
        "Transformación de ubicaciones completada."
    )

    return df