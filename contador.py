import pandas as pd
import json

archivos_idiomas = [
    ("Espanol.json", "Español"),
    ("Frances.json", "Francés"),
    ("Arabe.json", "Árabe"),
    ('Aleman.json', 'Alemán'),
    ('Ingles.json', 'Inglés'),
    ('Portugues.json', 'Portugues'),
    ('Rurdu.json', 'Rurdu'),
    ('Ruso.json', 'Ruso'),
    ('Chino.json', 'Chino')
]

estadisticas_temp = {}

for archivo, idioma in archivos_idiomas:
    df = pd.read_json(archivo, lines=True)

    total = len(df)
    total_odio = len(df[df["label"] == 1.0])
    porcentaje = (total_odio / total) * 100 if total > 0 else 0

    estadisticas_temp[idioma] = {
        "total_frases": total,
        "frases_odio": total_odio,
        "porcentaje_odio": round(porcentaje, 1)
    }

estadisticas_ordenadas = dict(sorted(
    estadisticas_temp.items(),
    key=lambda item: item[1]["porcentaje_odio"],
    reverse=True
))

print(json.dumps(estadisticas_ordenadas, indent=2, ensure_ascii=False))

with open("estadisticas_discursos_odio_por_idioma.json", "w", encoding="utf-8") as f:
    json.dump(estadisticas_ordenadas, f, ensure_ascii=False, indent=2)