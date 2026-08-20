from pathlib import Path
from datetime import datetime
import getpass
import pandas as pd

from src.export_helpers import (
    crear_estructura_powerbi,
    crear_dimensiones,
    crear_facts,
    exportar_dimensiones,
    exportar_facts,
    generar_metadata,
    generar_readme,
    generar_log_exportacion
)

from src.validar_modelo import validar_modelo_dimensional

# =====================================================
# ORQUESTADOR
# =====================================================

from pathlib import Path


def exportar_modelo_dimensional(
    inventario,
    layout,
    plan_reubicacion,
    ubicaciones_modelo,
    carpeta_salida,
    version_algoritmo="2.0.0"
):
    """
    ==========================================================
    EXPORTAR MODELO DIMENSIONAL

    Orquesta completamente la generación del Data Mart para
    Power BI.

    Flujo del proceso

        1. Crear estructura de carpetas

        2. Crear dimensiones

        3. Crear tablas Fact

        4. Validar modelo dimensional

        5. Exportar dimensiones

        6. Exportar Facts

        7. Generar Metadata

        8. Generar README

        9. Generar Log

    El modelo generado queda listo para ser consumido por
    Power BI.

    ==========================================================
    """

    print("\n===========================================")
    print(" EXPORTACIÓN MODELO DIMENSIONAL POWER BI")
    print("===========================================")

    # ======================================================
    # Crear estructura
    # ======================================================

    rutas = crear_estructura_powerbi(
        carpeta_salida
    )

    # ======================================================
    # Crear dimensiones
    # ======================================================

    dimensiones = crear_dimensiones(
        inventario=inventario,
        layout=layout,
        ubicaciones_modelo=ubicaciones_modelo
    )

    # ======================================================
    # Crear tablas Fact
    # ======================================================

    facts = crear_facts(
        layout=layout,
        plan_reubicacion=plan_reubicacion,
        carpeta_salida=rutas["facts"],
        version_algoritmo=version_algoritmo
    )

    # ======================================================
    # Validar modelo
    # ======================================================

    validar_modelo_dimensional(
        dimensiones,
        facts
    )

    # ======================================================
    # Exportar dimensiones
    # ======================================================

    exportar_dimensiones(
        dimensiones,
        rutas["dimensions"]
    )

    # ======================================================
    # Exportar Facts
    # ======================================================

    exportar_facts(
        facts,
        rutas["facts"]
    )

    # ======================================================
    # Metadata
    # ======================================================

    metadata = generar_metadata(
        dimensiones=dimensiones,
        facts=facts,
        carpeta_metadata=rutas["metadata"],
        version_algoritmo=version_algoritmo
    )

    # ======================================================
    # README
    # ======================================================

    generar_readme(
        rutas["base"]
    )

    # ======================================================
    # Log de exportación
    # ======================================================

    generar_log_exportacion(
        dimensiones=dimensiones,
        facts=facts,
        carpeta_logs=rutas["logs"],
        version_algoritmo=version_algoritmo
    )

    # ======================================================
    # Resumen final
    # ======================================================

    print("\n===========================================")
    print(" MODELO DIMENSIONAL EXPORTADO")
    print("===========================================")

    print(f"Carpeta destino : {Path(carpeta_salida).resolve()}")

    print(f"Dimensiones     : {len(dimensiones)}")

    print(f"Facts           : {len(facts)}")

    print(
        f"Total tablas    : "
        f"{len(dimensiones)+len(facts)}"
    )

    print(f"Versión ETL     : {version_algoritmo}")

    print("===========================================")

    return {

        "dimensiones": dimensiones,

        "facts": facts,

        "metadata": metadata,

        "rutas": rutas

    }