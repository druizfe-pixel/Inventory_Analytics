
==========================================================
 INVENTORY ANALYTICS & WAREHOUSE OPTIMIZATION
==========================================================

Modelo Dimensional para Power BI

Versión algoritmo : 1.0.0

Fecha generación : 2026-08-04

Hora generación  : 13:54:36

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

│   ├── fact_inventario.csv

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

fact_inventario
Información maestra del inventario.

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
