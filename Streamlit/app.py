"""Interfaz Streamlit del proyecto EOQ, alineada con el notebook estructurado."""
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from eoq_engine import leer_csv, procesar_inventario, procesar_ubicaciones

st.set_page_config(page_title="EOQ | Gestión de inventarios", page_icon="📦", layout="wide")
st.title("📦 Análisis de inventarios")
st.caption("EOQ · Clasificación ABC/XYZ · Reabastecimiento · Mapa 3D de ubicaciones")

with st.sidebar:
    st.header("Parámetros del modelo")
    lead_time = st.number_input("Lead time (días)", min_value=0.0, value=15.0, step=1.0)
    z = st.number_input("Factor Z de servicio", min_value=0.0, value=1.65, step=0.05)
    dias_mes = st.number_input("Días por mes", min_value=1.0, value=30.0, step=1.0)
    separador = st.selectbox("Separador del CSV", [";", ",", "\t"], index=0,
                            format_func=lambda x: "Tabulación" if x == "\t" else x)
    st.divider()
    st.caption("La tasa de Costo Almacenar se interpreta como tasa anual aplicada al valor unitario, igual que en el notebook.")

st.markdown(
    "Carga el archivo de inventario. Para habilitar el mapa físico, carga también "
    "un CSV de ubicaciones con las columnas `SKU`, `X`, `Y` y `Z`."
)
col_a, col_b = st.columns(2)
with col_a:
    archivo = st.file_uploader("Inventario (.csv)", type=["csv"])
with col_b:
    archivo_ubic = st.file_uploader("Ubicaciones (.csv, opcional)", type=["csv"], key="ubicaciones")


