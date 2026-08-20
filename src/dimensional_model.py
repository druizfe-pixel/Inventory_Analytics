import pandas as pd
import numpy as np
import getpass
from pathlib import Path
from datetime import datetime


def crear_dim_producto(inventario):
    """
    ==========================================================
    DIM_PRODUCTO

    Genera la dimensión principal del modelo dimensional.

    Una fila = Un SKU.

    Contiene toda la información maestra del producto y los
    indicadores logísticos necesarios para Power BI.

    Esta dimensión reemplaza la necesidad de fact_inventario.
    ==========================================================
    """

    print("\nGenerando dim_producto...")

    # ======================================================
    # Columnas del modelo
    # ======================================================

    columnas = [

        # Identificación
        "codigo",
        "descripcion",
        "familia",
        "grupo",
        "linea",

        # Clasificación
        "abc",
        "xyz",
        "abcxyz",

        # Slotting
        "prioridad_slotting",
        "zona_recomendada",
        "tipo_picking",

        # Demanda
        "demanda_anual",
        "demanda_promedio",

        # Valor
        "valor_consumo",

        # Inventario
        "inventario",
        "inventario_promedio",

        # Planeación
        "eoq",
        "stock_seguridad",
        "punto_reorden",

        # Parámetros
        "lead_time",
        "nivel_servicio",

        # Indicadores EOQ
        "pedidos_anuales",
        "dias_entre_pedidos",
        "costo_ordenar_anual",
        "costo_mantener_anual",
        "costo_total_eoq"

    ]

    # ======================================================
    # Seleccionar columnas
    # ======================================================

    dim = inventario[columnas].copy()

    # ======================================================
    # Eliminar registros sin código
    # ======================================================

    dim = dim.dropna(
        subset=["codigo"]
    )

    # ======================================================
    # Eliminar duplicados
    # ======================================================

    dim = dim.drop_duplicates(
        subset="codigo",
        keep="first"
    )

    # ======================================================
    # Ordenar
    # ======================================================

    dim = dim.sort_values(
        by="codigo"
    ).reset_index(
        drop=True
    )

    # ======================================================
    # Crear clave sustituta
    # ======================================================

    dim.insert(
        0,
        "id_producto",
        range(
            1,
            len(dim) + 1
        )
    )

    # ======================================================
    # Validaciones
    # ======================================================

    if dim.empty:

        raise ValueError(
            "dim_producto quedó vacía."
        )

    if dim["codigo"].isna().any():

        raise ValueError(
            "Hay códigos nulos en dim_producto."
        )

    duplicados = dim["codigo"].duplicated().sum()

    if duplicados > 0:

        raise ValueError(
            f"Se encontraron {duplicados} códigos duplicados."
        )

    # ======================================================
    # Conversión de tipos
    # ======================================================

    columnas_texto = [

        "descripcion",
        "familia",
        "grupo",
        "linea",
        "abc",
        "xyz",
        "abcxyz",
        "prioridad_slotting",
        "zona_recomendada",
        "tipo_picking"

    ]

    for col in columnas_texto:

        if col in dim.columns:

            dim[col] = (
                dim[col]
                .fillna("")
                .astype(str)
                .str.strip()
            )

    # ======================================================
    # Resumen
    # ======================================================

    print("--------------------------------------")
    print("DIM_PRODUCTO")
    print("--------------------------------------")
    print(f"Productos           : {len(dim):,}")
    print(f"Columnas            : {len(dim.columns)}")
    print(f"Duplicados          : {duplicados}")
    print(f"Nulos código        : {dim['codigo'].isna().sum()}")
    print("--------------------------------------")
    print("✓ Dimensión creada correctamente.\n")

    return dim

def crear_dim_familia(inventario):
    """
    Crea la dimensión de clasificación
    organizacional de los productos.

    Granularidad:
    Una combinación única de
    Grupo - Familia - Línea.
    """

    dim_familia = (
        inventario[
            [
                "grupo",
                "familia",
                "linea"
            ]
        ]
        .drop_duplicates()
        .sort_values(
            [
                "grupo",
                "familia",
                "linea"
            ]
        )
        .reset_index(drop=True)
    )

    # Clave sustituta
    dim_familia.insert(
        0,
        "id_familia",
        range(1, len(dim_familia) + 1)
    )

    return dim_familia



