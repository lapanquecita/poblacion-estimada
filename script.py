"""

Fuentes:

Poblacion por entidad:
https://www.datos.gob.mx/dataset/proyecciones-de-poblacion/resource/de522924-f4d8-4523-a6fd-6b2efe73f3af


Población por municipio:
https://www.gob.mx/cms/uploads/attachment/file/915066/BD_municipales_portada_regiones.pdf

Enlace directo:
https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/pry23/00_Pob_Mitad_1950_2070.csv

"""

import os
import pandas as pd


SEXO = ["Hombres", "Mujeres", "Total"]

GRUPOS_QUINQUENALES = [
    (0, 4),
    (5, 9),
    (10, 14),
    (15, 19),
    (20, 24),
    (25, 29),
    (30, 34),
    (35, 39),
    (40, 44),
    (45, 49),
    (50, 54),
    (55, 59),
    (60, 64),
    (65, 69),
    (70, 74),
    (75, 79),
    (80, 84),
    (85, 120),
]


def poblacion_general_entidad():
    """
    Genera archivos con la población de cada entidad
    desagregado por sexo y año.
    """

    # Creamos el directorio para la población general por entidad.
    os.makedirs("./poblacion_entidad", exist_ok=True)

    # Cargamos el dataset del CONAPO por entidad.
    df = pd.read_csv("./data/estatal.csv")

    # Iteramos por hombres, mujeres y total.
    for s in SEXO:
        # Para el archivo del total no haremos filtros por sexo.
        if s == "Total":
            temp_df = df.pivot_table(
                index="ENTIDAD",
                columns="AÑO",
                values="POBLACION",
                aggfunc="sum",
                fill_value=0,
            )
        else:
            # Para los archivos por sexo sí haremos un filtro.
            temp_df = df[df["SEXO"] == s].copy()
            temp_df = temp_df.pivot_table(
                index="ENTIDAD",
                columns="AÑO",
                values="POBLACION",
                aggfunc="sum",
                fill_value=0,
            )

        # Guardamos el archivo final.
        temp_df.to_csv(f"./poblacion_entidad/{s.lower()}.csv")


def poblacion_entidad_edad(a, b):
    """
    Genera archivos con la población de cada entidad
    desagregado por sexo y año, dentro del rango de edad especificado.

    Parameters
    ----------
    a : int
    El inicio del rango dedad.

    b : int
        eL FINAL DEL RANGO DE EDAD.

    """

    # Creamos el directorio usando el rango de edad.
    os.makedirs(f"./poblacion_entidad_{a}_{b}", exist_ok=True)

    # Cargamos el dataset del CONAPO por entidad.
    df = pd.read_csv("./data/estatal.csv")

    # Filtramos por le rango de edad.
    df = df[df["EDAD"].between(a, b)]

    # Iteramos por hombres, mujeres y total.
    for s in SEXO:
        # Para el archivo del total no haremos filtros por sexo.
        if s == "Total":
            temp_df = df.pivot_table(
                index="ENTIDAD",
                columns="AÑO",
                values="POBLACION",
                aggfunc="sum",
                fill_value=0,
            )
        else:
            # Para los archivos por sexo sí haremos un filtro.
            temp_df = df[df["SEXO"] == s].copy()
            temp_df = temp_df.pivot_table(
                index="ENTIDAD",
                columns="AÑO",
                values="POBLACION",
                aggfunc="sum",
                fill_value=0,
            )

        # Guardamos el archivo final usando los parámetros del rango de edad.
        temp_df.to_csv(f"./poblacion_entidad_{a}_{b}/{s.lower()}.csv")


def poblacion_adulta_entidad():
    """
    Genera archivos con la población de 18 años o más
    de cada entidad desagregado por sexo y año.
    """

    # Creamos el directorio para la población adulta por entidad.
    os.makedirs("./poblacion_adulta_entidad", exist_ok=True)

    # Cargamos el dataset del CONAPO por entidad.
    df = pd.read_csv("./data/estatal.csv")

    # Filtramos los registros para solo considerar la población de 18 años o más.
    df = df[df["EDAD"] >= 18]

    # Iteramos por hombres, mujeres y total.
    for s in SEXO:
        # Para el archivo del total no haremos filtros por sexo.
        if s == "Total":
            temp_df = df.pivot_table(
                index="ENTIDAD",
                columns="AÑO",
                values="POBLACION",
                aggfunc="sum",
                fill_value=0,
            )
        else:
            # Para los archivos por sexo sí haremos un filtro.
            temp_df = df[df["SEXO"] == s].copy()
            temp_df = temp_df.pivot_table(
                index="ENTIDAD",
                columns="AÑO",
                values="POBLACION",
                aggfunc="sum",
                fill_value=0,
            )

        # Guardamos el archivo final.
        temp_df.to_csv(f"./poblacion_adulta_entidad/{s.lower()}.csv")


