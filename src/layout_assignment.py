import logging
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def rankear_productos(df):
    """
    Genera un ranking único de productos (SKU)
    para asignarles la mejor ubicación disponible.
    """

    productos = (
        df
        .drop_duplicates(
            subset="codigo",
            keep="first"
        )
        .copy()
    )

    prioridad = {
        "Muy Alta": 1,
        "Alta": 2,
        "Media": 3,
        "Baja": 4,
        "Excluir": 5,
        "Sin clasificar": 6,
    }

    productos["prioridad_num"] = (
        productos["prioridad_slotting"]
        .map(prioridad)
        .fillna(99)
    )

    productos = productos.sort_values(
        by=[
            "prioridad_num",
            "demanda_anual",
            "valor_consumo",
        ],
        ascending=[
            True,
            False,
            False,
        ],
    ).reset_index(drop=True)

    productos["ranking_producto"] = (
        productos.index + 1
    )

    logger.info(
        "Productos únicos para optimización: %s",
        len(productos)
    )

    logger.info("Ranking de productos calculado.")

    print(
        productos[
            [
                "codigo",
                "prioridad_slotting",
                "ranking_producto",
            ]
        ].head(20)
    )

    return productos



def asignar_ubicaciones(productos, ubicaciones):
    """
    Asigna la mejor ubicación disponible a cada SKU según
    el ranking del producto y el ranking de la ubicación.
    """

    productos = productos.copy()
    ubicaciones = ubicaciones.copy()

    # Ordenar productos
    productos = productos.sort_values(
        "ranking_producto"
    ).reset_index(drop=True)

    # Ordenar ubicaciones
    ubicaciones = ubicaciones.sort_values(
        "ranking_ubicacion"
    ).reset_index(drop=True)

    n = min(len(productos), len(ubicaciones))

    asignacion = productos.iloc[:n].copy()

    asignacion["ubicacion_actual"] = (
        asignacion["codigo"]
    )

    asignacion["X_nuevo"] = ubicaciones["X"].values[:n]
    asignacion["Y_nuevo"] = ubicaciones["Y"].values[:n]
    asignacion["Z_nuevo"] = ubicaciones["Z"].values[:n]

    asignacion["ranking_ubicacion_nueva"] = (
        ubicaciones["ranking_ubicacion"].values[:n]
    )

    logger.info(
        "Productos asignados: %s",
        len(asignacion)
    )

    return asignacion


def comparar_layout(productos, asignacion):
    """
    Compara la ubicación actual con la propuesta.
    """

    resultado = productos.merge(

        asignacion[
            [
                "codigo",
                "ranking_ubicacion_nueva",
                "X_nuevo",
                "Y_nuevo",
                "Z_nuevo"
            ]
        ],

        on="codigo",
        how="left"

    )

    resultado["mejora_ranking"] = (

        resultado["ranking_ubicacion"]
        -
        resultado["ranking_ubicacion_nueva"]

    )

    resultado["requiere_movimiento"] = (

        resultado["mejora_ranking"] > 0

    )

    logger.info(
        "Productos a mover: %s",
        resultado["requiere_movimiento"].sum()
    )

    return resultado


def calcular_score_movimiento(df):
    """
    Calcula el beneficio esperado de mover cada SKU.
    """

    df = df.copy()

    df["mejora_ranking"] = (
        df["ranking_ubicacion"]
        - df["ranking_ubicacion_nueva"]
    )

    df["mejora_ranking"] = (
        df["mejora_ranking"]
        .fillna(0)
        .clip(lower=0)
    )

    df["score_movimiento"] = (

        df["mejora_ranking"] *

        df["demanda_anual"]

    )

    logger.info(
        "Score de movimiento calculado."
    )

    return df