def crear_dim_abcxyz(inventario):
    """
    Crea la dimensión ABCXYZ.

    Incluye atributos de negocio que
    podrán utilizarse directamente
    desde Power BI.
    """

    dim = (
        inventario[
            [
                "abcxyz",
                "abc",
                "xyz"
            ]
        ]
        .drop_duplicates()
        .sort_values(
            [
                "abc",
                "xyz"
            ]
        )
        .reset_index(drop=True)
    )

    prioridad = {
        "AX": 1,
        "AY": 2,
        "AZ": 3,
        "BX": 4,
        "BY": 5,
        "BZ": 6,
        "CX": 7,
        "CY": 8,
        "CZ": 9,
        "N": 99
    }

    nivel_servicio = {
        "AX": 0.99,
        "AY": 0.98,
        "AZ": 0.97,
        "BX": 0.97,
        "BY": 0.96,
        "BZ": 0.95,
        "CX": 0.94,
        "CY": 0.92,
        "CZ": 0.90,
        "N": 0.90
    }

    color = {
        "AX": "#16A34A",
        "AY": "#22C55E",
        "AZ": "#84CC16",
        "BX": "#3B82F6",
        "BY": "#60A5FA",
        "BZ": "#93C5FD",
        "CX": "#F59E0B",
        "CY": "#FBBF24",
        "CZ": "#DC2626",
        "N": "#9CA3AF"
    }

    dim["prioridad"] = dim["abcxyz"].map(prioridad)

    dim["nivel_servicio"] = (
        dim["abcxyz"]
        .map(nivel_servicio)
    )

    dim["color"] = (
        dim["abcxyz"]
        .map(color)
    )

    dim.insert(
        0,
        "id_abcxyz",
        range(1, len(dim) + 1)
    )

    return dim



def crear_dim_estado(layout):
    """
    Crea la dimensión de estados de slotting.

    Incluye información de negocio para
    facilitar la visualización en Power BI.
    """

    estados = [
        {
            "id_estado": 1,
            "estado_slotting": "Mover urgente",
            "orden": 1,
            "prioridad": "Crítica",
            "color": "#DC2626",
            "accion": "Reubicar inmediatamente"
        },
        {
            "id_estado": 2,
            "estado_slotting": "Mover",
            "orden": 2,
            "prioridad": "Alta",
            "color": "#F59E0B",
            "accion": "Programar reubicación"
        },
        {
            "id_estado": 3,
            "estado_slotting": "Aceptable",
            "orden": 3,
            "prioridad": "Media",
            "color": "#EAB308",
            "accion": "Evaluar mejora"
        },
        {
            "id_estado": 4,
            "estado_slotting": "Correcto",
            "orden": 4,
            "prioridad": "Baja",
            "color": "#16A34A",
            "accion": "Mantener"
        },
        {
            "id_estado": 5,
            "estado_slotting": "Óptimo",
            "orden": 5,
            "prioridad": "Ninguna",
            "color": "#2563EB",
            "accion": "Sin acción"
        },
        {
            "id_estado": 6,
            "estado_slotting": "Sin ubicación",
            "orden": 6,
            "prioridad": "Pendiente",
            "color": "#6B7280",
            "accion": "Asignar ubicación"
        },
        {
            "id_estado": 7,
            "estado_slotting": "No evaluar",
            "orden": 7,
            "prioridad": "Excluir",
            "color": "#9CA3AF",
            "accion": "Sin análisis"
        }
    ]

    dim_estado = pd.DataFrame(estados)

    return dim_estado


def crear_dim_zona():
    """
    Crea la dimensión de zonas logísticas
    del almacén.
    """

    zonas = [

        {
            "id_zona": 1,
            "zona": "A",
            "orden": 1,
            "prioridad": "Muy Alta",
            "color": "#16A34A",
            "distancia_objetivo": "Muy corta",
            "tipo_almacenamiento": "Alta rotación"
        },

        {
            "id_zona": 2,
            "zona": "B",
            "orden": 2,
            "prioridad": "Alta",
            "color": "#3B82F6",
            "distancia_objetivo": "Corta",
            "tipo_almacenamiento": "Rotación media"
        },

        {
            "id_zona": 3,
            "zona": "C",
            "orden": 3,
            "prioridad": "Media",
            "color": "#F59E0B",
            "distancia_objetivo": "Media",
            "tipo_almacenamiento": "Rotación baja"
        },

        {
            "id_zona": 4,
            "zona": "D",
            "orden": 4,
            "prioridad": "Baja",
            "color": "#DC2626",
            "distancia_objetivo": "Larga",
            "tipo_almacenamiento": "Reserva"
        }

    ]

    dim_zona = pd.DataFrame(zonas)

    return dim_zona




