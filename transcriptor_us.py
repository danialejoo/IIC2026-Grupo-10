import json
from collections import Counter

with open("datos_sin_procesar/datos_tweets_global.json", "r", encoding="utf-8") as f:
    tweets = [json.loads(line) for line in f]

def es_de_estados_unidos(tweet):
    user_country = tweet.get("user_location", {}).get("country_code", "").lower()
    return user_country == "us"

tweets_us = [tweet for tweet in tweets if es_de_estados_unidos(tweet)]

def obtener_estado(tweet):
    return tweet.get("user_location", {}).get("state")

estados = [obtener_estado(tweet) for tweet in tweets_us if obtener_estado(tweet)]

conteo = Counter(estados)
total_us = sum(conteo.values())

resultado = [
    {
        "estado": estado,
        "cantidad": cantidad,
        "porcentaje": round((cantidad / total_us) * 100, 2)
    }
    for estado, cantidad in conteo.most_common()
]

with open("resumen_estados_us.json", "w", encoding="utf-8") as f_out:
    json.dump(resultado, f_out, ensure_ascii=False, indent=2)

print("✅ Archivo resumen_estados_us.json creado con éxito.")
