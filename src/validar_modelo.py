import pandas as pd


def validar_dimension(
    df,
    clave,
    nombre_dimension
):
    """
    ==========================================================
    Valida una dimensión del modelo dimensional.

    Verifica:

    • La tabla no esté vacía.
    • La clave exista.
    • No existan valores nulos.
    • No existan claves duplicadas.

    Retorna True si la dimensión es válida.
    ==========================================================
    """

    print("\n====================================")
    print(f"Validando {nombre_dimension}")
    print("====================================")

    # --------------------------------------
    # Tabla vacía
    # --------------------------------------

    if df.empty:

        raise ValueError(
            f"{nombre_dimension} está vacía."
        )

    # --------------------------------------
    # Columna clave
    # --------------------------------------

    if clave not in df.columns:

        raise ValueError(
            f"La columna '{clave}' no existe en {nombre_dimension}."
        )

    # --------------------------------------
    # Nulos
    # --------------------------------------

    nulos = df[clave].isna().sum()

    if nulos > 0:

        raise ValueError(
            f"{nombre_dimension} tiene {nulos} claves nulas."
        )

    # --------------------------------------
    # Duplicados
    # --------------------------------------

    duplicados = df[clave].duplicated().sum()

    if duplicados > 0:

        raise ValueError(
            f"{nombre_dimension} tiene {duplicados} claves duplicadas."
        )

    # --------------------------------------
    # Resumen
    # --------------------------------------

    print(f"Registros : {len(df):,}")
    print(f"Clave     : {clave}")
    print(f"Nulos     : {nulos}")
    print(f"Duplicados: {duplicados}")

    print("✓ OK")

    return True


def validar_fact(
    df,
    nombre_fact
):
    """
    ==========================================================
    Valida una tabla Fact.

    Verifica:

    • No esté vacía.
    • Tenga registros.

    La integridad referencial se valida
    posteriormente.
    ==========================================================
    """

    print("\n====================================")
    print(f"Validando {nombre_fact}")
    print("====================================")

    if df.empty:

        raise ValueError(
            f"{nombre_fact} está vacía."
        )

    print(f"Registros : {len(df):,}")

    print("✓ OK")

    return True


def validar_integridad(
    fact,
    dim,
    clave_fact,
    clave_dim,
    nombre_fact,
    nombre_dim
):
    """
    ==========================================================
    Valida integridad referencial.

    Todos los valores de la Fact deben existir
    en la Dimensión.
    ==========================================================
    """

    print("\n------------------------------------")
    print(
        f"{nombre_fact} -> {nombre_dim}"
    )

    faltantes = fact.loc[
        ~fact[clave_fact].isin(
            dim[clave_dim]
        )
    ]

    if len(faltantes) > 0:

        raise ValueError(

            f"{nombre_fact} tiene "

            f"{len(faltantes)} registros "

            f"sin correspondencia en "

            f"{nombre_dim}."

        )

    print("✓ Integridad correcta")

    return True


def validar_modelo_dimensional(
    dimensiones,
    facts
):
    """
    ==========================================================
    Ejecuta todas las validaciones
    del modelo dimensional.
    ==========================================================
    """

    print("\n======================================")
    print("VALIDANDO MODELO DIMENSIONAL")
    print("======================================")

    # ==========================
    # Dimensiones
    # ==========================

    validar_dimension(
        dimensiones["dim_producto"],
        "codigo",
        "dim_producto"
    )

    validar_dimension(
        dimensiones["dim_familia"],
        "id_familia",
        "dim_familia"
    )

    validar_dimension(
        dimensiones["dim_abcxyz"],
        "id_abcxyz",
        "dim_abcxyz"
    )

    validar_dimension(
        dimensiones["dim_estado"],
        "id_estado",
        "dim_estado"
    )

    validar_dimension(
        dimensiones["dim_zona"],
        "id_zona",
        "dim_zona"
    )

    validar_dimension(
        dimensiones["dim_picking"],
        "id_picking",
        "dim_picking"
    )

    validar_dimension(
        dimensiones["dim_ubicacion"],
        "id_ubicacion",
        "dim_ubicacion"
    )

    validar_dimension(
        dimensiones["dim_calendario"],
        "id_fecha",
        "dim_calendario"
    )

    # ==========================
    # Facts
    # ==========================

    for nombre, tabla in facts.items():

        validar_fact(
            tabla,
            nombre
        )

    print("\n======================================")
    print("MODELO VALIDADO CORRECTAMENTE")
    print("======================================")

    return True