def crear_dim_picking():
    """
    Crea la dimensión de estrategias de picking.

    Permite ampliar el modelo sin modificar
    el dashboard cuando se implementen nuevas
    estrategias de preparación de pedidos.
    """

    picking = [

        {
            "id_picking": 1,
            "tipo_picking": "Picking dinámico",
            "orden": 1,
            "prioridad": "Alta",
            "color": "#16A34A",
            "descripcion": "Productos de alta rotación ubicados cerca al despacho."
        },

        {
            "id_picking": 2,
            "tipo_picking": "Picking convencional",
            "orden": 2,
            "prioridad": "Media",
            "color": "#3B82F6",
            "descripcion": "Productos de rotación normal."
        }

    ]

    dim_picking = pd.DataFrame(picking)

    return dim_picking


import numpy as np
import pandas as pd


def crear_dim_ubicacion(ubicaciones_modelo):
    """
    Convierte el maestro de ubicaciones
    en la dimensión de Power BI.
    """

    return ubicaciones_modelo.copy()

    # ======================================
    # Tipo de posición
    # ======================================

    dim["tipo_posicion"] = np.where(
        dim["Z"] <= 1.5,
        "Piso",
        "Rack"
    )

    return dim




def crear_dim_calendario(
    fecha_inicio="2024-01-01",
    fecha_fin="2030-12-31"
):
    """
    Crea la dimensión calendario.

    Será utilizada para el histórico
    de ejecuciones del algoritmo y
    análisis temporales.
    """

    calendario = pd.DataFrame({

        "fecha": pd.date_range(
            start=fecha_inicio,
            end=fecha_fin,
            freq="D"
        )

    })

    calendario["id_fecha"] = (
        calendario["fecha"]
        .dt.strftime("%Y%m%d")
        .astype(int)
    )

    calendario["anio"] = calendario["fecha"].dt.year

    calendario["mes_numero"] = calendario["fecha"].dt.month

    calendario["mes"] = (
        calendario["fecha"]
        .dt.month_name(locale="es_ES")
    )

    calendario["trimestre"] = (
        "T"
        + calendario["fecha"]
        .dt.quarter.astype(str)
    )

    calendario["semana"] = (
        calendario["fecha"]
        .dt.isocalendar()
        .week
        .astype(int)
    )

    calendario["dia"] = calendario["fecha"].dt.day

    calendario["nombre_dia"] = (
        calendario["fecha"]
        .dt.day_name(locale="es_ES")
    )

    calendario["fin_semana"] = (
        calendario["fecha"]
        .dt.weekday >= 5
    )

    return calendario

def crear_fact_inventario(inventario):
    """
    Crea la tabla de hechos del inventario.

    Granularidad:
    Un registro por SKU.

    Contiene únicamente métricas.
    """

    fact = (
        inventario[
            [
                "codigo",
                "demanda_anual",
                "valor_consumo",
                "inventario",
                "inventario_promedio",
                "eoq",
                "pedidos_anuales",
                "stock_seguridad",
                "punto_reorden",
                "costo_ordenar_anual",
                "costo_mantener_anual",
                "costo_total_eoq"
            ]
        ]
        .copy()
    )

    return fact

