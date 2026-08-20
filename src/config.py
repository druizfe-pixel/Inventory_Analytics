"""
config.py

Configuración general del proyecto
Inventory Analytics
"""

from pathlib import Path

# ==========================
# Directorio principal
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================
# Carpetas
# ==========================

DATA = BASE_DIR / "data"

RAW_DATA = DATA / "raw"

PROCESSED_DATA = DATA / "processed"

OUTPUTS = BASE_DIR / "outputs"

GRAFICOS = OUTPUTS / "graficos"

REPORTES = OUTPUTS / "reportes"

POWERBI = BASE_DIR / "powerbi"

# ==========================
# Archivos
# ==========================

INVENTARIO = RAW_DATA / "Ejercicio ABCXYZ Blank.xlsx"

UBICACIONES = RAW_DATA / "ubicaciones.xlsx"


# ==========================
# INVENTARIOS
# ==========================

LEAD_TIME_DEFAULT = 7
NIVEL_SERVICIO_DEFAULT = 0.95

# ==========================
# DEMANDA
# ==========================

DIAS_ANIO = 365
DIAS_MES = 365 / 12

# ==========================
# CLASIFICACIÓN ABC
# ==========================

ABC_A = 0.80
ABC_B = 0.95

# ==========================
# CLASIFICACIÓN XYZ
# ==========================

XYZ_X = 0.20
XYZ_Y = 0.50

"""
Constantes del proyecto.
"""

# ===============================
# Valores Z
# ===============================

NIVELES_SERVICIO = {
    0.90: 1.28,
    0.95: 1.65,
    0.97: 1.88,
    0.98: 2.05,
    0.99: 2.33,
}