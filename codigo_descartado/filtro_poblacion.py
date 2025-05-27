import pandas as pd
import json

excel_path = "datos_sin_procesar/apportionment-2020-table02.xlsx"
df = pd.read_excel(excel_path, sheet_name='Table 2')
data = df.iloc[3:, [0, 1]].dropna()
data.columns = ['state', 'population']
data = data[data['state'].apply(lambda x: isinstance(x, str))]
result = data.to_dict(orient='records')

with open("poblacion_estados.json", "w") as f:
    json.dump(result, f, indent=2)

print("Archivo JSON generado.")