def crear_fact_layout(layout):
    """
    Crea la tabla de hechos del Layout.

    Granularidad:
    Un registro por SKU.

    Contiene únicamente las métricas
    generadas por el algoritmo de slotting.
    """

    fact = (
        layout[
            [
                "codigo",

                "ranking_producto",

                "ranking_ubicacion",

                "ranking_ubicacion_nueva",

                "distancia_despacho",

                "distancia_nueva",

                "mejora_ranking",

                "ahorro_distancia",

                "score_movimiento",

                "estado_slotting",

                "zona_recomendada",

                "tipo_picking"
            ]
        ]
        .copy()
    )

    fact.rename(
        columns={
            "distancia_despacho": "distancia_actual"
        },
        inplace=True
    )


    fact["distancia_actual"] = (
        fact["distancia_actual"]
        .round(2)
    )

    fact["distancia_nueva"] = (
        fact["distancia_nueva"]
        .round(2)
    )

    fact["ahorro_distancia"] = (
        fact["ahorro_distancia"]
        .round(2)
    )

    fact["mejora_ranking"] = (
        fact["mejora_ranking"]
        .fillna(0)
        .astype(int)
    )
    return fact

def crear_fact_plan_reubicacion(plan_reubicacion):
    """
    Crea la tabla de hechos del plan de
    reubicación.

    Granularidad:
    Un movimiento recomendado por SKU.
    """

    fact = (
        plan_reubicacion[
            [
                "codigo",

                "orden_movimiento",

                "ranking_producto",

                "ranking_ubicacion",

                "ranking_ubicacion_nueva",

                "distancia_actual",

                "distancia_nueva",

                "mejora_ranking",

                "ahorro_distancia",

                "score_movimiento",

                "estado_slotting",

                "zona_recomendada"
            ]
        ]
        .copy()
    )

    return fact



from datetime import datetime
import getpass

import pandas as pd


def crear_fact_historico(
    layout,
    historico=None,
    version_algoritmo="1.0.0"
):
    """
    Crea y actualiza la tabla Fact_Historico.

    La función NO lee ni escribe archivos.

    Si existe un histórico previo (DataFrame),
    agrega la nueva ejecución.

    Si no existe, crea el histórico desde cero.

    Granularidad:
        1 registro = 1 SKU por ejecución.

    Parameters
    ----------
    layout : DataFrame
        Resultado final del algoritmo.

    historico : DataFrame, optional
        Histórico existente.

    version_algoritmo : str
        Versión del algoritmo.

    Returns
    -------
    DataFrame
        Fact_Historico actualizado.
    """

    # ==========================================
    # Información de la ejecución
    # ==========================================

    ahora = datetime.now()

    fecha = ahora.strftime("%Y-%m-%d")

    fecha_hora = ahora.strftime("%Y-%m-%d %H:%M:%S")

    id_ejecucion = ahora.strftime("%Y%m%d%H%M%S")

    usuario = getpass.getuser()

    # ==========================================
    # Nueva ejecución
    # ==========================================

    nuevo = layout[
        [
            "codigo",
            "estado_slotting",
            "ranking_producto",
            "ranking_ubicacion",
            "ranking_ubicacion_nueva",
            "distancia_despacho",
            "distancia_nueva",
            "mejora_ranking",
            "ahorro_distancia",
            "score_movimiento"
        ]
    ].copy()

    nuevo.rename(
        columns={
            "distancia_despacho": "distancia_actual"
        },
        inplace=True
    )

    # ==========================================
    # Auditoría
    # ==========================================

    nuevo.insert(
        0,
        "id_ejecucion",
        id_ejecucion
    )

    nuevo.insert(
        1,
        "fecha_hora_ejecucion",
        fecha_hora
    )

    nuevo.insert(
        2,
        "fecha_ejecucion",
        fecha
    )

    nuevo.insert(
        3,
        "version_algoritmo",
        version_algoritmo
    )

    nuevo.insert(
        4,
        "usuario_ejecucion",
        usuario
    )

    # ==========================================
    # Actualizar histórico
    # ==========================================

    if historico is None:

        historico = nuevo

    else:

        historico = pd.concat(
            [
                historico,
                nuevo
            ],
            ignore_index=True
        )

    # ==========================================
    # Eliminar duplicados
    # ==========================================

    historico = historico.drop_duplicates(
        subset=[
            "id_ejecucion",
            "codigo"
        ],
        keep="last"
    )

    # ==========================================
    # Ordenar histórico
    # ==========================================

    historico = historico.sort_values(
        by=[
            "fecha_hora_ejecucion",
            "codigo"
        ]
    ).reset_index(
        drop=True
    )

    return historico