import logging
from src.eoq import resumen_eoq
from src.stock_seguridad import resumen_stock_seguridad
from src.punto_reorden import resumen_punto_reorden

logger = logging.getLogger(__name__)

def mostrar_resumen_abcxyz(df):
    """
    Muestra el resumen de la clasificación ABCXYZ.
    """

    logger.info(
        "\n%s",
        df["xyz"].value_counts(dropna=False)
    )

    logger.info(
        "\n%s",
        df["abcxyz"].value_counts(dropna=False)
    )

    logger.info(
        "\nProductos excluidos:\n%s",
        df.loc[
            ~df["demanda_valida_xyz"],
            ["codigo", "demanda_anual"]
        ]
    )


def mostrar_resumen_indicadores(df):
    """
    Muestra una muestra de los indicadores calculados.
    """

    columnas = [
        "codigo",
        "demanda_anual",
        "demanda_mensual",
        "demanda_diaria",
        "inventario",
        "inventario_promedio",
    ]

    logger.info(
        "\n%s",
        df[columnas].head(10)
    )

    columnas = [
        "codigo",
        "vr_unit",
        "costo_almacenar",
        "costo_mantenimiento_unitario",
    ]

    logger.info(
        "\n%s",
        df[columnas].head(10)
    )

def mostrar_resumen_eoq(df):
    """
    Muestra el resumen del modelo EOQ.
    """

    resumen_eoq(df)


def mostrar_resumen_stock(df):
    """
    Muestra estadísticas del stock de seguridad.
    """

    resumen_stock_seguridad(df)

def mostrar_resumen_punto_reorden(df):
    """
    Muestra estadísticas del punto de reorden.
    """

    resumen_punto_reorden(df)


def mostrar_reportes(df):
    """
    Ejecuta todos los reportes disponibles.
    """

    mostrar_resumen_abcxyz(df)

    mostrar_resumen_indicadores(df)

    mostrar_resumen_eoq(df)

    mostrar_resumen_stock(df)

    mostrar_resumen_punto_reorden(df)

