import pandas as pd
import json
import os

os.makedirs("datos_limpios", exist_ok=True)
df = pd.read_csv("datos_sin_procesar/covid_confirmed_usafacts.csv")
columnas_fecha = sorted(df.columns[4:])
inicio = "2022-01-01"
fin = "2022-03-01"
fechas_deseadas = [f for f in columnas_fecha if inicio <= f <= fin]
indice_inicio = columnas_fecha.index(inicio)

for i, fecha in enumerate(fechas_deseadas):
    if i == 0:
        fecha_anterior = columnas_fecha[indice_inicio - 1]
    else:
        fecha_anterior = fechas_deseadas[i - 1]

    casos_hoy = df.groupby("State")[fecha].sum()
    casos_ayer = df.groupby("State")[fecha_anterior].sum()
    casos_dia = (casos_hoy - casos_ayer).clip(lower=0)

    lista_estado_casos = [
        {"estado": estado, "cantidad": int(casos)}
        for estado, casos in casos_dia.items()
    ]
    total_nacional = int(casos_dia.sum())
    estructura_json = {
        "estados": lista_estado_casos,
        "total_nacional": total_nacional
    }
    ruta = os.path.join("datos_limpios", f"{fecha}.json")
    with open(ruta, "w") as f:
        json.dump(estructura_json, f, indent=2)

    print(f"✅ {fecha}.json generado con total nacional: {total_nacional}")