def grafico_3d(ubic):
    fig = plt.figure(figsize=(11, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(
        ubic["X"], ubic["Y"], ubic["Z"],
        c=ubic["Color"],
        s=ubic["PrioridadGrafico"] * 30,
        alpha=0.8,
        edgecolors="black",
        linewidths=0.25,
    )
    ax.set_xlabel("Pasillo (X)")
    ax.set_ylabel("Posición (Y)")
    ax.set_zlabel("Nivel (Z)")
    ax.set_title("Mapa 3D del Centro de Distribución")
    ax.grid(True)
    fig.tight_layout()
    return fig


def grafico_xy(ubic):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(ubic["X"], ubic["Y"], c=ubic["Color"], s=35, alpha=0.8)
    ax.set_xlabel("Pasillo (X)")
    ax.set_ylabel("Posición (Y)")
    ax.set_title("Vista superior del Centro de Distribución")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    return fig


def grafico_xz(ubic):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(ubic["X"], ubic["Z"], c=ubic["Color"], s=35, alpha=0.8)
    ax.set_xlabel("Pasillo (X)")
    ax.set_ylabel("Nivel (Z)")
    ax.set_title("Vista vertical de ubicaciones")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    return fig


if archivo:
    try:
        raw = leer_csv(archivo, sep=separador)
        resultado = procesar_inventario(raw, lead_time=lead_time, z=z, dias_mes=dias_mes)
        st.success(f"Procesamiento completado: {len(resultado):,} referencias.")

        total_valor = resultado["Valor Consumo"].sum()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Referencias", f"{len(resultado):,}")
        c2.metric("Valor de consumo", f"{total_valor:,.2f}")
        c3.metric("Referencias clase A", f"{(resultado['ABC'] == 'A').sum():,}")
        c4.metric("EOQ calculable", f"{resultado['EOQ'].notna().sum():,}")

        tabs = st.tabs(["Resumen", "ABC/XYZ", "EOQ y reabastecimiento", "Datos completos", "Ubicaciones 3D"])
        with tabs[0]:
            st.subheader("Valor de consumo por clase ABC")
            resumen = resultado.groupby("ABC", dropna=False)["Valor Consumo"].sum().reindex(["A", "B", "C", "N"], fill_value=0)
            st.bar_chart(resumen)
            if "Familia" in resultado.columns:
                st.subheader("Top 10 familias por valor de consumo")
                familias = resultado.groupby("Familia", dropna=False)["Valor Consumo"].sum().nlargest(10)
                st.bar_chart(familias)
            st.subheader("20 referencias de mayor demanda anual")
            cols_top = ["Código", "Descripción", "Demanda Anual", "ABCXYZ"]
            st.dataframe(resultado.nlargest(20, "Demanda Anual")[cols_top], use_container_width=True)

        with tabs[1]:
            st.subheader("Matriz ABC/XYZ")
            tabla = pd.crosstab(resultado["ABC"], resultado["XYZ"]).reindex(
                index=["A", "B", "C", "N"], columns=["X", "Y", "Z", "N"], fill_value=0
            )
            st.dataframe(tabla, use_container_width=True)
            st.subheader("Participación porcentual")
            st.dataframe((tabla / max(int(tabla.to_numpy().sum()), 1) * 100).round(1), use_container_width=True)
            st.subheader("Referencias por clase ABCXYZ")
            st.bar_chart(resultado["ABCXYZ"].value_counts().sort_index())

        with tabs[2]:
            st.subheader("Inventario actual frente a EOQ")
            st.scatter_chart(resultado.dropna(subset=["Inventario", "EOQ"]), x="Inventario", y="EOQ", color="ABCXYZ")
            st.subheader("Referencias con mayor punto de reorden")
            cols = ["Código", "Descripción", "Inventario", "EOQ", "Stock Seguridad", "Punto Reorden", "ABCXYZ", "Estado Reposicion"]
            st.dataframe(resultado.nlargest(20, "Punto Reorden")[cols], use_container_width=True)
            st.subheader("Rotación frente a cobertura")
            rot = resultado.dropna(subset=["Rotacion", "Cobertura Meses"])
            if not rot.empty:
                st.scatter_chart(rot, x="Cobertura Meses", y="Rotacion", color="ABCXYZ")
            else:
                st.info("No hay suficientes datos para graficar rotación y cobertura.")

        with tabs[3]:
            busqueda = st.text_input("Buscar por código o descripción")
            vista = resultado
            if busqueda:
                mask = resultado["Código"].astype(str).str.contains(busqueda, case=False, na=False) | resultado["Descripción"].astype(str).str.contains(busqueda, case=False, na=False)
                vista = resultado[mask]
            st.dataframe(vista, use_container_width=True, height=500)
            st.download_button(
                "Descargar resultados completos (CSV)",
                resultado.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig"),
                "inventario_procesado_eoq.csv", "text/csv",
            )

        with tabs[4]:
            if archivo_ubic:
                try:
                    ubic_raw = leer_csv(archivo_ubic, sep=separador)
                    ubic = procesar_ubicaciones(ubic_raw, resultado)
                    validas = ubic.dropna(subset=["X", "Y", "Z"])
                    if validas.empty:
                        st.warning("No hay coordenadas X, Y y Z válidas para representar.")
                    else:
                        st.caption("El color y tamaño de cada punto representan la prioridad ABC/XYZ. Las referencias sin clase se muestran en gris.")
                        t3d, txy, txz, tdatos = st.tabs(["Mapa 3D", "Vista superior X/Y", "Vista vertical X/Z", "Datos de ubicación"])
                        with t3d:
                            st.pyplot(grafico_3d(validas), use_container_width=True)
                        with txy:
                            st.pyplot(grafico_xy(validas), use_container_width=True)
                        with txz:
                            st.pyplot(grafico_xz(validas), use_container_width=True)
                        with tdatos:
                            st.dataframe(ubic, use_container_width=True)
                        st.metric("Ubicaciones", f"{len(ubic):,}")
                        st.metric("Ubicaciones sin clase", f"{ubic['ABCXYZ'].isna().sum():,}")
                        st.download_button(
                            "Descargar ubicaciones clasificadas",
                            ubic.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig"),
                            "ubicaciones_clasificadas.csv", "text/csv",
                        )
                except Exception as exc:
                    st.error(f"No se pudieron procesar las ubicaciones: {exc}")
            else:
                st.info("Carga un CSV de ubicaciones con columnas SKU, X, Y y Z para activar el mapa 3D.")
    except Exception as exc:
        st.error(f"No se pudo procesar el archivo: {exc}")
        st.markdown(
            "Verifica que el CSV incluya `Código`, `Descripción`, `Vr Unit`, "
            "`Costo Ordenar`, `Costo Almacenar`, `Inventario` y los 12 meses de demanda "
            "de sep-18 a ago-19."
        )
else:
    st.info("Carga un CSV de inventario para iniciar el análisis.")
    with st.expander("Columnas esperadas"):
        st.write("Código, Descripción, Vr Unit, Costo Ordenar, Costo Almacenar, Inventario y meses de sep-18 a ago-19. Familia, Grupo, Línea y Pedidos son opcionales.")
