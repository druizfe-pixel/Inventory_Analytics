import logging
import numpy as np
import pandas as pd
logger = logging.getLogger(__name__)


import logging
import numpy as np

logger = logging.getLogger(__name__)


def calcular_distancia(df):
    """
    Calcula la distancia desde el despacho (0,0,0)
    hasta cada ubicación.
    """

    columnas = ["X", "Y", "Z"]

    for columna in columnas:

        if columna not in df.columns:
            raise ValueError(
                f"No existe la columna {columna}"
            )

        df[columna] = (
            df[columna]
            .astype(str)
            .str.replace(",", ".")
            .astype(float)
        )

    df["distancia_despacho"] = np.sqrt(
        df["X"]**2 +
        df["Y"]**2 +
        df["Z"]**2
    )

    df["distancia_despacho"] = df["distancia_despacho"].round(2)

    logger.info("Distancia al despacho calculada.")
    logger.info(
        "Distancia promedio: %.2f m",
        df["distancia_despacho"].mean()
    )

    return df

def integrar_ubicaciones(
    inventario,
    ubicaciones
):
    """
    Integra las coordenadas de las ubicaciones al
    DataFrame de inventario para el análisis de
    slotting.

    Ambos DataFrames deben llegar previamente
    normalizados.
    """

    slotting_df = inventario.merge(
        ubicaciones,
        on="codigo",
        how="left"
    )

    encontrados = slotting_df["X"].notna().sum()

    logger.info(
        "Productos con ubicación: %s",
        encontrados
    )

    logger.info(
        "Productos sin ubicación: %s",
        len(slotting_df) - encontrados
    )

    return slotting_df


def rankear_ubicaciones(df):
    """
    Genera un ranking de las ubicaciones según su cercanía
    al punto de despacho.
    """

    df = df.copy()

    # Ordenar únicamente para facilitar la lectura
    df = df.sort_values(
        "distancia_despacho",
        ascending=True,
        na_position="last"
    ).reset_index(drop=True)

    # Inicializar la columna
    df["ranking_ubicacion"] = np.nan

    # Solo las ubicaciones válidas reciben ranking
    mascara = df["distancia_despacho"].notna()

    df["ranking_ubicacion"] = pd.NA

    df.loc[mascara, "ranking_ubicacion"] = (
        df.loc[mascara, "distancia_despacho"]
        .rank(method="dense")
        .astype("Int64")
    )

    logger.info("Ranking de ubicaciones calculado.")

    return df

import logging

logger = logging.getLogger(__name__)


def recomendar_ubicacion(df):
    """
    Recomienda una acción de ubicación según el estado del slotting.
    """

    # Valor por defecto
    df["ubicacion_recomendada"] = "Mantener"

    # ==========================================
    # Productos que requieren movimiento urgente
    # ==========================================

    condicion = (
        df["estado_slotting"] == "Mover urgente"
    )

    df.loc[
        condicion,
        "ubicacion_recomendada"
    ] = "Reubicar Zona A"

    # ==========================================
    # Productos que requieren movimiento
    # ==========================================

    condicion = (
        df["estado_slotting"] == "Mover"
    )

    df.loc[
        condicion,
        "ubicacion_recomendada"
    ] = "Reubicar Zona B"

    # ==========================================
    # Productos aceptables
    # ==========================================

    condicion = (
        df["estado_slotting"] == "Aceptable"
    )

    df.loc[
        condicion,
        "ubicacion_recomendada"
    ] = "Evaluar"

    # ==========================================
    # Productos óptimos
    # ==========================================

    condicion = (
        df["estado_slotting"] == "Óptimo"
    )

    df.loc[
        condicion,
        "ubicacion_recomendada"
    ] = "Mantener"

    logger.info("Ubicaciones recomendadas calculadas.")

    return df


