import pandas as pd
import json
import os

# Crear carpeta de salida
os.makedirs("datos_limpios", exist_ok=True)

# Leer CSV original
df = pd.read_csv("datos_sin_procesar/covid_confirmed_usafacts.csv")
# Fechas disponibles en columnas (a partir de la 5ª)
columnas_fecha = sorted(df.columns[4:])
# Rango deseado
inicio = "2022-01-01"
fin = "2022-03-01"
fechas_deseadas = [f for f in columnas_fecha if inicio <= f <= fin]
indice_inicio = columnas_fecha.index(inicio)

# Mapeo de siglas a nombres completos de estados
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

# Diccionario para acumulado por estado
dic_acumulado = {}

for i, fecha in enumerate(fechas_deseadas):
    # Determinar fecha anterior
    if i == 0:
        fecha_anterior = columnas_fecha[indice_inicio - 1]
    else:
        fecha_anterior = fechas_deseadas[i - 1]

    # Calcular casos diarios hoy vs ayer por estado
    casos_hoy = df.groupby("State")[fecha].sum()
    casos_ayer = df.groupby("State")[fecha_anterior].sum()
    casos_dia = (casos_hoy - casos_ayer).clip(lower=0)

    # Actualizar acumulado total por estado
    for estado, cnt in casos_dia.items():
        dic_acumulado[estado] = dic_acumulado.get(estado, 0) + int(cnt)

    # Lista de diccionarios estado-casos diarios (siglas)
    lista_estado_casos = [
        {"estado": estado, "cantidad": int(cnt)}
        for estado, cnt in casos_dia.items()
    ]
    total_dia = int(casos_dia.sum())

    # Generar Top 5 acumulado con nombres completos
    sorted_acum = sorted(dic_acumulado.items(), key=lambda x: x[1], reverse=True)
    top5_acumulado = [
        {"estado": dic_state_names.get(est, est), "total": total}
        for est, total in sorted_acum[:5]
    ]

    # Estructura JSON final
    estructura_json = {
        "estados": lista_estado_casos,
        "total_nacional": total_dia,
        "top5": top5_acumulado
    }
    ruta = os.path.join("datos_limpios", f"{fecha}.json")
    with open(ruta, "w") as f:
        json.dump(estructura_json, f, indent=2)

    print(f"✅ {fecha}.json generado con total nacional {total_dia} y Top 5 acumulado incluidos.")