def poblacion_edad_quinquenal():
    """
    Genera archivos con la población de México en grupos quinquenales.
    Desagregado por sexo y año.
    """

    # Creamos el directorio para la población por grupo de edad quinquenal a nivel nacional.
    os.makedirs("./poblacion_quinquenal_nacional", exist_ok=True)

    # Cargamos el dataset del CONAPO por entidad.
    df = pd.read_csv("./data/estatal.csv")

    # Iteramos por hombres, mujeres y total.
    for s in SEXO:
        # Para el archivo del total no haremos filtros por sexo.
        if s == "Total":
            temp_df = df.pivot_table(
                index="EDAD",
                columns="AÑO",
                values="POBLACION",
                aggfunc="sum",
                fill_value=0,
            )

            dfs = list()

            # Vamos a iterar sobre cada grupo de edad y sumar los totales.
            # Estos totales después serán convertidos a un nueov DataFrame.
            for a, b in GRUPOS_QUINQUENALES:
                sub_df = temp_df[(temp_df.index >= a) & (temp_df.index <= b)].sum(
                    axis=0
                )

                # Para el último grupo agregaremos el símbolo de igual o mayor que.
                sub_df.name = f"≥{a}" if a == 85 else f"{a}-{b}"
                dfs.append(sub_df)

        else:
            # Para los archivos por sexo sí haremos un filtro.
            temp_df = df[df["SEXO"] == s].copy()
            temp_df = temp_df.pivot_table(
                index="EDAD",
                columns="AÑO",
                values="POBLACION",
                aggfunc="sum",
                fill_value=0,
            )

            dfs = list()

            # Vamos a iterar sobre cada grupo de edad y sumar los totales.
            # Estos totales después serán convertidos a un nueov DataFrame.
            for a, b in GRUPOS_QUINQUENALES:
                sub_df = temp_df[(temp_df.index >= a) & (temp_df.index <= b)].sum(
                    axis=0
                )

                # Para el último grupo agregaremos el símbolo de igual o mayor que.
                sub_df.name = f"≥{a}" if a == 85 else f"{a}-{b}"
                dfs.append(sub_df)

        # Unimos las Series por edad en un solo DataFrame.
        final_df = pd.concat(dfs, axis=1).transpose()
        final_df.index.name = "GRUPO_EDAD"

        # Guardamos el archivo final.
        final_df.to_csv(f"./poblacion_quinquenal_nacional/{s.lower()}.csv")


def poblacion_general_municipal():
    # Creamos el directorio para la población general por municipio.
    os.makedirs("./poblacion_municipal", exist_ok=True)

    # Cargamos el dataset del CONAPO por municipio.
    df = pd.read_csv("./data/municipal_quinquenal.csv")

    # Convertimos la clave str y lo normlizamos a 5 dígitos.
    df["CLAVE"] = df["CLAVE"].astype(str).str.zfill(5)

    # Guardamos una referencia de los nombres de los municipios.
    nombres = df.groupby("CLAVE").last()[["NOM_ENT", "NOM_MUN"]]

    # Renombramos las columnas.
    nombres.columns = ["Entidad", "Municipio"]

    # Iteramos por hombres, mujeres y total.
    for s in SEXO:
        data = list()

        # Si la iteración corresponde a 'Total' no realizamos filtrado.
        if s != "Total":
            temp_df = df[df["SEXO"] == s.upper()]
        else:
            temp_df = df

        # Iteramos por municipio.
        for m in temp_df["CLAVE"].unique():
            # Filtramos por el municipio.
            sub_temp_df = temp_df[temp_df["CLAVE"] == m]

            # Agrupamos por año, sumamos y seleccionamos la población.
            sub_temp_df = sub_temp_df.groupby("AÑO").sum()["POB_TOTAL"]

            # Iteramos por cada año y agregamos un diccionario a nuestra lista de datos.
            for k, v in sub_temp_df.items():
                data.append(
                    {
                        "Año": k,
                        "Población": v,
                        "CVE": m,
                    }
                )
        # Creamos el DataFrame con todos los registros por municipio y año.
        municipios = pd.DataFrame.from_records(data)

        # Reorganizamos el DataFrame para que el índice sea la clave del municipio.
        # y las columnas sean los años.
        municipios = municipios.pivot_table(
            index="CVE", columns="Año", values="Población"
        )

        # Convertimos de floats a ints.
        municipios = municipios.astype(int)

        # Unimos ambos DataFrames.
        final = pd.concat([nombres, municipios], axis=1)

        # Renombramos el índice.
        final.index.name = "CVE"

        # Guardamos el archivo final.
        final.to_csv(f"./poblacion_municipal/{s.lower()}.csv")


if __name__ == "__main__":
    poblacion_general_entidad()
    poblacion_entidad_edad(18, 120)
    poblacion_adulta_entidad()
    poblacion_edad_quinquenal()

    poblacion_general_municipal()
