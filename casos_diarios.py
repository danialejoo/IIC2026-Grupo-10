import pandas as pd
import json
import os

os.makedirs("datos_limpios", exist_ok=True)
df = pd.read_csv("datos_sin_procesar/covid_confirmed_usafacts.csv")
columnas_fecha = df.columns[4:]
fechas_ordenadas = sorted(columnas_fecha)
inicio = "2022-01-01"
fin = "2022-03-01"

fechas_deseadas = [
    fecha for fecha in fechas_ordenadas
    if inicio <= fecha <= fin
]
indice_inicio = fechas_ordenadas.index(inicio)

for i, fecha in enumerate(fechas_deseadas):
    if i == 0:
        fecha_anterior = fechas_ordenadas[indice_inicio - 1]
    else:
        fecha_anterior = fechas_deseadas[i - 1]

    casos_hoy = df.groupby("State")[fecha].sum()
    casos_ayer = df.groupby("State")[fecha_anterior].sum()
    casos_dia = (casos_hoy - casos_ayer).clip(lower=0)
    lista_estado_casos = [
        {"estado": estado, "cantidad": int(casos)}
        for estado, casos in casos_dia.items()
    ]
    ruta = os.path.join("datos_limpios", f"{fecha}.json")

    with open(ruta, "w") as f:
        json.dump(lista_estado_casos, f, indent=2)
    print(f"✅ Generado: {ruta}")