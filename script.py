"""

Fuente:
https://datos.gob.mx/busca/dataset/proyecciones-de-la-poblacion-de-mexico-y-de-las-entidades-federativas-2020-2070

Enlace directo:
https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/pry23/00_Pob_Mitad_1950_2070.csv

"""


import os
import pandas as pd


SEXO = ["Hombres", "Mujeres", "Total"]

QUINQUENALES = [
    (0, 4), (5, 9), (10, 14), (15, 19),
    (20, 24), (25, 29), (30, 34), (35, 39),
    (40, 44), (45, 49), (50, 54), (55, 59),
    (60, 64), (65, 69), (70, 74), (75, 79),
    (80, 84), (85, 89), (90, 94), (95, 99),
    (100, 120),
]


def poblacion_general_entidad():

    # Creamos el directorio para la población general por entidad.
    os.makedirs("./poblacion_entidad", exist_ok=True)

    # Cargamos el dataset del CONAPO.
    df = pd.read_csv("./CONAPO.csv")

    # Filtramos los registros para solo tomar de 1970 en adelante.
    # Las estimaciones estatales comienzan a partir de ese año.
    df = df[df["AÑO"] >= 1970]

    # Iteramos por hombres, mujeres y total.
    for s in SEXO:

        data = list()

        # Si la iteración corresponde a 'Total' no realizamos filtrado.
        if s != "Total":
            temp_df = df[df["SEXO"] == s]
        else:
            temp_df = df

        # Iteramos por entidad federativa.
        for e in temp_df["ENTIDAD"].unique():

            # Filtramos por la entidad federativa.
            sub_temp_df = temp_df[temp_df["ENTIDAD"] == e]

            # Agrupamos por año, sumamos y seleccionamos la población.
            sub_temp_df = sub_temp_df.groupby("AÑO").sum()["POBLACION"]

            # Iteramos por cada año y agregamos un diccionario a nuestra lista de datos.
            # En el caso de los registros de la República Mexicana los renombramos a '0'
            # para que salga primero en la lista.
            for k, v in sub_temp_df.items():
                data.append({
                    "Año": k,
                    "Población": v,
                    "Entidad": "0" if e == "República Mexicana" else e,
                })
        # Creamos el DataFrame con todos los registros por entidad y año.
        final = pd.DataFrame.from_records(data)

        # Reorganizamos el DataFrame para que el índice sea la entidad
        # y las columnas sean los años.
        final = final.pivot_table(
            index="Entidad", columns="Año", values="Población")

        # Renombarmos de nuevo la República Mexicana.
        final.index = final.index.str.replace("0", "Estados Unidos Mexicanos")

        # Convertimos de floats a ints.
        final = final.astype(int)

        # Guardamos el archivo final.
        final.to_csv(f"./poblacion_entidad/{s.lower()}.csv")


def poblacion_adulta_entidad():

    # Creamos el directorio para la población adulta por entidad.
    os.makedirs("./poblacion_adulta_entidad", exist_ok=True)

    # Cargamos el dataset del CONAPO.
    df = pd.read_csv("./CONAPO.csv")

    # Filtramos los registros para solo considerar la población de 18 años o más.
    df = df[df["EDAD"] >= 18]

    # Filtramos los registros para solo tomar de 1970 en adelante.
    # Las estimaciones estatales comienzan a partir de ese año.
    df = df[df["AÑO"] >= 1970]

    # Iteramos por hombres, mujeres y total.
    for s in SEXO:

        data = list()

        # Si la iteración corresponde a 'Total' no realizamos filtrado.
        if s != "Total":
            temp_df = df[df["SEXO"] == s]
        else:
            temp_df = df

        # Iteramos por entidad federativa.
        for e in temp_df["ENTIDAD"].unique():

            # Filtramos por la entidad federativa.
            sub_temp_df = temp_df[temp_df["ENTIDAD"] == e]

            # Agrupamos por año, sumamos y seleccionamos la población.
            sub_temp_df = sub_temp_df.groupby("AÑO").sum()["POBLACION"]

            # Iteramos por cada año y agregamos un diccionario a nuestra lista de datos.
            # En el caso de los registros de la República Mexicana los renombramos a '0'
            # para que salga primero en la lista.
            for k, v in sub_temp_df.items():
                data.append({
                    "Año": k,
                    "Población": v,
                    "Entidad": "0" if e == "República Mexicana" else e,
                })
        # Creamos el DataFrame con todos los registros por entidad y año.
        final = pd.DataFrame.from_records(data)

        # Reorganizamos el DataFrame para que el índice sea la entidad
        # y las columnas sean los años.
        final = final.pivot_table(
            index="Entidad", columns="Año", values="Población")

        # Renombarmos de nuevo la República Mexicana.
        final.index = final.index.str.replace("0", "Estados Unidos Mexicanos")

        # Convertimos de floats a ints.
        final = final.astype(int)

        # Guardamos el archivo final.
        final.to_csv(f"./poblacion_adulta_entidad/{s.lower()}.csv")


