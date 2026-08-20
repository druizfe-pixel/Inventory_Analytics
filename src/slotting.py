import logging

logger = logging.getLogger(__name__)


def asignar_prioridad(df):
    """
    Asigna la prioridad logística según la clasificación ABCXYZ.
    """

    prioridad = {
        "AX": "Muy Alta",
        "AY": "Muy Alta",
        "AZ": "Alta",
        "BX": "Alta",
        "BY": "Media",
        "BZ": "Media",
        "CX": "Media",
        "CY": "Baja",
        "CZ": "Baja",
        "N": "Excluir",
    }

    df["prioridad_slotting"] = (
        df["abcxyz"]
        .map(prioridad)
        .fillna("Sin clasificar")
    )

    logger.info("Prioridad de slotting asignada.")

    return df


def asignar_zona(df):
    """
    Asigna la zona recomendada de almacenamiento.
    """

    zonas = {
        "Muy Alta": "A",
        "Alta": "B",
        "Media": "C",
        "Baja": "D",
        "Excluir": "Revisar",
        "Sin clasificar": "Revisar",
    }

    df["zona_recomendada"] = (
        df["prioridad_slotting"]
        .map(zonas)
    )

    logger.info("Zona recomendada asignada.")

    return df


def asignar_tipo_picking(df):
    """
    Asigna el tipo de picking recomendado.
    """

    picking = {
        "AX": "Picking dinámico",
        "AY": "Picking dinámico",
        "AZ": "Picking dinámico",
        "BX": "Picking convencional",
        "BY": "Picking convencional",
        "BZ": "Picking convencional",
        "CX": "Reserva",
        "CY": "Reserva",
        "CZ": "Reserva",
        "N": "No aplica",
    }

    df["tipo_picking"] = (
        df["abcxyz"]
        .map(picking)
        .fillna("No definido")
    )

    logger.info("Tipo de picking asignado.")

    return df


def ejecutar_slotting(df):
    """
    Ejecuta todas las reglas de slotting.
    """

    df = asignar_prioridad(df)
    df = asignar_zona(df)
    df = asignar_tipo_picking(df)

    logger.info("Proceso de slotting finalizado.")

    return df