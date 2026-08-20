import logging
import pandas as pd
import numpy as np

from src.constants import CODIGO
from src.constants import (
    COSTO_ALMACENAR,
    VR_UNIT,
)

from src.config import (
    ABC_A,
    ABC_B
)

logger = logging.getLogger(__name__)

def obtener_columnas_demanda(df: pd.DataFrame):
    """
    Identifica automáticamente las columnas de demanda
    en valor y en unidades.
    """

    columnas = list(df.columns)

    inicio = columnas.index(COSTO_ALMACENAR) + 1
    fin = columnas.index(VR_UNIT)

    columnas_demanda = columnas[inicio:fin]

    demanda_valor = columnas_demanda[:12]

    demanda_unidades = columnas_demanda[12:]
    

    return {
        "valor": demanda_valor,
        "unidades": demanda_unidades,
    }


def calcular_demanda_anual(
    df: pd.DataFrame,
    demanda_unidades: list
) -> pd.DataFrame:
    """
    Calcula la demanda anual en unidades.
    """

    df["demanda_anual"] = (
        df[demanda_unidades]
        .sum(axis=1)
    )

    
    return df

def validar_demanda_xyz(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Marca los productos que pueden participar en la
    clasificación XYZ.

    Un producto es válido cuando su demanda anual es
    estrictamente mayor a cero.
    """

    df["demanda_valida_xyz"] = df["demanda_anual"] > 0

    
    return df


def calcular_valor_consumo(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula el valor anual consumido.
    """

    df["valor_consumo"] = (
        df["demanda_anual"] *
        df[VR_UNIT]
    )

    
    return df


def clasificacion_abc(
    df: pd.DataFrame,
    porcentaje_a: float = ABC_A,
    porcentaje_b: float = ABC_B,
) -> pd.DataFrame:
    """
    Calcula la clasificación ABC con base en el valor anual de consumo.
    """

    df = df.sort_values(
        by="valor_consumo",
        ascending=False
    ).copy()

    total = df["valor_consumo"].sum()

    df["porcentaje_valor"] = (
        df["valor_consumo"] / total
    )

    df["porcentaje_acumulado"] = (
        df["porcentaje_valor"].cumsum()
    )

    condiciones = [
        df["porcentaje_acumulado"] <= porcentaje_a,
        df["porcentaje_acumulado"] <= porcentaje_b,
    ]

    clases = ["A", "B"]

    df["abc"] = np.select(
        condiciones,
        clases,
        default="C"
    )

    return df

def calcular_demanda_promedio(
    df: pd.DataFrame,
    demanda_unidades: list,
) -> pd.DataFrame:
    """
    Calcula la demanda promedio mensual.
    """

    df["demanda_promedio"] = (
        df[demanda_unidades]
        .mean(axis=1)
    )

    
    return df


def calcular_desviacion_demanda(
    df: pd.DataFrame,
    demanda_unidades: list,
) -> pd.DataFrame:
    """
    Calcula la desviación estándar de la demanda mensual.
    """

    df["desviacion_demanda"] = (
        df[demanda_unidades]
        .std(axis=1)
    )

    return df


def calcular_coeficiente_variacion(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcula el coeficiente de variación de la demanda.
    """

    df["coeficiente_variacion"] = (
        df["desviacion_demanda"] /
        df["demanda_promedio"].replace(0, np.nan)
    )

    df["coeficiente_variacion"] = (
        df["coeficiente_variacion"]
        .fillna(0)
        .round(3)
    )

    return df

def clasificacion_xyz(
    df: pd.DataFrame,
    limite_x: float = 0.50,
    limite_y: float = 1.00,
) -> pd.DataFrame:
    """
    Clasifica los productos según el coeficiente
    de variación de la demanda.

    Los productos sin demanda positiva quedan
    marcados como 'N'.
    """

    df["xyz"] = "N"

    mascara = df["demanda_valida_xyz"]

    condiciones = [
        df.loc[mascara, "coeficiente_variacion"] <= limite_x,
        df.loc[mascara, "coeficiente_variacion"] <= limite_y,
    ]

    clases = ["X", "Y"]

    df.loc[mascara, "xyz"] = np.select(
        condiciones,
        clases,
        default="Z",
    )

    return df


def clasificacion_abcxyz(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Combina las clasificaciones ABC y XYZ.

    Los productos sin demanda positiva
    se clasifican como 'N'.
    """

    mascara = df["xyz"] != "N"

    df["abcxyz"] = "N"

    df.loc[mascara, "abcxyz"] = (
        df.loc[mascara, "abc"] +
        df.loc[mascara, "xyz"]
    )

    return df