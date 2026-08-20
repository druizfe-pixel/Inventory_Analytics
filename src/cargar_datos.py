"""
Módulo de carga de datos.

Proyecto:
Inventory Analytics

Autor:
Daniel Ruiz
"""

from pathlib import Path
import logging

import pandas as pd

from src.config import INVENTARIO
from src.config import UBICACIONES

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def cargar_excel(ruta: Path) -> pd.DataFrame:
    """
    Lee un archivo Excel.
    """

    if not ruta.exists():
        raise FileNotFoundError(f"No existe:\n{ruta}")

    logging.info(f"Leyendo archivo: {ruta.name}")

    return pd.read_excel(ruta)


def cargar_inventario() -> pd.DataFrame:

    return cargar_excel(INVENTARIO)


def cargar_ubicaciones() -> pd.DataFrame:

    return cargar_excel(UBICACIONES)



def validar_dataframe(df: pd.DataFrame, nombre: str):

    logging.info("="*60)

    logging.info(f"DATASET : {nombre}")

    logging.info(f"Filas : {df.shape[0]}")

    logging.info(f"Columnas : {df.shape[1]}")

    logging.info(f"Nulos : {df.isnull().sum().sum()}")

    logging.info(f"Duplicados : {df.duplicated().sum()}")

    logging.info("="*60)

    COLUMNAS_PERMITEN_NULOS = [
        "eoq",
        "stock_seguridad",
        "punto_reorden",
    ]


def resumen(df: pd.DataFrame):

    print(df.info())

    print()

    print(df.describe(include="all"))

    print()

    print(df.head())