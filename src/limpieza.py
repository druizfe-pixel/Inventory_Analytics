import pandas as pd
import logging
import unicodedata
import numpy as pd

from src.constants import (
    CODIGO,
    DESCRIPCION,
    FAMILIA,
    GRUPO,
    LINEA,
    VR_UNIT,
    COSTO_ORDENAR,
    COSTO_ALMACENAR,
    INVENTARIO,
    PEDIDOS,
    WIP
)

COLUMNAS_OBLIGATORIAS = [
    CODIGO,
    DESCRIPCION,
    FAMILIA,
    GRUPO,
    LINEA,
    COSTO_ORDENAR,
    COSTO_ALMACENAR,
    VR_UNIT,
    INVENTARIO,
    PEDIDOS,
    WIP,
]

MAPEO_COLUMNAS = {
    "Código": "codigo",
    "Descripción": "descripcion",
    "Familia": "familia",
    "Grupo": "grupo",
    "Línea": "linea",
    "Costo Ordenar": "costo_ordenar",
    "Costo Almacenar": "costo_almacenar",
    "Vr Unit": "vr_unit",
    "Inventario": "inventario",
    "Pedidos": "pedidos",
    "WIP Planta": "wip_planta",
}
#--------------------------------------------------------------------

def renombrar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renombra únicamente las columnas principales del negocio.
    """

    df = df.rename(columns=MAPEO_COLUMNAS)

    logger.info("Columnas principales renombradas.")

    return df

logger = logging.getLogger(__name__)

##---------------------------------------------------------------------

def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ejecuta todas las tareas de limpieza.
    """

    df = renombrar_columnas(df)

    validar_columnas(df)

    validar_duplicados(df)

    return df
#----------------------------------------------------------------------


def eliminar_duplicados_codigo(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina códigos duplicados conservando el registro
    con mayor cantidad de información útil.

    Criterios:

    1. Mayor número de meses con demanda.
    2. Mayor demanda acumulada.
    3. Mayor inventario.
    """

    df = df.copy()

    # ---------------------------------------
    # Normalizar código
    # ---------------------------------------

    df["codigo"] = (
        df["codigo"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # ---------------------------------------
    # Columnas de demanda
    # ---------------------------------------

    excluir = {
        "codigo",
        "descripcion",
        "familia",
        "grupo",
        "linea",
        "costo_ordenar",
        "costo_almacenar",
        "vr_unit",
        "inventario",
        "pedidos",
        "wip_planta"
    }

    columnas_demanda = [
        c
        for c in df.columns
        if c not in excluir
    ]

    # ---------------------------------------
    # Score de calidad
    # ---------------------------------------

    df["meses_con_demanda"] = (
        df[columnas_demanda]
        .fillna(0)
        .ne(0)
        .sum(axis=1)
    )

    df["demanda_total"] = (
        df[columnas_demanda]
        .fillna(0)
        .abs()
        .sum(axis=1)
    )

    df["score_calidad"] = (

        df["meses_con_demanda"] * 100000

        + df["demanda_total"]

        + (df["inventario"] > 0).astype(int) * 100

        + (df["vr_unit"] > 0).astype(int) * 100

    )

    # ---------------------------------------
    # Conservar mejor registro
    # ---------------------------------------

    df = (
        df.sort_values(
            "score_calidad",
            ascending=False
        )
        .drop_duplicates(
            subset="codigo",
            keep="first"
        )
    )

    # ---------------------------------------
    # Eliminar columnas auxiliares
    # ---------------------------------------

    df.drop(
        columns=[
            "meses_con_demanda",
            "demanda_total",
            "score_calidad"
        ],
        inplace=True
    )

    df.reset_index(
        drop=True,
        inplace=True
    )

    return df

#----------------------------------------------------------------------
def validar_columnas(df: pd.DataFrame) -> None:
    """
    Verifica que existan todas las columnas necesarias
    para ejecutar el proyecto.
    """

    faltantes = sorted(
        set(COLUMNAS_OBLIGATORIAS) - set(df.columns)
    )

    if faltantes:
        raise ValueError(
            f"Faltan las siguientes columnas: {faltantes}"
        )

    #logger = logging.getLogger(__name__)

    logger.info("Validación de columnas completada.")

#----------------------------------------------------------------------


def validar_duplicados(df: pd.DataFrame) -> None:
    """
    Verifica si existen códigos de producto repetidos.
    """

    duplicados = df[df[CODIGO].duplicated(keep=False)]

    if duplicados.empty:
        logger.info("No se encontraron códigos duplicados.")
        return

    logger.warning(
        f"Se encontraron {duplicados[CODIGO].nunique()} códigos duplicados."
    )

    codigos = (
        duplicados[CODIGO]
        .astype(str)
        .str.strip()
        .unique()
    )

    logger.warning(
        "Códigos duplicados: %s",
        sorted(codigos)
    )
