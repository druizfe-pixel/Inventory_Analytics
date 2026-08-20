import logging
import numpy as np
import pandas as pd
from src.utilidades import validar_columnas
from src.constants import (
    NIVELES_SERVICIO,
    COLUMNAS_DESVIACION,
    COLUMNAS_LEAD_TIME,
    COLUMNAS_STOCK_SEGURIDAD,
)

from src.config import (
    LEAD_TIME_DEFAULT,
    NIVEL_SERVICIO_DEFAULT,
)

from src.config import (
    LEAD_TIME_DEFAULT,
    NIVEL_SERVICIO_DEFAULT,
    DIAS_MES,
)

from src.config import (
    DIAS_ANIO,
    DIAS_MES
)

logger = logging.getLogger(__name__)



def agregar_lead_time(
    df: pd.DataFrame,
    lead_time: int = LEAD_TIME_DEFAULT,
) -> pd.DataFrame:
    """
    Agrega el Lead Time (días).
    """

    df["lead_time"] = lead_time

    logger.info(
        "Lead Time configurado en %s días.",
        lead_time,
    )

    return df


def agregar_nivel_servicio(
    df: pd.DataFrame,
    nivel_servicio: float = NIVEL_SERVICIO_DEFAULT,
) -> pd.DataFrame:
    """
    Agrega el nivel de servicio y el valor Z.
    """

    if nivel_servicio not in NIVELES_SERVICIO:
        raise ValueError(
            f"Nivel de servicio no soportado: {nivel_servicio}"
        )

    df["nivel_servicio"] = nivel_servicio
    df["valor_z"] = NIVELES_SERVICIO[nivel_servicio]

    
    return df

def calcular_desviacion_diaria(
    df: pd.DataFrame,
    dias_mes: float = DIAS_MES,
) -> pd.DataFrame:
    """
    Calcula la desviación estándar diaria de la demanda.
    """

    validar_columnas(
        df,
        [
            "demanda_anual",
            "desviacion_demanda",
        ],
    )

    mascara = (
        (df["demanda_anual"] > 0)
        &
        (df["desviacion_demanda"] > 0)
    )

    df["desviacion_diaria"] = np.nan

    df.loc[
        mascara,
        "desviacion_diaria"
    ] = (
        df.loc[
            mascara,
            "desviacion_demanda"
        ]
        /
        np.sqrt(dias_mes)
    )

    return df

def calcular_desviacion_lead_time(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcula la desviación estándar durante el Lead Time.
    """

    validar_columnas(
        df,
        [
            "desviacion_diaria",
            "lead_time",
        ],
    )

    mascara = (
        (df["desviacion_diaria"] > 0)
        &
        (df["lead_time"] > 0)
    )

    df["desviacion_lead_time"] = np.nan

    df.loc[
        mascara,
        "desviacion_lead_time"
    ] = (
        df.loc[
            mascara,
            "desviacion_diaria"
        ]
        *
        np.sqrt(
            df.loc[
                mascara,
                "lead_time"
            ]
        )
    )

    return df

def calcular_stock_seguridad(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcula el Stock de Seguridad.
    """

    validar_columnas(
        df,
        [
            "valor_z",
            "desviacion_lead_time",
        ],
    )

    mascara = (
        (df["valor_z"] > 0)
        &
        (df["desviacion_lead_time"] > 0)
    )

    df["stock_seguridad"] = np.nan

    df.loc[
        mascara,
        "stock_seguridad"
    ] = (
        df.loc[
            mascara,
            "valor_z"
        ]
        *
        df.loc[
            mascara,
            "desviacion_lead_time"
        ]
    )

    df["stock_seguridad"] = (
        df["stock_seguridad"]
        .round(0)
    )

    return df

def resumen_stock_seguridad(
    df: pd.DataFrame,
) -> None:
    """
    Muestra estadísticas del Stock de Seguridad.
    """

    columnas = [
        "lead_time",
        "nivel_servicio",
        "valor_z",
        "desviacion_diaria",
        "desviacion_lead_time",
        "stock_seguridad",
    ]

    validar_columnas(
        df,
        columnas,
    )

    df_validos = df[
        df["stock_seguridad"].notna()
    ]

    