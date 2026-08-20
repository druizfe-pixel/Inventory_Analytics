import logging

import numpy as np
import pandas as pd
from src.utilidades import validar_columnas

from src.constants import (
    COLUMNAS_EOQ,
    COLUMNAS_PEDIDOS,
    COLUMNAS_TIEMPO_PEDIDOS,
    COLUMNAS_COSTO_ORDENAR,
    COLUMNAS_COSTO_MANTENER,
    COLUMNAS_COSTO_TOTAL,
    COLUMNAS_REQUERIDAS,
    COLUMNAS_MANTENIMIENTO,
)


logger = logging.getLogger(__name__)



def validar_datos_eoq(
    df: pd.DataFrame,
) -> None:
    """
    Valida que existan las columnas necesarias para calcular EOQ.
    """

    validar_columnas(
        df,
        COLUMNAS_REQUERIDAS,
    )

    logger.info(
        "Datos validados para cálculo de EOQ."
    )


def calcular_eoq(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcula la Cantidad Económica de Pedido (EOQ).
    """

    validar_datos_eoq(df)

    mascara = (
        (df["demanda_anual"] > 0)
        &
        (df["costo_ordenar"] > 0)
        &
        (df["costo_mantenimiento_unitario"] > 0)
    )

    df["eoq"] = np.nan

    df.loc[
        mascara,
        "eoq"
    ] = np.sqrt(
        (
            2
            * df.loc[mascara, "demanda_anual"]
            * df.loc[mascara, "costo_ordenar"]
        )
        /
        df.loc[
            mascara,
            "costo_mantenimiento_unitario"
        ]
    )

    df["eoq"] = (
        df["eoq"]
        .round(0)
    )

    
    return df

def calcular_numero_pedidos(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcula el número óptimo de pedidos por año.
    """

    # if "eoq" not in df.columns:
    #     raise ValueError(
    #         "Debe ejecutar calcular_eoq() primero."
    #     )
    validar_columnas(
        df,
        ["eoq", "demanda_anual"],
    )

    mascara = (
        df["eoq"] > 0
    )

    df["pedidos_anuales"] = np.nan

    df.loc[
        mascara,
        "pedidos_anuales"
    ] = (
        df.loc[mascara, "demanda_anual"]
        /
        df.loc[mascara, "eoq"]
    )

    df["pedidos_anuales"] = (
        df["pedidos_anuales"]
        .round(2)
    )

    

    return df

def calcular_tiempo_entre_pedidos(
    df: pd.DataFrame,
    dias_laborales: int = 365,
) -> pd.DataFrame:
    """
    Calcula el tiempo promedio entre pedidos.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con la información del inventario.

    dias_laborales : int, default=365
        Número de días considerados para el cálculo.

    Returns
    -------
    pd.DataFrame
        DataFrame con la columna 'dias_entre_pedidos'.
    """

    validar_columnas(
        df,
        ["pedidos_anuales"],
    )

   
    mascara = (
        df["pedidos_anuales"] > 0
    )

    df["dias_entre_pedidos"] = np.nan

    df.loc[
        mascara,
        "dias_entre_pedidos"
    ] = (
        dias_laborales
        /
        df.loc[
            mascara,
            "pedidos_anuales"
        ]
    )

    df["dias_entre_pedidos"] = (
        df["dias_entre_pedidos"]
        .round(1)
    )

    logger.info(
        "Tiempo entre pedidos calculado."
    )

    return df

def calcular_costo_ordenar_anual(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcula el costo anual de emitir pedidos.
    """

    validar_columnas(
        df,
        COLUMNAS_PEDIDOS,
    )

    mascara = (
        (df["pedidos_anuales"] > 0)
        &
        (df["costo_ordenar"] > 0)
    )

    df["costo_ordenar_anual"] = np.nan

    df.loc[
        mascara,
        "costo_ordenar_anual"
    ] = (
        df.loc[mascara, "pedidos_anuales"]
        *
        df.loc[mascara, "costo_ordenar"]
    )

    df["costo_ordenar_anual"] = (
        df["costo_ordenar_anual"]
        .round(2)
    )

    

    return df

def calcular_costo_mantener_anual(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcula el costo anual de mantener inventario.
    """

    validar_columnas(
        df,
        COLUMNAS_MANTENIMIENTO,
    )

    mascara = (
        (df["eoq"] > 0)
        &
        (df["costo_mantenimiento_unitario"] > 0)
    )

    df["costo_mantener_anual"] = np.nan

    df.loc[
        mascara,
        "costo_mantener_anual"
    ] = (
        (df.loc[mascara, "eoq"] / 2)
        *
        df.loc[
            mascara,
            "costo_mantenimiento_unitario"
        ]
    )

    df["costo_mantener_anual"] = (
        df["costo_mantener_anual"]
        .round(2)
    )

    return df

def calcular_costo_total_eoq(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcula el costo total anual del modelo EOQ.
    """
    validar_columnas(
        df,
        COLUMNAS_COSTO_TOTAL,        
    )

    mascara = (
        df["costo_ordenar_anual"].notna()
        &
        df["costo_mantener_anual"].notna()
    )

    df["costo_total_eoq"] = np.nan

    df.loc[
        mascara,
        "costo_total_eoq"
    ] = (
        df.loc[
            mascara,
            "costo_ordenar_anual"
        ]
        +
        df.loc[
            mascara,
            "costo_mantener_anual"
        ]
    )

    df["costo_total_eoq"] = (
        df["costo_total_eoq"]
        .round(2)
    )

    return df

def resumen_eoq(
    df: pd.DataFrame,
) -> None:
    """
    Muestra estadísticas básicas de los indicadores EOQ.
    """

    columnas = [
        "eoq",
        "pedidos_anuales",
        "dias_entre_pedidos",
        "costo_ordenar_anual",
        "costo_mantener_anual",
        "costo_total_eoq",
    ]

    validar_columnas(df, columnas)

    