def evaluar_slotting(df):
    """
    Evalúa si la ubicación actual del producto es adecuada
    según su prioridad logística y el ranking de la ubicación.
    """

    df = df.copy()

    # ==========================================
    # Estado por defecto
    # ==========================================

    df["estado_slotting"] = "Sin ubicación"

    # Solo evaluar productos con ranking válido
    mascara = df["ranking_ubicacion"].notna()

    # ==================================================
    # PRIORIDAD MUY ALTA
    # ==================================================

    condicion = (
        mascara &
        (df["prioridad_slotting"] == "Muy Alta") &
        (df["ranking_ubicacion"] <= 100)
    )

    df.loc[condicion, "estado_slotting"] = "Óptimo"

    condicion = (
        mascara &
        (df["prioridad_slotting"] == "Muy Alta") &
        (df["ranking_ubicacion"] > 100) &
        (df["ranking_ubicacion"] <= 250)
    )

    df.loc[condicion, "estado_slotting"] = "Aceptable"

    condicion = (
        mascara &
        (df["prioridad_slotting"] == "Muy Alta") &
        (df["ranking_ubicacion"] > 250)
    )

    df.loc[condicion, "estado_slotting"] = "Mover urgente"

    # ==================================================
    # PRIORIDAD ALTA
    # ==================================================

    condicion = (
        mascara &
        (df["prioridad_slotting"] == "Alta") &
        (df["ranking_ubicacion"] <= 250)
    )

    df.loc[condicion, "estado_slotting"] = "Óptimo"

    condicion = (
        mascara &
        (df["prioridad_slotting"] == "Alta") &
        (df["ranking_ubicacion"] > 250) &
        (df["ranking_ubicacion"] <= 500)
    )

    df.loc[condicion, "estado_slotting"] = "Aceptable"

    condicion = (
        mascara &
        (df["prioridad_slotting"] == "Alta") &
        (df["ranking_ubicacion"] > 500)
    )

    df.loc[condicion, "estado_slotting"] = "Mover"

    # ==================================================
    # PRIORIDAD MEDIA
    # ==================================================

    condicion = (
        mascara &
        (df["prioridad_slotting"] == "Media") &
        (df["ranking_ubicacion"] <= 600)
    )

    df.loc[condicion, "estado_slotting"] = "Óptimo"

    condicion = (
        mascara &
        (df["prioridad_slotting"] == "Media") &
        (df["ranking_ubicacion"] > 600) &
        (df["ranking_ubicacion"] <= 900)
    )

    df.loc[condicion, "estado_slotting"] = "Aceptable"

    condicion = (
        mascara &
        (df["prioridad_slotting"] == "Media") &
        (df["ranking_ubicacion"] > 900)
    )

    df.loc[condicion, "estado_slotting"] = "Mover"

    # ==================================================
    # PRIORIDAD BAJA
    # ==================================================

    condicion = (
        mascara &
        (df["prioridad_slotting"] == "Baja")
    )

    df.loc[condicion, "estado_slotting"] = "Correcto"

    # ==================================================
    # PRODUCTOS EXCLUIDOS
    # ==================================================

    condicion = (
        df["prioridad_slotting"] == "Excluir"
    )

    df.loc[condicion, "estado_slotting"] = "No evaluar"

    logger.info("Estado de slotting calculado.")

    logger.info(
        "\n%s",
        df["estado_slotting"].value_counts(dropna=False)
    )

    return df


def rankear_productos(df):
    """
    Genera el ranking logístico de los SKU.
    """

    productos = (
        df.drop_duplicates(
            subset="codigo",
            keep="first"
        )
        .copy()
    )

    logger.info(
        "Productos únicos: %s",
        len(productos)
    )

    productos = productos.sort_values(
        by=[
            "prioridad_slotting",
            "demanda_anual",
            "valor_consumo"
        ],
        ascending=[
            True,
            False,
            False
        ]
    ).reset_index(drop=True)

    productos["ranking_producto"] = (
        productos.index + 1
    )

    logger.info(
        "Ranking de productos calculado."
    )

    logger.info(
        "Productos únicos: %s",
        len(productos)
    )

    print(productos[[
        "codigo",
        "prioridad_slotting",
        "ranking_producto"
    ]].head(20))


    return productos


def obtener_ubicaciones_disponibles(layout):
    """
    Devuelve únicamente las ubicaciones utilizables
    para realizar una optimización.
    """

    disponibles = layout.copy()

    # Solo ubicaciones existentes
    disponibles = disponibles[
        disponibles["X"].notna()
    ]

    # Ordenadas de la mejor a la peor
    disponibles = disponibles.sort_values(
        "ranking_ubicacion"
    )

    disponibles = disponibles.reset_index(
        drop=True
    )

    logger.info(
        "Ubicaciones disponibles: %s",
        len(disponibles)
    )

    return disponibles


def crear_maestro_ubicaciones(layout):
    """
    Genera el catálogo maestro de ubicaciones físicas
    del almacén.

    Una fila = una ubicación.
    """

    import pandas as pd
    import numpy as np

    columnas = [
        "ranking_ubicacion",
        "X",
        "Y",
        "Z",
        "distancia_despacho"
    ]

    maestro = (
        layout[columnas]
        .dropna(subset=["ranking_ubicacion"])
        .drop_duplicates(subset="ranking_ubicacion")
        .copy()
    )

    # Tipos de datos
    for col in columnas:

        maestro[col] = pd.to_numeric(
            maestro[col],
            errors="coerce"
        )

    maestro = maestro.dropna()

    # Zona física

    maestro["zona_fisica"] = np.select(
        [
            maestro["distancia_despacho"] <= 10,
            maestro["distancia_despacho"] <= 20,
            maestro["distancia_despacho"] <= 30
        ],
        [
            "A",
            "B",
            "C"
        ],
        default="D"
    )

    # Pasillo

    maestro["pasillo"] = maestro["X"].astype(int)

    # Nivel

    maestro["nivel"] = np.select(
        [
            maestro["Z"] <= 3,
            maestro["Z"] <= 6
        ],
        [
            "Bajo",
            "Medio"
        ],
        default="Alto"
    )

    # Tipo

    maestro["tipo_posicion"] = np.where(
        maestro["Z"] <= 1.5,
        "Piso",
        "Rack"
    )

    # Clave sustituta

    maestro.insert(
        0,
        "id_ubicacion",
        range(1, len(maestro) + 1)
    )

    return maestro.sort_values(
        "ranking_ubicacion"
    ).reset_index(drop=True)