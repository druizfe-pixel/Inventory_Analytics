from pathlib import Path

import pandas as pd


def exportar_powerbi(
    inventario,
    layout,
    plan_reubicacion,
    ubicaciones,
    carpeta_salida = "powerbi"
):
    """
    Exporta todas las tablas necesarias para Power BI.
    """

    carpeta = Path(carpeta_salida)
    carpeta.mkdir(exist_ok=True)

    indicadores = generar_indicadores(
        inventario,
        layout,
        plan_reubicacion
    )

    inventario.to_csv(
        carpeta / "inventario.csv",
        index=False,
        encoding="utf-8-sig"
    )

    layout.to_csv(
        carpeta / "layout.csv",
        index=False,
        encoding="utf-8-sig"
    )

    plan_reubicacion.to_csv(
        carpeta / "plan_reubicacion.csv",
        index=False,
        encoding="utf-8-sig"
    )

    ubicaciones.to_csv(
        carpeta / "ubicaciones.csv",
        index=False,
        encoding="utf-8-sig"
    )

    indicadores.to_csv(
        carpeta / "indicadores.csv",
        index=False,
        encoding="utf-8-sig"
    )


    print("\nTablas para Power BI exportadas correctamente.")



def generar_indicadores(
    inventario,
    layout,
    plan_reubicacion
):
    """
    Genera la tabla de indicadores generales
    para el Dashboard Ejecutivo.
    """

    indicadores = pd.DataFrame([{

        "total_sku": inventario["codigo"].nunique(),

        "sku_reubicar": len(plan_reubicacion),

        "sku_correctos":
            (layout["estado_slotting"] == "Correcto").sum(),

        "sku_optimos":
            (layout["estado_slotting"] == "Óptimo").sum(),

        "sku_mover":
            layout["estado_slotting"].isin(
                [
                    "Mover urgente",
                    "Mover"
                ]
            ).sum(),

        "sku_sin_ubicacion":
            (layout["estado_slotting"] == "Sin ubicación").sum(),

        "distancia_promedio":
            round(
                layout["distancia_despacho"].mean(),
                2
            ),

        "distancia_total":
            round(
                layout["distancia_despacho"].sum(),
                2
            ),

        "ahorro_total":
            round(
                plan_reubicacion["ahorro_distancia"].sum(),
                2
            ),

        "eoq_promedio":
            round(
                inventario["eoq"].mean(),
                2
            ),

        "stock_seguridad_promedio":
            round(
                inventario["stock_seguridad"].mean(),
                2
            ),

        "punto_reorden_promedio":
            round(
                inventario["punto_reorden"].mean(),
                2
            )

    }])

    return indicadores