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

dic_state_names = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
    "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
    "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
    "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
    "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
    "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont",
    "VA": "Virginia", "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming",
    "DC": "District of Columbia"
}

dic_acumulado = {}

for i, fecha in enumerate(fechas_deseadas):
    if i == 0:
        fecha_anterior = columnas_fecha[indice_inicio - 1]
    else:
        fecha_anterior = fechas_deseadas[i - 1]

    casos_hoy = df.groupby("State")[fecha].sum()
    casos_ayer = df.groupby("State")[fecha_anterior].sum()
    casos_dia = (casos_hoy - casos_ayer).clip(lower=0)

    for estado, cnt in casos_dia.items():
        dic_acumulado[estado] = dic_acumulado.get(estado, 0) + int(cnt)

    lista_estado_casos = [
        {"estado": estado, "cantidad": int(cnt)}
        for estado, cnt in casos_dia.items()
    ]
    total_dia = int(casos_dia.sum())
    sorted_acum = sorted(dic_acumulado.items(), key=lambda x: x[1], reverse=True)
    top5_acumulado = [
        {"estado": dic_state_names.get(est, est), "total": total}
        for est, total in sorted_acum[:5]
    ]
    estructura_json = {
        "estados": lista_estado_casos,
        "total_nacional": total_dia,
        "top5": top5_acumulado
    }
    ruta = os.path.join("datos_limpios", f"{fecha}.json")
    with open(ruta, "w") as f:
        json.dump(estructura_json, f, indent=2)