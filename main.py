import logging

logger = logging.getLogger(__name__)

from src.cargar_datos import (
    cargar_inventario,
    cargar_ubicaciones,
    validar_dataframe,
)

from src.limpieza import (
    limpiar_datos,
    eliminar_duplicados_codigo
)
from src.transformacion import transformar_datos

from src.pipeline import (
    ejecutar_abc_xyz,
    ejecutar_indicadores,
    ejecutar_eoq,
    ejecutar_stock_seguridad,
    ejecutar_punto_reorden
)
from src.reportes import (
    mostrar_reportes
)

from src.exportar import (
    exportar_resultados
)
from src.slotting import (
    ejecutar_slotting,
)

from src.layout_optimizer import (
    integrar_ubicaciones,
    calcular_distancia,
    rankear_ubicaciones,
    evaluar_slotting,
    recomendar_ubicacion,
    obtener_ubicaciones_disponibles,
    crear_maestro_ubicaciones
)

from src.layout_assignment import (
    rankear_productos,
    asignar_ubicaciones,
    comparar_layout,
    calcular_score_movimiento,
    generar_plan_reubicacion,
    asignar_ubicacion_optima,
    obtener_ubicaciones_disponibles,
    validar_asignacion,
    calcular_ahorro_distancia,
)

from src.powerbi_export import exportar_powerbi
from src.exportar_modelo import (
    exportar_modelo_dimensional
)

from src.transformacion import transformar_ubicaciones

def main():

    # ===================================
    # Carga de datos
    # ===================================

    inventario = cargar_inventario()
    ubicaciones = cargar_ubicaciones()
    
    ubicaciones.rename(
        columns={
            "Codigo": "codigo"
        },
        inplace=True
    )
    print(ubicaciones.columns.tolist())

    # ===================================
    # Limpieza y transformación
    # ===================================

    inventario = limpiar_datos(inventario)
    inventario = eliminar_duplicados_codigo(inventario)
    inventario = transformar_datos(inventario)

    # Normalizar códigos de ubicaciones
    ubicaciones = transformar_ubicaciones(ubicaciones)

    # ===================================
    # Clasificación ABC XYZ
    # ===================================

    inventario = ejecutar_abc_xyz(
        inventario
    )

    # ===================================
    # Indicadores
    # ===================================

    inventario = ejecutar_indicadores(inventario)

    # ===================================
    # EOQ
    # ===================================
    
    inventario = ejecutar_eoq(inventario)

    
    # ===================================
    # Stock de Seguridad
    # ===================================

    inventario = ejecutar_stock_seguridad(inventario)

    # ===================================
    # Punto de Reorden
    # ===================================

    inventario = ejecutar_punto_reorden(inventario)

    # ===================================
    # Slotting
    # ===================================

    slotting = ejecutar_slotting(inventario)

    slotting = integrar_ubicaciones(
        slotting,
        ubicaciones
    )

    slotting = calcular_distancia(slotting)

    slotting = rankear_ubicaciones(slotting)

    print(slotting.columns.tolist())

    slotting = evaluar_slotting(slotting)

    slotting = recomendar_ubicacion(slotting)

    

    # ===================================
    # Optimización de Layout
    # ===================================
    
    productos = rankear_productos(slotting)
    
    
    layout = asignar_ubicaciones(
        productos,
        slotting
    )

    ubicaciones_disponibles = obtener_ubicaciones_disponibles(layout)

    
    print(ubicaciones_disponibles.head(10))

    layout = comparar_layout(
        productos,
        layout
    )

    layout = calcular_score_movimiento(layout)

    layout = asignar_ubicacion_optima(
        layout,
        ubicaciones_disponibles
    )

    layout = calcular_ahorro_distancia(layout)

    layout = validar_asignacion(layout)

    ubicaciones_modelo = crear_maestro_ubicaciones(
        layout
    )

    print(layout.columns.tolist())

    plan_reubicacion = generar_plan_reubicacion(layout)


   #ubicaciones_disponibles = obtener_ubicaciones_disponibles(...)

    print(
        plan_reubicacion.head(20)
    )

    # ===================================
    # Reportes
    # ===================================  

    mostrar_reportes(inventario)

    # ===================================
    # Exportar
    # =================================== 

    exportar_resultados(
        inventario,
        slotting,
        plan_reubicacion
    )


    print("\n===== VARIABLES ANTES DE EXPORTAR =====")
    print("inventario:", type(inventario))
    print("layout:", type(layout))
    print("plan_reubicacion:", type(plan_reubicacion))
    print("ubicaciones:", type(ubicaciones))
    print("=======================================\n")

    exportar_modelo_dimensional(
        inventario,
        layout,
        plan_reubicacion,
        ubicaciones_modelo,
        carpeta_salida="output/powerbi",
        version_algoritmo="1.0.0"
    )

    print(ubicaciones.info())
    
    logger.info("=" * 60)
    logger.info("Proceso finalizado correctamente.")
    logger.info("Inventario procesado: %s", len(inventario))
    logger.info("Registros slotting: %s", len(slotting))
    logger.info("Ubicaciones procesadas: %s", len(ubicaciones))
    logger.info("=" * 60)

if __name__ == "__main__":

    main()