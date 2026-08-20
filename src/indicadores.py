import logging

import numpy as np
import pandas as pd

from src.config import (
    DIAS_ANIO,
    DIAS_MES    
)

logger = logging.getLogger(__name__)


def calcular_demanda_mensual(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcula la demanda promedio mensual.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """

    if "demanda_anual" not in df.columns:
        raise ValueError(
            "Debe ejecutar calcular_demanda_anual() antes."
        )

    df["demanda_mensual"] = (
        df["demanda_anual"] / 12
    )

    logger.info(
        "Demanda promedio mensual calculada."
    )

    return df

def calcular_demanda_diaria(
    df: pd.DataFrame,
    dias_anio: int = DIAS_ANIO,
) -> pd.DataFrame:
    """
    Calcula la demanda promedio diaria.
    """

    if "demanda_anual" not in df.columns:
        raise ValueError(
            "Debe ejecutar calcular_demanda_anual() antes."
        )

    df["demanda_diaria"] = (
        df["demanda_anual"] / dias_anio
    )

    logger.info("Demanda diaria calculada.")

    return df

def calcular_inventario_promedio(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcula el inventario promedio.
    """

    if "inventario" not in df.columns:
        raise ValueError(
            "No existe la columna 'inventario'."
        )

    df["inventario_promedio"] = (
        df["inventario"] / 2
    )

    logger.info("Inventario promedio calculado.")

    
    return df


def calcular_costo_mantenimiento_unitario(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcula el costo anual de mantenimiento por unidad (H).

    H = Valor Unitario × Tasa de mantenimiento
    """

    columnas = [
        "vr_unit",
        "costo_almacenar",
    ]

    faltantes = [
        col
        for col in columnas
        if col not in df.columns
    ]

    if faltantes:
        raise ValueError(
            f"Faltan columnas: {faltantes}"
        )

    mascara = (
        (df["vr_unit"] > 0)
        &
        (df["costo_almacenar"] > 0)
    )

    df["costo_mantenimiento_unitario"] = np.nan

    df.loc[
        mascara,
        "costo_mantenimiento_unitario"
    ] = (
        df.loc[mascara, "vr_unit"]
        *
        df.loc[mascara, "costo_almacenar"]
    )

    logger.info("Costo anual de mantenimiento unitario calculado.")

    return df

