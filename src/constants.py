# ==========================
# COLUMNAS PRINCIPALES
# ==========================

CODIGO = "codigo"
DESCRIPCION = "descripcion"
FAMILIA = "familia"
GRUPO = "grupo"
LINEA = "linea"

COSTO_ORDENAR = "costo_ordenar"
COSTO_ALMACENAR = "costo_almacenar"

VR_UNIT = "vr_unit"
INVENTARIO = "inventario"
PEDIDOS = "pedidos"
WIP = "wip_planta"



# ==========================
# EOQ
# ==========================

COLUMNAS_EOQ = [
    "demanda_anual",
    "costo_ordenar",
    "costo_mantenimiento_unitario",
]

COLUMNAS_PEDIDOS = [
    "demanda_anual",
    "eoq",
]

COLUMNAS_TIEMPO_PEDIDOS = [
    "pedidos_anuales",
]

COLUMNAS_COSTO_ORDENAR = [
    "pedidos_anuales",
    "costo_ordenar",
]

COLUMNAS_COSTO_MANTENER = [
    "eoq",
    "costo_mantenimiento_unitario",
]

COLUMNAS_COSTO_TOTAL = [
    "costo_ordenar_anual",
    "costo_mantener_anual",
]

COLUMNAS_REQUERIDAS = [
    "demanda_anual",
    "costo_ordenar",
    "costo_mantenimiento_unitario",
]

COLUMNAS_PEDIDOS = [
    "pedidos_anuales",
    "costo_ordenar",
]

COLUMNAS_MANTENIMIENTO = [
    "eoq",
    "costo_mantenimiento_unitario",
]

COLUMNAS_COSTO_TOTAL = [
    "costo_ordenar_anual",
    "costo_mantener_anual",
]


# ==========================
# STOCK DE SEGURIDAD
# ==========================

COLUMNAS_DESVIACION = [
    "demanda_anual",
    "desviacion_demanda",
]

COLUMNAS_LEAD_TIME = [
    "demanda_anual",
    "desviacion_diaria",
    "lead_time",
]

COLUMNAS_STOCK_SEGURIDAD = [
    "demanda_anual",
    "valor_z",
    "desviacion_lead_time",
]

# ==========================
# PUNTO DE REORDEN
# ==========================

COLUMNAS_PUNTO_REORDEN = [
    "demanda_anual",
    "demanda_diaria",
    "lead_time",
    "stock_seguridad",
]

NIVELES_SERVICIO = {
    0.90: 1.28,
    0.95: 1.65,
    0.97: 1.88,
    0.98: 2.05,
    0.99: 2.33,
}

# =====================================================
# COLUMNAS PARA EXPORTACIÓN
# =====================================================

COLUMNAS_EXPORTAR_ABC = [
    "codigo",
    "abcxyz",
    "abc",
    "xyz",
    "demanda_anual",
    "valor_consumo",
    "coeficiente_variacion",
]

COLUMNAS_EXPORTAR_EOQ = [
    "codigo",
    "eoq",
    "pedidos_anuales",
    "dias_entre_pedidos",
    "costo_total_eoq",
]

COLUMNAS_EXPORTAR_SLOTTING = [
    "codigo",
    "abcxyz",
    "prioridad_slotting",
    "zona_recomendada",
    "tipo_picking",
    "X",
    "Y",
    "Z",
    "distancia_despacho",
    "ranking_ubicacion",
    "estado_slotting",
    "ubicacion_recomendada",
]