def poblacion_por_edad():

    # Creamos el directorio para la población por edad a nivel nacional.
    os.makedirs("./poblacion_edad", exist_ok=True)

    # Cargamos el dataset del CONAPO.
    df = pd.read_csv("./CONAPO.csv")

    # Seleccionamos solo los datos de la República Mexicana.
    df = df[df["ENTIDAD"] == "República Mexicana"]

    # Iteramos por hombres, mujeres y total.
    for s in SEXO:

        # Si la iteración corresponde a 'Total' no realizamos filtrado.
        if s != "Total":
            temp_df = df[df["SEXO"] == s]
        else:
            temp_df = df

        # Reorganizamos el DataFrame para que el índice sea la edad
        # y las columnas sean los años.
        temp_df = temp_df.pivot_table(
            index="EDAD", columns="AÑO", values="POBLACION", aggfunc="sum")

        # Renombramos el índice.
        temp_df.index.name = "Edad"

        # Guardamos el archivo final.
        temp_df.to_csv(f"./poblacion_edad/{s.lower()}.csv")


def poblacion_edad_quinquenal():

    # Creamos el directorio para la población por grupo de edad quinquenal a nivel nacional.
    os.makedirs("./poblacion_quinquenal", exist_ok=True)

    # Cargamos el dataset del CONAPO.
    df = pd.read_csv("./CONAPO.csv")

    # Seleccionamos solo los datos de la República Mexicana.
    df = df[df["ENTIDAD"] == "República Mexicana"]

    # Iteramos por hombres, mujeres y total.
    for s in SEXO:

        data = list()

        # Si la iteración corresponde a 'Total' no realizamos filtrado.
        if s != "Total":
            temp_df = df[df["SEXO"] == s]
        else:
            temp_df = df

        # Iteramos sobre los grupos quinquenales.
        for i, (a, b) in enumerate(QUINQUENALES):

            # Filtramos por grupo quinquenal, las edades que se encuentre
            # entre 'a' y 'b' de forma inclusiva.
            sub_temp_df = temp_df[temp_df["EDAD"].between(a, b)]

            # Agrupamos por año, sumamos y seleccionamos la población.
            sub_temp_df = sub_temp_df.groupby("AÑO").sum()["POBLACION"]

            # Iteramos por cada año y agregamos un diccionario a nuestra lista de datos.
            for k, v in sub_temp_df.items():
                data.append({
                    "Año": k,
                    "Población": v,
                    "Edad": i,
                })

        # Creamos el DataFrame con todos los registros por edad y año.
        final = pd.DataFrame.from_records(data)

        # Reorganizamos el DataFrame para que el índice sea el grupo de edad
        # y las columnas sean los años.
        final = final.pivot_table(
            index="Edad", columns="Año", values="Población")

        # Ajustamos el índice para que indique los rangos de edad de cada grupo.
        final.index = final.index.map(
            lambda x: f"{QUINQUENALES[x][0]}-{QUINQUENALES[x][1]}")

        # Renombramos el grupo de 100-120 a 100 y más.
        final.index = final.index.str.replace("100-120", "≥100")

        # Convertimos de floats a ints.
        final = final.astype(int)

        # Renombramos el índice.
        final.index.name = "Grupo edad"

        # Guardamos el archivo final.
        final.to_csv(f"./poblacion_quinquenal/{s.lower()}.csv")


if __name__ == "__main__":

    poblacion_general_entidad()
    poblacion_adulta_entidad()
    poblacion_por_edad()
    poblacion_edad_quinquenal()
