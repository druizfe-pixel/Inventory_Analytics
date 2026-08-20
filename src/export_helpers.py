from pathlib import Path
from datetime import datetime
import getpass
import pandas as pd

from src.dimensional_model import (

    # ===========================
    # Dimensiones
    # ===========================

    crear_dim_producto,
    crear_dim_familia,
    crear_dim_abcxyz,
    crear_dim_estado,
    crear_dim_zona,
    crear_dim_picking,
    crear_dim_ubicacion,
    crear_dim_calendario,

    # ===========================
    # Facts
    # ===========================

    crear_fact_layout,
    crear_fact_plan_reubicacion,
    crear_fact_historico

)

# =====================================================
# FUNCIONES AUXILIARES
# =====================================================

def crear_estructura_powerbi(
    carpeta_base
):
    """
    Crea la estructura de carpetas para el
    modelo dimensional de Power BI.
    """

    carpeta_base = Path(carpeta_base)

    rutas = {

        "base": carpeta_base,

        "dimensions": carpeta_base / "dimensions",

        "facts": carpeta_base / "facts",

        "metadata": carpeta_base / "metadata",

        "logs": carpeta_base / "logs"

    }

    for carpeta in rutas.values():

        carpeta.mkdir(
            parents=True,
            exist_ok=True
        )

    return rutas

def crear_dimensiones(
    inventario,
    layout,
    ubicaciones_modelo
):
    """
    ======================================================
    Genera todas las dimensiones del modelo dimensional.
    ======================================================
    """

    print("\nGenerando dimensiones...")

    dimensiones = {

        "dim_producto": crear_dim_producto(
            inventario
        ),

        "dim_familia": crear_dim_familia(
            inventario
        ),

        "dim_abcxyz": crear_dim_abcxyz(
            inventario
        ),

        "dim_estado": crear_dim_estado(
            layout
        ),

        "dim_zona": crear_dim_zona(),

        "dim_picking": crear_dim_picking(),

        "dim_ubicacion": crear_dim_ubicacion(
            ubicaciones_modelo
        ),

        "dim_calendario": crear_dim_calendario()

    }

    print(
        f"✓ {len(dimensiones)} dimensiones creadas."
    )

    return dimensiones

def exportar_dimensiones(
    dimensiones,
    carpeta_dimensions
):
    """
    Exporta todas las dimensiones del modelo.

    Parameters
    ----------
    dimensiones : dict
        Diccionario con nombre_archivo : DataFrame

    carpeta_dimensions : Path
        Carpeta donde se guardarán las dimensiones.
    """

    print("\nExportando dimensiones...")

    for nombre, tabla in dimensiones.items():

        archivo = carpeta_dimensions / f"{nombre}.csv"

        tabla.to_csv(
            archivo,
            index=False,
            sep=";",
            decimal=",",
            encoding="utf-8-sig"
        )

        print(
            f"   ✓ {nombre}.csv ({len(tabla):,} registros)"
        )

def crear_facts(
    layout,
    plan_reubicacion,
    carpeta_salida,
    version_algoritmo
):
    """
    Genera todas las tablas Fact.
    """

    print("\nGenerando tablas Fact...")

    # ======================================
    # Histórico existente
    # ======================================

    archivo_historico = (
        Path(carpeta_salida) /
        "fact_historico.csv"
    )

    if archivo_historico.exists():

        historico = pd.read_csv(
            archivo_historico,
            encoding="utf-8-sig"
        )

    else:

        historico = None

    # ======================================
    # Crear Facts
    # ======================================

    facts = {

        "fact_layout": crear_fact_layout(
            layout
        ),

        "fact_plan_reubicacion":
            crear_fact_plan_reubicacion(
                plan_reubicacion
            ),

        "fact_historico":
            crear_fact_historico(
                layout=layout,
                historico=historico,
                version_algoritmo=version_algoritmo
            )

    }

    return facts



def exportar_facts(
    facts,
    carpeta_facts
):
    """
    Exporta todas las tablas Fact del modelo.

    Parameters
    ----------
    facts : dict
        Diccionario con nombre_archivo : DataFrame

    carpeta_facts : Path
        Carpeta donde se guardarán las tablas Fact.
    """

    print("\nExportando tablas Fact...")

    for nombre, tabla in facts.items():

        archivo = carpeta_facts / f"{nombre}.csv"

        tabla.to_csv(
            archivo,
            index=False,
            sep=";",
            decimal=",",
            encoding="utf-8-sig"
        )

        print(
            f"   ✓ {nombre}.csv ({len(tabla):,} registros)"
        )

def generar_metadata(
    dimensiones,
    facts,
    carpeta_metadata,
    version_algoritmo="1.0.0"
):
    """
    Genera el archivo metadata_modelo.csv
    con información de auditoría del ETL.
    """

    registros = []

    # =====================================
    # Dimensiones
    # =====================================

    for nombre, tabla in dimensiones.items():

        registros.append({

            "tipo": "Dimension",

            "tabla": nombre,

            "registros": len(tabla)

        })

    # =====================================
    # Facts
    # =====================================

    for nombre, tabla in facts.items():

        registros.append({

            "tipo": "Fact",

            "tabla": nombre,

            "registros": len(tabla)

        })

    metadata = pd.DataFrame(registros)

    # =====================================
    # Auditoría
    # =====================================

    metadata["fecha_generacion"] = datetime.now().strftime(
        "%Y-%m-%d"
    )

    metadata["hora_generacion"] = datetime.now().strftime(
        "%H:%M:%S"
    )

    metadata["usuario"] = getpass.getuser()

    metadata["version_algoritmo"] = version_algoritmo

    metadata["total_dimensiones"] = len(dimensiones)

    metadata["total_facts"] = len(facts)

    metadata["total_tablas"] = (
        len(dimensiones)
        + len(facts)
    )

    metadata["total_registros"] = metadata[
        "registros"
    ].sum()

    # =====================================
    # Exportar
    # =====================================

    metadata.to_csv(

        carpeta_metadata / "metadata_modelo.csv",

        index=False,

        encoding="utf-8-sig"

    )

    print(
        "\n✓ metadata_modelo.csv generado."
    )

    return metadata