def generar_plan_reubicacion(layout):
    """
    Genera el plan definitivo de reubicación de SKU.

    El plan incluye:

    - Prioridad logística
    - Clasificación ABCXYZ
    - Picking recomendado
    - Ubicación actual
    - Nueva ubicación
    - Beneficio esperado
    """

    plan = layout[
        layout["estado_slotting"].isin(
            [
                "Mover urgente",
                "Mover"
            ]
        )
    ].copy()

    # =====================================
    # Selección de columnas
    # =====================================

    plan = plan[
        [
            # Identificación
            "codigo",
            "descripcion",
            "familia",
            "grupo",
            "linea",

            # Clasificación
            "abcxyz",
            "prioridad_slotting",
            "zona_recomendada",
            "tipo_picking",

            # Importancia del SKU
            "demanda_anual",
            "valor_consumo",

            # Ranking
            "ranking_producto",
            "ranking_ubicacion",
            "ranking_nuevo",

            # Ubicación actual
            "X",
            "Y",
            "Z",
            "distancia_despacho",

            # Nueva ubicación
            "X_nuevo",
            "Y_nuevo",
            "Z_nuevo",
            "distancia_nueva",

            # Beneficios
            "mejora_ranking",
            "ahorro_distancia",
            "score_movimiento",

            # Diagnóstico
            "estado_slotting",
            "ubicacion_recomendada"
        ]
    ].copy()

    # =====================================
    # Renombrar columnas
    # =====================================

    plan.rename(
        columns={
            "ranking_nuevo": "ranking_ubicacion_nueva",
            "distancia_despacho": "distancia_actual"
        },
        inplace=True
    )

    # =====================================
    # Ordenar por prioridad de movimiento
    # =====================================

    plan = plan.sort_values(
        by=[
            "score_movimiento",
            "mejora_ranking"
        ],
        ascending=[
            False,
            False
        ]
    ).reset_index(drop=True)

    # =====================================
    # Número secuencial del movimiento
    # =====================================

    plan.insert(
        0,
        "orden_movimiento",
        range(1, len(plan) + 1)
    )

    logger.info(
        "Plan de reubicación generado."
    )

    logger.info(
        "Movimientos a realizar: %s",
        len(plan)
    )

    return plan



def buscar_mejor_ubicacion(
    ubicaciones,
    zonas_preferidas
):
    """
    Busca la mejor ubicación disponible según
    el orden de zonas preferidas.
    """

    for zona in zonas_preferidas:

        disponibles = ubicaciones[
            ubicaciones["zona_fisica"] == zona
        ]

        if len(disponibles) > 0:

            indice = disponibles.index[0]

            ubicacion = disponibles.loc[indice]

            ubicaciones = ubicaciones.drop(indice)

            return ubicacion, ubicaciones

    return None, ubicaciones



