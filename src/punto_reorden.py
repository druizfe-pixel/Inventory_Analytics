import logging
import numpy as np
import pandas as pd

from src.utilidades import validar_columnas
from src.constants import (
    COLUMNAS_PUNTO_REORDEN,
)

logger = logging.getLogger(__name__)


def calcular_punto_reorden(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcula el Punto de Reorden.
    """

    validar_columnas(
        df,
        COLUMNAS_PUNTO_REORDEN,
    )

    mascara = (
        (df["demanda_anual"] > 0)
        &
        (df["demanda_diaria"] >= 0)
        &
        (df["lead_time"] > 0)
        &
        (df["stock_seguridad"].notna())
    )

    df["punto_reorden"] = np.nan

    df.loc[
        mascara,
        "punto_reorden",
    ] = (
        (
            df.loc[
                mascara,
                "demanda_diaria",
            ]
            *
            df.loc[
                mascara,
                "lead_time",
            ]
        )
        +
        df.loc[
            mascara,
            "stock_seguridad",
        ]
    )

    df["punto_reorden"] = (
        df["punto_reorden"]
        .round(0)
    )

    return df


def resumen_punto_reorden(
    df: pd.DataFrame,
) -> None:
    """
    Muestra estadísticas del Punto de Reorden.
    """

    columnas = [
        "demanda_diaria",
        "lead_time",
        "stock_seguridad",
        "punto_reorden",
    ]

    validar_columnas(
        df,
        columnas,
    )

    df_validos = df[
        df["punto_reorden"].notna()
    ]

    