def generar_readme(
    carpeta_metadata,
    version_algoritmo="1.0.0"
):
    """
    Genera un archivo README con la descripción
    del modelo dimensional exportado.
    """

    contenido = f"""
==========================================================
 INVENTORY ANALYTICS & WAREHOUSE OPTIMIZATION
==========================================================

Modelo Dimensional para Power BI

Versión algoritmo : {version_algoritmo}

Fecha generación : {datetime.now().strftime("%Y-%m-%d")}

Hora generación  : {datetime.now().strftime("%H:%M:%S")}

==========================================================

ESTRUCTURA

powerbi/

├── dimensions/

│   ├── dim_producto.csv

│   ├── dim_familia.csv

│   ├── dim_abcxyz.csv

│   ├── dim_estado.csv

│   ├── dim_zona.csv

│   ├── dim_picking.csv

│   ├── dim_ubicacion.csv

│   └── dim_calendario.csv

├── facts/

│   ├── fact_layout.csv

│   ├── fact_plan_reubicacion.csv

│   └── fact_historico.csv

├── metadata/

│   ├── metadata_modelo.csv

│   └── README.txt

└── logs/

==========================================================

DESCRIPCIÓN

Dimensiones

dim_producto
Información de los SKU.

dim_familia
Familias de productos.

dim_abcxyz
Clasificación ABC XYZ.

dim_estado
Estado del slotting.

dim_zona
Zona logística.

dim_picking
Tipo de picking.

dim_ubicacion
Ubicaciones físicas.

dim_calendario
Calendario para análisis temporal.

----------------------------------------------------------

Facts

fact_layout
Estado actual del layout.

fact_plan_reubicacion
Movimientos recomendados.

fact_historico
Histórico de todas las ejecuciones del algoritmo.

----------------------------------------------------------

Proyecto desarrollado por:

Daniel Ruiz

Ingeniería Industrial
Supply Chain Analytics
Inventory Optimization
Python + Power BI

==========================================================
"""

    archivo = (
        carpeta_metadata /
        "README.txt"
    )

    with open(
        archivo,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(contenido)

    print(
        "✓ README generado."
    )

def generar_log_exportacion(
    dimensiones,
    facts,
    carpeta_logs,
    version_algoritmo="1.0.0"
):
    """
    Genera un log sencillo de la exportación.
    """

    ahora = datetime.now()

    archivo = (
        carpeta_logs /
        "exportacion.log"
    )

    with open(
        archivo,
        "w",
        encoding="utf-8"
    ) as log:

        log.write(
            "=====================================\n"
        )

        log.write(
            "EXPORTACIÓN MODELO DIMENSIONAL\n"
        )

        log.write(
            "=====================================\n\n"
        )

        log.write(
            f"Fecha : {ahora.strftime('%Y-%m-%d')}\n"
        )

        log.write(
            f"Hora : {ahora.strftime('%H:%M:%S')}\n"
        )

        log.write(
            f"Versión : {version_algoritmo}\n\n"
        )

        log.write(
            "DIMENSIONES\n"
        )

        log.write(
            "--------------------------\n"
        )

        for nombre, tabla in dimensiones.items():

            log.write(
                f"{nombre}: {len(tabla):,} registros\n"
            )

        log.write("\n")

        log.write(
            "FACTS\n"
        )

        log.write(
            "--------------------------\n"
        )

        for nombre, tabla in facts.items():

            log.write(
                f"{nombre}: {len(tabla):,} registros\n"
            )

        log.write("\n")

        total = (
            sum(len(df) for df in dimensiones.values())
            +
            sum(len(df) for df in facts.values())
        )

        log.write(
            f"Total registros : {total:,}\n"
        )

        log.write(
            f"Total dimensiones : {len(dimensiones)}\n"
        )

        log.write(
            f"Total facts : {len(facts)}\n"
        )

        log.write(
            "\nProceso finalizado correctamente.\n"
        )

    print(
        "✓ Log de exportación generado."
    )

def crear_dimensiones(
    inventario,
    layout,
    ubicaciones_modelo
):
    """
    ======================================================
    Genera todas las dimensiones del modelo dimensional.
    ======================================================
    """

    print("\nGenerando dimensiones...")

    dimensiones = {

        "dim_producto": crear_dim_producto(
            inventario
        ),

        "dim_familia": crear_dim_familia(
            inventario
        ),

        "dim_abcxyz": crear_dim_abcxyz(
            inventario
        ),

        "dim_estado": crear_dim_estado(
            layout
        ),

        "dim_zona": crear_dim_zona(),

        "dim_picking": crear_dim_picking(),

        "dim_ubicacion": crear_dim_ubicacion(
            ubicaciones_modelo
        ),

        "dim_calendario": crear_dim_calendario()

    }

    print(
        f"✓ {len(dimensiones)} dimensiones creadas."
    )

    return dimensiones