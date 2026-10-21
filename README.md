# 📦 Inventory Analytics

## Clasificación ABC-XYZ, Gestión de Inventarios y Optimización de Almacén

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458)
![NumPy](https://img.shields.io/badge/NumPy-Numerical-013243)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange) ![Power
BI](https://img.shields.io/badge/Power%20BI-Analytics-F2C811)
![Git](https://img.shields.io/badge/Git-Version%20Control-F05032)

------------------------------------------------------------------------

## 📌 Descripción

**Inventory Analytics** es una solución de analítica de inventarios
desarrollada con **Python y Power BI** para transformar información
operacional en decisiones de Supply Chain.

El proyecto integra metodologías de gestión de inventarios, análisis de
demanda y optimización de ubicaciones para construir una visión integral
de la operación de almacenamiento.

La solución permite:

-   Clasificación **ABC** por valor de consumo.
-   Clasificación **XYZ** por variabilidad de la demanda.
-   Matriz combinada **ABC-XYZ**.
-   Cálculo de **EOQ (Economic Order Quantity)**.
-   Cálculo de **Stock de Seguridad**.
-   Cálculo de **Punto de Reorden**.
-   Segmentación por tipo de picking.
-   Evaluación del estado de las ubicaciones.
-   Análisis de **Slotting**.
-   Optimización de Layout.
-   Identificación de SKU candidatos a reubicación.
-   Estimación de ahorro potencial.
-   Construcción de un modelo dimensional para Power BI.
-   Dashboard interactivo para análisis y toma de decisiones.

------------------------------------------------------------------------

# 🎯 Objetivo

Desarrollar una solución que permita pasar de una gestión tradicional
del inventario a un enfoque basado en datos, donde las decisiones
consideren simultáneamente:

**Valor del inventario + comportamiento de la demanda + variabilidad +
políticas de inventario + ubicación física + movimiento de los SKU.**

El objetivo final es **priorizar recursos, mejorar la disponibilidad,
optimizar el espacio y reducir desplazamientos innecesarios dentro del
almacén**.

------------------------------------------------------------------------

# 🏭 Caso de negocio

En una operación de almacenamiento, no todos los SKU deben gestionarse
de la misma manera.

Un producto de alto valor y demanda estable requiere una política
diferente a un producto de bajo valor y alta variabilidad. De la misma
forma, la ubicación física debe considerar el comportamiento de los
productos y su frecuencia de movimiento.

Por esta razón, el proyecto combina:

**ABC + XYZ + Inventario + Picking + Slotting + Layout**

para generar una visión integral de la operación.

------------------------------------------------------------------------

# 📊 Resultados principales

El dashboard desarrollado en Power BI consolida los principales
resultados del análisis.

## Inventario

  Indicador                   Resultado
  -------------------- ----------------
  SKU analizados                **770**
  Inventario total          **590 mil**
  Demanda anual          **6 millones**
  Valor de consumo        **\$40,1 MM**
  Stock de seguridad        **155 mil**
  Punto de reorden          **262 mil**

------------------------------------------------------------------------

# 🔬 Clasificación ABC

La clasificación ABC segmenta los productos según su importancia
económica.

  Clasificación         SKU   Participación
  --------------- --------- ---------------
  A                     134          17,4 %
  B                     182          23,6 %
  C                     454          59,0 %
  **Total**         **770**       **100 %**

Aunque la mayor cantidad de referencias pertenece a la categoría C, el
impacto económico está fuertemente concentrado en la categoría A.

### Valor de consumo

  Clasificación     Valor aproximado
  --------------- ------------------
  A                      **\$32 MM**
  B                       **\$6 MM**
  C                       **\$2 MM**

**Hallazgo:** aproximadamente el **80 % del valor de consumo** se
concentra en los SKU categoría A. Esto respalda la necesidad de aplicar
niveles de control diferenciados.

------------------------------------------------------------------------

# 📈 Clasificación XYZ

La clasificación XYZ incorpora la variabilidad del comportamiento de la
demanda.

  Clasificación         SKU   Participación aprox.
  --------------- --------- ----------------------
  X                      59                  7,7 %
  Y                     100                 13,0 %
  Z                     605                 78,6 %
  N                       6                  0,8 %
  **Total**         **770**              **100 %**

El resultado muestra una **alta concentración de SKU en la categoría
Z**.

Esto representa un reto para las políticas de abastecimiento, ya que una
proporción importante del portafolio presenta un comportamiento de
demanda menos estable.

------------------------------------------------------------------------

# 🧩 Matriz ABC-XYZ

La combinación de ambas metodologías permite identificar simultáneamente
importancia económica y variabilidad.

  Clasificación         SKU
  --------------- ---------
  **CZ**            **443**
  BZ                    126
  AY                     51
  AX                     47
  BY                     44
  AZ                     36
  BX                     12
  N                       6
  CY                      5

La combinación **CZ concentra 443 de 770 SKU**, aproximadamente **57,5 %
del portafolio**.

Esto convierte a CZ en el principal segmento por cantidad de referencias
y en un grupo relevante para definir políticas específicas de inventario
y abastecimiento.

------------------------------------------------------------------------

# 📦 Políticas de inventario

El proyecto incorpora herramientas para establecer políticas de
reposición y niveles de inventario.

## EOQ --- Economic Order Quantity

  Indicador                  Resultado
  -------------------- ---------------
  EOQ promedio           **14,15 mil**
  Stock de seguridad       **155 mil**
  Punto de reorden         **262 mil**
  Costo total EOQ          **193 mil**

El EOQ permite estimar una cantidad económica de pedido orientada a
equilibrar los costos asociados al abastecimiento y mantenimiento del
inventario.

------------------------------------------------------------------------

# 🚨 Punto de reorden

El análisis identifica:

  Estado                         SKU   Participación
  ------------------------ --------- ---------------
  Sobre punto de reorden     **567**        **74 %**
  Bajo punto de reorden      **203**        **26 %**
  **Total**                  **770**       **100 %**

El **26 % del portafolio se encuentra bajo el punto de reorden**,
constituyendo un grupo prioritario para revisión de abastecimiento.

------------------------------------------------------------------------

# 📍 Slotting

El módulo de Slotting analiza la correspondencia entre los SKU y sus
ubicaciones actuales.

## Indicadores principales

  Indicador             Resultado
  ------------------- -----------
  SKU totales             **770**
  SKU óptimos             **136**
  SKU mover                **15**
  SKU mover urgente        **51**
  SKU sin ubicación       **165**
  Ahorro potencial        **364**

### Estado del Slotting

  Estado            Participación
  --------------- ---------------
  Correcto            **45,84 %**
  Sin ubicación       **21,43 %**
  Óptimo              **17,66 %**
  Mover urgente        **6,62 %**
  Aceptable            **5,71 %**

El análisis identifica oportunidades relevantes relacionadas con SKU sin
ubicación y referencias que requieren movimiento.

------------------------------------------------------------------------

# 🚚 Tipo de Picking

La distribución de SKU por tipo de picking es:

  Tipo                         SKU
  ---------------------- ---------
  Reserva                  **448**
  Picking convencional     **182**
  Picking dinámico         **134**
  No aplica                  **6**

Esta información permite relacionar las características del inventario
con las necesidades operativas del almacén.

------------------------------------------------------------------------

# 🗺️ Optimización del Layout

El módulo de Layout analiza el impacto potencial de reubicar productos.

## Resultados

  Indicador                        Resultado
  ---------------------------- -------------
  SKU a reubicar                      **66**
  Distancia actual               **≈ 2 mil**
  Distancia nueva                **≈ 1 mil**
  Ahorro potencial                   **364**
  Reducción de distancia            **24 %**
  Mejora promedio de ranking         **210**

La propuesta de reubicación permite reducir potencialmente los
desplazamientos asociados a la ubicación actual de los productos.

### Ahorro potencial por zona

  Zona     Ahorro aproximado
  ------ -------------------
  A                  **305**
  B                   **49**
  C                   **11**

La zona A concentra la mayor oportunidad de ahorro potencial.

------------------------------------------------------------------------

# 💰 Oportunidad de ahorro

El modelo estima un:

## **364 de ahorro potencial**

asociado a las oportunidades de reubicación identificadas.

Además, la optimización del layout muestra una:

## **24 % de reducción potencial de distancia**

Estos resultados permiten priorizar intervenciones físicas en el almacén
con base en impacto potencial.

------------------------------------------------------------------------

# 📊 Dashboard Power BI

El análisis fue consolidado en un dashboard interactivo desarrollado en
Microsoft Power BI.

El dashboard se estructura en las siguientes vistas:

``` text
Overview
   │
   ├── Inventario
   │
   ├── Slotting
   │
   ├── Layout
   │
   ├── EOQ
   │
   ├── Reubicaciones
   │
   └── Histórico
```

## Overview

![Inventory Analytics Dashboard](Indicadores%20Almacen.jpeg)

> Para una visualización completa del dashboard, consultar
> `Inventory_Analytics_Dashboard.pbix`.

------------------------------------------------------------------------

# 🧱 Modelo dimensional

Para facilitar el análisis en Power BI se construyó un modelo
dimensional.

``` text
                         Dim Producto
                              │
                              │
Dim Familia ─────────── Fact Histórico ───────── Dim Calendario
                              │
                              │
                        Dim Ubicación
                              │
                              │
                           Dim Zona
```

El proceso genera dimensiones y tablas de hechos para alimentar el
modelo analítico.

### Principales estructuras

``` text
output/
└── powerbi/
    ├── dimensions/
    │   ├── dim_abcxyz.csv
    │   ├── dim_calendario.csv
    │   ├── dim_estado.csv
    │   ├── dim_familia.csv
    │   ├── dim_picking.csv
    │   ├── dim_producto.csv
    │   ├── dim_ubicacion.csv
    │   └── dim_zona.csv
    │
    ├── facts/
    │   ├── fact_historico.csv
    │   ├── fact_layout.csv
    │   └── fact_plan_reubicacion.csv
    │
    ├── metadata/
    │   └── metadata_modelo.csv
    │
    ├── indicadores.csv
    ├── inventario.csv
    ├── layout.csv
    ├── plan_reubicacion.csv
    └── ubicaciones.csv
```

------------------------------------------------------------------------

# 🐍 Arquitectura Python

El procesamiento se encuentra modularizado dentro de `src/`.

``` text
src/
│
├── abcxyz.py
├── cargar_datos.py
├── config.py
├── constants.py
├── dimensional_model.py
├── eoq.py
├── exportar.py
├── exportar_modelo.py
├── export_helpers.py
├── indicadores.py
├── layout_assignment.py
├── layout_optimizer.py
├── limpieza.py
├── pipeline.py
├── powerbi_export.py
├── punto_reorden.py
├── reportes.py
├── slotting.py
├── stock_seguridad.py
├── transformacion.py
├── utilidades.py
├── validar_modelo.py
└── visualizaciones.py
```

La separación por módulos permite mantener independientes las diferentes
etapas del procesamiento y facilita la reutilización de componentes.

------------------------------------------------------------------------

# 🔄 Flujo de procesamiento

``` text
                 DATOS RAW
                     │
                     ▼
              Carga de datos
                     │
                     ▼
                  Limpieza
                     │
                     ▼
              Transformación
                     │
                     ▼
              ┌──────────────┐
              │   ABC - XYZ  │
              └──────┬───────┘
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
    Políticas de             Slotting
     inventario                 │
          │                     ▼
    ┌─────┼─────┐            Layout
    ▼     ▼     ▼               │
   EOQ  Stock   ROP             ▼
        seguridad          Reubicación
          │                     │
          └──────────┬──────────┘
                     ▼
             Modelo dimensional
                     │
                     ▼
                  Power BI
                     │
                     ▼
             Toma de decisiones
```

------------------------------------------------------------------------

# 📂 Estructura del proyecto

``` text
EOQ_Python/
│
├── data/
│   └── raw/
│       ├── Ejercicio ABCXYZ Blank.csv
│       ├── Ejercicio ABCXYZ Blank.xlsx
│       ├── ubicaciones.csv
│       └── ubicaciones.xlsx
│
├── notebooks/
│   └── EOQ_proyecto.ipynb
│
├── output/
│   ├── inventario_procesado.xlsx
│   └── powerbi/
│       ├── dimensions/
│       ├── facts/
│       ├── metadata/
│       └── datasets analíticos
│
├── powerbi/
│   ├── inventario.csv
│   ├── layout.csv
│   └── plan_reubicacion.csv
│
├── src/
│   ├── abcxyz.py
│   ├── eoq.py
│   ├── stock_seguridad.py
│   ├── punto_reorden.py
│   ├── slotting.py
│   ├── layout_optimizer.py
│   ├── dimensional_model.py
│   ├── pipeline.py
│   └── ...
│
├── main.py
├── Inventory_Analytics_Dashboard.pbix
├── DOCUMENTO DE DISEÑO DEL DASHBOARD.docx
├── Indicadores Almacen.jpeg
├── requirements.txt
├── readme.md
└── .gitignore
```

------------------------------------------------------------------------

# 🛠️ Tecnologías utilizadas

  Tecnología             Aplicación
  ---------------------- ----------------------------------------
  **Python**             Desarrollo del sistema
  **Pandas**             Manipulación y transformación de datos
  **NumPy**              Cálculos numéricos
  **Jupyter Notebook**   Exploración y análisis
  **Power BI**           Business Intelligence y visualización
  **Excel / CSV**        Fuentes y datasets
  **Git / GitHub**       Control de versiones

------------------------------------------------------------------------

# 🚀 Ejecución

## 1. Clonar el repositorio

``` bash
git clone https://github.com/USUARIO/Clasificacion_ABCXYZ.git
cd Clasificacion_ABCXYZ
```

## 2. Crear entorno virtual

``` bash
python -m venv .venv
```

## 3. Activar entorno virtual

### Windows

``` powershell
.venv\Scripts\activate
```

### Linux / macOS

``` bash
source .venv/bin/activate
```

## 4. Instalar dependencias

``` bash
pip install -r requirements.txt
```

## 5. Ejecutar el pipeline

``` bash
python main.py
```

------------------------------------------------------------------------

# 📓 Notebook

El análisis y desarrollo inicial se encuentra en:

``` text
notebooks/EOQ_proyecto.ipynb
```

El notebook documenta el proceso de análisis, transformación y
construcción de los componentes relacionados con la gestión de
inventarios.

------------------------------------------------------------------------

# 📊 Power BI

El archivo principal del dashboard es:

``` text
Inventory_Analytics_Dashboard.pbix
```

Las tablas utilizadas por el modelo de BI son generadas mediante los
procesos desarrollados en Python y se encuentran principalmente en:

``` text
output/powerbi/
```

------------------------------------------------------------------------

# 🔎 Principales hallazgos

## 1. Concentración económica

Aunque el **59 % de los SKU pertenece a la categoría C**, los productos
A concentran aproximadamente **\$32 MM de los \$40,1 MM de valor de
consumo**.

Esto evidencia la necesidad de aplicar diferentes niveles de control
según el impacto económico.

------------------------------------------------------------------------

## 2. Alta variabilidad

El **78,6 % de los SKU se clasifican como Z**, mostrando una alta
concentración de referencias con variabilidad elevada de demanda.

Esto debe ser considerado al definir niveles de seguridad y políticas de
reposición.

------------------------------------------------------------------------

## 3. Dominio de CZ

La combinación **CZ representa aproximadamente el 57,5 % del
portafolio**.

Esta concentración permite identificar un grupo prioritario para definir
estrategias específicas de abastecimiento y control.

------------------------------------------------------------------------

## 4. Riesgo de reposición

**203 SKU**, equivalentes al **26 %**, se encuentran bajo el punto de
reorden.

Este grupo debe ser objeto de revisión para evitar posibles problemas de
disponibilidad.

------------------------------------------------------------------------

## 5. Oportunidad de Slotting

Se identifican:

-   **165 SKU sin ubicación**.
-   **51 SKU con movimiento urgente**.
-   **66 SKU candidatos a reubicación**.

Esto representa una oportunidad de mejora de la organización física del
almacén.

------------------------------------------------------------------------

## 6. Optimización del Layout

La propuesta de reubicación muestra una:

**24 % de reducción potencial de distancia**

y un:

**364 de ahorro potencial**.

La mayor oportunidad de ahorro se concentra en la zona A.

------------------------------------------------------------------------

# 🎯 Valor para el negocio

El principal aporte del proyecto es integrar en una misma solución tres
dimensiones que normalmente pueden analizarse de manera independiente:

``` text
                    INVENTARIO
                        │
             ┌──────────┴──────────┐
             │                     │
          ABC-XYZ              Políticas
             │                 de inventario
             │                     │
             └──────────┬──────────┘
                        │
                        ▼
                    OPERACIÓN
                        │
                 Slotting / Layout
                        │
                        ▼
                  OPTIMIZACIÓN
                        │
                        ▼
               DECISIONES DE
                SUPPLY CHAIN
```

La solución permite responder preguntas de negocio como:

-   **¿Qué productos requieren mayor control?**
-   **¿Qué productos presentan mayor variabilidad?**
-   **¿Cuánto inventario mantener?**
-   **¿Cuándo reponer?**
-   **¿Qué SKU requieren atención inmediata?**
-   **¿Dónde ubicar los productos?**
-   **¿Qué productos mover primero?**
-   **¿Dónde existe mayor oportunidad de ahorro?**

De esta manera, el proyecto evoluciona desde un análisis descriptivo
hacia un enfoque de **analítica prescriptiva aplicada a Supply Chain**.

------------------------------------------------------------------------

# 🔮 Próximas mejoras

-   Incorporar pronósticos de demanda.
-   Automatizar actualización de datasets.
-   Incorporar escenarios de simulación.
-   Integrar costos reales de almacenamiento y abastecimiento.
-   Automatizar políticas ABC-XYZ.
-   Incorporar alertas de inventario.
-   Integrar fuentes transaccionales.
-   Automatizar actualización del dashboard.
-   Incorporar optimización matemática avanzada para Slotting.
-   Desarrollar una aplicación web para consulta de resultados.

------------------------------------------------------------------------

# 👨‍💻 Autor

## Daniel Ruiz

**Ingeniero Industrial**\
**Especialista en Ingeniería de Operaciones**

**Supply Chain · Inventory Management · Data Science · Business
Intelligence**

### Tecnologías

`Python` · `Pandas` · `Power BI` · `SQL` · `Supply Chain` ·
`Inventory Management`

------------------------------------------------------------------------

# ⭐ Proyecto de portafolio

Este proyecto integra:

**Inventory Management + Data Analytics + Python + Business
Intelligence + Warehouse Optimization**

para transformar datos operacionales en **información accionable y
decisiones de Supply Chain**.


# EOQ Streamlit

Aplicación de análisis y optimización de inventarios desarrollada con Python y Streamlit, basada en el proyecto EOQ.

## Archivos principales

- `Streamlit/app.py`: interfaz para cargar datos, consultar resultados y descargar los cálculos.
- `Streamlit/eoq_engine.py`: motor de cálculo reutilizable para el análisis de inventarios.
- `notebooks/EOQ_proyecto.ipynb`: notebook original del análisis.
- `notebooks/EOQ_proyecto_estructurado.ipynb`: versión estructurada del notebook.

## Ejecutar en Windows

Desde la carpeta raíz del proyecto:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run Streamlit/app.py
```

## Datos de entrada

El archivo CSV de inventarios debe incluir las columnas `Código`, `Descripción`, `Vr Unit`, `Costo Ordenar`, `Costo Almacenar` e `Inventario`, además de las columnas mensuales de demanda que utiliza el notebook. Se admiten los nombres de las columnas mensuales con o sin sufijo `.1`, según la estructura de los datos.

El separador predeterminado del CSV es `;`.

El archivo de ubicaciones es opcional y debe incluir `SKU`, `X`, `Y` y `Z`.

## Fórmulas y parámetros

- **ABC:** clasificación por valor de consumo acumulado: A hasta el 80 %, B hasta el 95 % y C para el restante.
- **XYZ:** X para CV ≤ 0,50; Y para CV ≤ 1,00; Z para valores superiores.
- **EOQ:** raíz cuadrada de (2 × demanda anual × costo de ordenar / costo de mantener).
- **Stock de seguridad:** Z × desviación estándar de la demanda diaria × raíz cuadrada del lead time.
- **Punto de reorden:** demanda diaria × lead time + stock de seguridad.

Los parámetros iniciales documentados son 15 días de lead time, Z = 1,65 y 30 días por mes. Se pueden modificar desde la barra lateral de la aplicación, si esa funcionalidad está habilitada en la versión actual.