def asignar_ubicacion_optima(
    layout,
    ubicaciones_disponibles
):
    """
    Asigna a cada SKU que requiere movimiento la mejor
    ubicación disponible según el ranking del producto.

    Calcula además:

    - Ranking nuevo
    - Nueva ubicación
    - Mejora de ranking
    - Ahorro de distancia
    """

    layout = layout.copy()

    ubicaciones = (
        ubicaciones_disponibles
        .copy()
        .sort_values(
            "ranking_ubicacion"
        )
        .reset_index(drop=True)
    )

    # =====================================
    # Columnas destino
    # =====================================

    layout["ranking_nuevo"] = np.nan

    layout["X_nuevo"] = np.nan
    layout["Y_nuevo"] = np.nan
    layout["Z_nuevo"] = np.nan

    layout["distancia_nueva"] = np.nan

    layout["zona_nueva"] = None
    layout["ubicacion_nueva"] = None

    layout["mejora_ranking"] = np.nan
    layout["ahorro_distancia"] = np.nan

    # =====================================
    # SKU que deben reubicarse
    # =====================================

    mover = layout[
        layout["estado_slotting"].isin(
            [
                "Mover urgente",
                "Mover"
            ]
        )
    ].copy()

    mover = mover.sort_values(
        "ranking_producto"
    )

    logger.info(
        "SKU a reubicar: %s",
        len(mover)
    )

    # =====================================
    # Validar disponibilidad
    # =====================================

    cantidad = min(
        len(mover),
        len(ubicaciones)
    )

    logger.info(
        "Ubicaciones disponibles: %s",
        len(ubicaciones)
    )

    logger.info(
        "Asignaciones posibles: %s",
        cantidad
    )

    # =====================================
    # Asignación uno a uno
    # =====================================

    for i in range(cantidad):

        indice_layout = mover.index[i]

        ubicacion = ubicaciones.iloc[i]

        # -----------------------------
        # Nueva ubicación
        # -----------------------------

        layout.loc[
            indice_layout,
            "ranking_nuevo"
        ] = ubicacion["ranking_ubicacion"]

        layout.loc[
            indice_layout,
            "X_nuevo"
        ] = ubicacion["X"]

        layout.loc[
            indice_layout,
            "Y_nuevo"
        ] = ubicacion["Y"]

        layout.loc[
            indice_layout,
            "Z_nuevo"
        ] = ubicacion["Z"]

        layout.loc[
            indice_layout,
            "distancia_nueva"
        ] = ubicacion["distancia_despacho"]

        # -----------------------------
        # Texto ubicación
        # -----------------------------

        texto = (
            f"X={ubicacion['X']} | "
            f"Y={ubicacion['Y']} | "
            f"Z={ubicacion['Z']}"
        )

        layout.loc[
            indice_layout,
            "zona_nueva"
        ] = texto

        layout.loc[
            indice_layout,
            "ubicacion_nueva"
        ] = texto

        # -----------------------------
        # Mejora ranking
        # -----------------------------

        layout.loc[
            indice_layout,
            "mejora_ranking"
        ] = (
            layout.loc[
                indice_layout,
                "ranking_ubicacion"
            ]
            -
            ubicacion["ranking_ubicacion"]
        )

        # -----------------------------
        # Ahorro distancia
        # -----------------------------

        layout.loc[
            indice_layout,
            "ahorro_distancia"
        ] = (
            layout.loc[
                indice_layout,
                "distancia_despacho"
            ]
            -
            ubicacion["distancia_despacho"]
        )

    logger.info(
        "Ubicaciones óptimas asignadas correctamente."
    )

    logger.info(
        "SKU reubicados: %s",
        cantidad
    )

    return layout


def validar_asignacion(layout):
    """
    Muestra un resumen de la asignación realizada.
    """

    asignados = layout[
        layout["ranking_nuevo"].notna()
    ].copy()

    logger.info("=" * 60)
    logger.info("VALIDACIÓN DE LA ASIGNACIÓN")
    logger.info("=" * 60)

    logger.info(
        "Productos reubicados: %s",
        len(asignados)
    )

    logger.info(
        "\n%s",
        asignados["zona_nueva"]
        .value_counts()
    )

    print(
        asignados[
            [
                "codigo",
                "prioridad_slotting",
                "ranking_producto",
                "zona_nueva",
                "ranking_nuevo"
            ]
        ].head(30)
    )

    return layout


