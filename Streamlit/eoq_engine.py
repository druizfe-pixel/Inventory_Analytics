"""Motor compartido de análisis EOQ, ABC/XYZ y ubicaciones.

La lógica sigue el notebook EOQ_proyecto_estructurado.ipynb.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

MESES_NOTEBOOK = [
    "sep-18.1", "oct-18.1", "nov-18.1", "dic-18.1",
    "ene-19.1", "feb-19.1", "mar-19.1", "abr-19.1",
    "may-19.1", "jun-19.1", "jul-19.1", "ago-19.1",
]
MESES_SIN_SUFIJO = [m.removesuffix(".1") for m in MESES_NOTEBOOK]
PRIORIDAD = {
    "AX": 9, "AY": 8, "AZ": 7,
    "BX": 6, "BY": 5, "BZ": 4,
    "CX": 3, "CY": 2, "CZ": 1,
}


def leer_csv(archivo, sep=";") -> pd.DataFrame:
    """Lee CSV con BOM y normaliza los encabezados."""
    df = pd.read_csv(archivo, sep=sep, encoding="utf-8-sig")
    df.columns = df.columns.astype(str).str.strip()
    return df


def _numerico(serie: pd.Series) -> pd.Series:
    """Convierte valores numéricos con coma decimal o punto decimal."""
    if pd.api.types.is_numeric_dtype(serie):
        return pd.to_numeric(serie, errors="coerce")
    s = serie.astype("string").str.strip().str.replace(" ", "", regex=False)
    con_coma = s.str.contains(",", regex=False, na=False)
    s.loc[con_coma] = (
        s.loc[con_coma]
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    return pd.to_numeric(s, errors="coerce")


def procesar_inventario(
    datos: pd.DataFrame,
    lead_time: float = 15,
    z: float = 1.65,
    dias_mes: float = 30,
) -> pd.DataFrame:
    """Calcula indicadores alineados con el notebook estructurado."""
    if dias_mes <= 0:
        raise ValueError("Días por mes debe ser mayor que cero.")
    if lead_time < 0:
        raise ValueError("Lead time no puede ser negativo.")
    if z < 0:
        raise ValueError("El factor Z no puede ser negativo.")

    df = datos.copy()
    df.columns = df.columns.astype(str).str.strip()
    requeridas = [
        "Código", "Descripción", "Vr Unit", "Costo Ordenar",
        "Costo Almacenar", "Inventario",
    ]
    faltan = [c for c in requeridas if c not in df.columns]
    if faltan:
        raise ValueError("Faltan columnas obligatorias: " + ", ".join(faltan))

    meses = [m for m in MESES_NOTEBOOK if m in df.columns]
    if len(meses) != 12:
        meses = [m for m in MESES_SIN_SUFIJO if m in df.columns]
    if len(meses) != 12:
        raise ValueError(
            "Se requieren los 12 meses de demanda de sep-18 a ago-19, "
            "con sufijo .1 o sin él."
        )

    numericas = set(meses + ["Vr Unit", "Costo Ordenar", "Costo Almacenar", "Inventario"])
    if "Pedidos" in df.columns:
        numericas.add("Pedidos")
    for col in numericas:
        df[col] = _numerico(df[col])
    for col in ["Código", "Descripción", "Familia", "Grupo", "Línea"]:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

    df_demanda = df[meses].clip(lower=0)
    df["Demanda Anual"] = df_demanda.sum(axis=1, min_count=1)
    df["Demanda Promedio"] = df_demanda.mean(axis=1)
    df["Desv"] = df_demanda.std(axis=1, ddof=1)
    df["Valor Consumo"] = df["Demanda Anual"] * df["Vr Unit"]

    df = df.sort_values("Valor Consumo", ascending=False, na_position="last").copy()
    valor_total = df["Valor Consumo"].where(df["Valor Consumo"] > 0).sum()
    if pd.notna(valor_total) and valor_total > 0:
        df["Participacion"] = df["Valor Consumo"].clip(lower=0) / valor_total
        df["Acumulado"] = df["Participacion"].cumsum()
        df["ABC"] = np.select(
            [
                df["Valor Consumo"].isna() | (df["Valor Consumo"] <= 0),
                df["Acumulado"] <= 0.80,
                df["Acumulado"] <= 0.95,
            ],
            ["N", "A", "B"],
            default="C",
        )
    else:
        df["Participacion"] = np.nan
        df["Acumulado"] = np.nan
        df["ABC"] = "N"

    df["CV"] = np.where(
        df["Demanda Promedio"] > 0,
        df["Desv"] / df["Demanda Promedio"],
        np.nan,
    )
    df["XYZ"] = np.select(
        [df["CV"].isna(), df["CV"] <= 0.50, df["CV"] <= 1.00],
        ["N", "X", "Y"],
        default="Z",
    )
    df["ABCXYZ"] = np.where(
        (df["ABC"] != "N") & (df["XYZ"] != "N"),
        df["ABC"] + df["XYZ"],
        "N",
    )

    df["Costo Mantener"] = df["Vr Unit"] * df["Costo Almacenar"]
    condicion_eoq = (
        (df["Demanda Anual"] > 0)
        & (df["Costo Ordenar"] > 0)
        & (df["Costo Mantener"] > 0)
    )
    df["EOQ"] = np.nan
    df.loc[condicion_eoq, "EOQ"] = np.sqrt(
        2 * df.loc[condicion_eoq, "Demanda Anual"]
        * df.loc[condicion_eoq, "Costo Ordenar"]
        / df.loc[condicion_eoq, "Costo Mantener"]
    )
    df["Rotacion"] = np.where(
        df["Inventario"] > 0, df["Demanda Anual"] / df["Inventario"], np.nan
    )
    df["Cobertura Meses"] = np.where(
        df["Demanda Promedio"] > 0,
        df["Inventario"] / df["Demanda Promedio"],
        np.nan,
    )
    df["Demanda Diaria"] = df["Demanda Promedio"] / dias_mes
    df["Desv Diaria"] = df["Desv"] / np.sqrt(dias_mes)
    df["Stock Seguridad"] = z * df["Desv Diaria"] * np.sqrt(lead_time)
    df["Punto Reorden"] = (
        df["Demanda Diaria"] * lead_time + df["Stock Seguridad"]
    )
    df["Estado Reposicion"] = np.select(
        [df["Inventario"].isna(), df["Inventario"] <= df["Punto Reorden"]],
        ["Sin dato", "Revisar reposición"],
        default="Sobre punto de reorden",
    )
    return df.reset_index(drop=True)


def procesar_ubicaciones(datos_ubicaciones: pd.DataFrame, inventario: pd.DataFrame) -> pd.DataFrame:
    """Cruza coordenadas X/Y/Z con ABCXYZ y prepara color/tamaño para el mapa."""
    u = datos_ubicaciones.copy()
    u.columns = u.columns.astype(str).str.strip()
    requeridas = ["SKU", "X", "Y", "Z"]
    faltan = [c for c in requeridas if c not in u.columns]
    if faltan:
        raise ValueError("Faltan columnas en ubicaciones: " + ", ".join(faltan))
    for col in ["X", "Y", "Z"]:
        u[col] = _numerico(u[col])
    u["SKU"] = u["SKU"].astype("string").str.strip()
    u = u.drop_duplicates(subset="SKU", keep="first").copy()

    if not {"Código", "ABCXYZ"}.issubset(inventario.columns):
        raise ValueError("El inventario procesado debe incluir Código y ABCXYZ.")
    mapa_clase = inventario[["Código", "ABCXYZ"]].copy()
    mapa_clase["Código"] = mapa_clase["Código"].astype("string").str.strip()
    mapa_clase = mapa_clase.drop_duplicates(subset="Código", keep="first")
    u = u.merge(mapa_clase, left_on="SKU", right_on="Código", how="left")
    u["Prioridad"] = u["ABCXYZ"].map(PRIORIDAD)

    def color_por_prioridad(valor):
        if pd.isna(valor):
            return "gray"
        if valor >= 7:
            return "red"
        if valor >= 5:
            return "orange"
        if valor >= 3:
            return "yellow"
        return "green"

    u["Color"] = u["Prioridad"].apply(color_por_prioridad)
    u["PrioridadGrafico"] = (
        pd.to_numeric(u["Prioridad"], errors="coerce").fillna(1).clip(1, 9)
    )
    return u.reset_index(drop=True)
