import pandas as pd
import os
import json

df = pd.read_csv("datos_sin_procesar/covid_confirmed_usafacts.csv")
output_dir = "covid_by_date_json"
os.makedirs(output_dir, exist_ok=True)
date_columns = df.columns[4:]
state_totals = df.groupby("State")[date_columns].sum()

for date in date_columns:
    day_series = state_totals[date]
    total_nacional = day_series.sum()
    json_list = []
    for estado, cantidad in day_series.items():
        porcentaje = round((cantidad / total_nacional) * 100, 2) if total_nacional > 0 else 0.0
        json_list.append({
            "estado": estado,
            "cantidad": int(cantidad),
            "porcentaje": porcentaje
        })
    filename = os.path.join(output_dir, f"{date.replace('/', '-')}.json")
    with open(filename, "w") as f:
        json.dump(json_list, f, indent=2)