def obtener_ubicaciones_disponibles(layout):
    """
    Obtiene las ubicaciones que pueden reutilizarse
    porque pertenecen a productos que serán movidos.

    Además clasifica automáticamente las ubicaciones
    en zonas físicas según su distancia al despacho.
    """

    disponibles = layout[
        layout["estado_slotting"].isin(
            [
                "Mover urgente",
                "Mover",
                "Aceptable"
            ]
        )
    ].copy()

    # ---------------------------------
    # Seleccionar columnas necesarias
    # ---------------------------------

    disponibles = disponibles[
        [
            "ranking_ubicacion",
            "X",
            "Y",
            "Z",
            "distancia_despacho"
        ]
    ]

    # ---------------------------------
    # Eliminar ubicaciones duplicadas
    # ---------------------------------

    disponibles = disponibles.drop_duplicates(
        subset="ranking_ubicacion"
    )

    # ---------------------------------
    # Ordenar por cercanía
    # ---------------------------------

    disponibles = disponibles.sort_values(
        "ranking_ubicacion"
    ).reset_index(drop=True)

    # ---------------------------------
    # Crear zonas físicas automáticamente
    # ---------------------------------

    disponibles["zona_fisica"] = np.select(
        [
            disponibles["distancia_despacho"] <= 10,
            disponibles["distancia_despacho"] <= 20,
            disponibles["distancia_despacho"] <= 30
        ],
        [
            "A",
            "B",
            "C"
        ],
        default="D"
    )

    # ---------------------------------
    # Logging
    # ---------------------------------

    logger.info(
        "Ubicaciones disponibles: %s",
        len(disponibles)
    )

    logger.info(
        "\n%s",
        disponibles["zona_fisica"].value_counts()
    )

    return disponibles


def calcular_ahorro_distancia(layout):
    """
    Calcula el ahorro de recorrido obtenido
    con la nueva ubicación propuesta.
    """
    

    layout = layout.copy()

    # -----------------------------
    # Ahorro individual
    # -----------------------------

    layout["ahorro_distancia"] = (
        layout["distancia_despacho"]
        - layout["distancia_nueva"]
    )

    # Si no hubo nueva ubicación
    layout["ahorro_distancia"] = (
        layout["ahorro_distancia"]
        .fillna(0)
    )

    logger.info(
        "Ahorro de distancia calculado."
    )

    
    print(
        layout[
            [
                "distancia_despacho",
                "distancia_nueva",
                "ahorro_distancia"
            ]
        ].head(20)
    )
    return layout


def preparar_plan_operativo(plan):
    """
    Da formato al plan de reubicación para que pueda ser
    utilizado directamente por el equipo de operaciones.
    """

    plan = plan.copy()

    # ============================================
    # Ubicación actual
    # ============================================

    plan["ubicacion_actual"] = (
        "X=" + plan["X"].astype(str) +
        " | Y=" + plan["Y"].astype(str) +
        " | Z=" + plan["Z"].astype(str)
    )

    # ============================================
    # Nueva ubicación
    # ============================================

    plan["ubicacion_nueva"] = (
        "X=" + plan["X_nuevo"].astype(str) +
        " | Y=" + plan["Y_nuevo"].astype(str) +
        " | Z=" + plan["Z_nuevo"].astype(str)
    )

    # ============================================
    # Prioridad operativa
    # ============================================

    plan["prioridad_operativa"] = "BAJA"

    plan.loc[
        plan["score_movimiento"] >= 50000000,
        "prioridad_operativa"
    ] = "CRÍTICA"

    plan.loc[
        (
            (plan["score_movimiento"] >= 20000000) &
            (plan["score_movimiento"] < 50000000)
        ),
        "prioridad_operativa"
    ] = "ALTA"

    plan.loc[
        (
            (plan["score_movimiento"] >= 5000000) &
            (plan["score_movimiento"] < 20000000)
        ),
        "prioridad_operativa"
    ] = "MEDIA"

    # ============================================
    # Estado del movimiento
    # ============================================

    plan["estado_movimiento"] = "Pendiente"

    # ============================================
    # Reordenar columnas
    # ============================================

    plan = plan[
        [
            "orden_movimiento",
            "codigo",
            "descripcion",

            "abcxyz",
            "prioridad_slotting",
            "prioridad_operativa",

            "demanda_anual",
            "valor_consumo",

            "ranking_producto",

            "estado_slotting",

            "ubicacion_actual",
            "ubicacion_nueva",

            "distancia_actual",
            "distancia_nueva",
            "ahorro_distancia",

            "score_movimiento",

            "zona_recomendada",
            "tipo_picking",

            "estado_movimiento"
        ]
    ]

    logger.info(
        "Plan operativo preparado."
    )

    return plan