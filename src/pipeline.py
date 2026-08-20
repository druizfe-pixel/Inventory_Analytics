import logging

logger = logging.getLogger(__name__)


from src.abcxyz import (
    obtener_columnas_demanda,
    calcular_demanda_anual,
    validar_demanda_xyz,
    calcular_valor_consumo,
    clasificacion_abc,
    calcular_demanda_promedio,
    calcular_desviacion_demanda,
    calcular_coeficiente_variacion,
    clasificacion_xyz,
    clasificacion_abcxyz,
)

from src.indicadores import (
    calcular_demanda_mensual,
    calcular_demanda_diaria,
    calcular_inventario_promedio,
    calcular_costo_mantenimiento_unitario,
)

from src.eoq import (
    validar_datos_eoq,
    calcular_eoq,
    calcular_numero_pedidos,
    calcular_tiempo_entre_pedidos,
    calcular_costo_ordenar_anual,
    calcular_costo_mantener_anual,
    calcular_costo_total_eoq,
    resumen_eoq,
)

from src.stock_seguridad import (
    agregar_lead_time,
    agregar_nivel_servicio,
    calcular_desviacion_diaria,
    calcular_desviacion_lead_time,
    calcular_stock_seguridad,
    resumen_stock_seguridad
)

from src.punto_reorden import (
    calcular_punto_reorden,
    resumen_punto_reorden,
)



def ejecutar_abc_xyz(df):
    """
    Ejecuta todo el proceso de clasificación ABC-XYZ.
    """

    columnas = obtener_columnas_demanda(df)
    demanda_unidades = columnas["unidades"]

    df = calcular_demanda_anual(
        df,
        demanda_unidades,
    )

    df = validar_demanda_xyz(df)

    df = calcular_valor_consumo(df)

    df = calcular_demanda_promedio(
        df,
        demanda_unidades,
    )

    df = calcular_desviacion_demanda(
        df,
        demanda_unidades,
    )

    df = calcular_coeficiente_variacion(df)

    df = clasificacion_xyz(df)

    df = clasificacion_abc(df)

    df = clasificacion_abcxyz(df)
    

    return df


def ejecutar_indicadores(df):
    """
    Ejecuta el cálculo de indicadores básicos de inventario.
    """

    df = calcular_demanda_mensual(df)

    df = calcular_demanda_diaria(df)

    df = calcular_inventario_promedio(df)

    df = calcular_costo_mantenimiento_unitario(df)

    return df

def ejecutar_eoq(df):
    """
    Ejecuta todos los cálculos del modelo EOQ.
    """

    #validar_datos_eoq(df)

    df = calcular_eoq(df)

    df = calcular_numero_pedidos(df)

    df = calcular_tiempo_entre_pedidos(df)

    df = calcular_costo_ordenar_anual(df)

    df = calcular_costo_mantener_anual(df)

    df = calcular_costo_total_eoq(df)

    resumen_eoq(df)

    return df

def ejecutar_stock_seguridad(df):

    df = agregar_lead_time(df)

    df = agregar_nivel_servicio(df)

    df = calcular_desviacion_diaria(df)

    df = calcular_desviacion_lead_time(df)

    df = calcular_stock_seguridad(df)

    resumen_stock_seguridad(df)

    return df

def ejecutar_punto_reorden(df):

    df = calcular_punto_reorden(df)

    resumen_punto_reorden(df)

    return df

