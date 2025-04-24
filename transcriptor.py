import json
from collections import Counter

with open("datos_sin_procesar/datos_tweets_global.json", "r", encoding="utf-8") as f:
    tweets = [json.loads(line) for line in f]

def obtener_pais(tweet):
    if tweet.get("user_location", {}).get("country_code"):
        return tweet["user_location"]["country_code"].lower()
    elif tweet.get("tweet_locations"):
        return tweet["tweet_locations"][0].get("country_code", "").lower()
    return None

paises = [obtener_pais(tweet) for tweet in tweets if obtener_pais(tweet)]
conteo = Counter(paises)

resultado = [
    {"pais": pais, "cantidad": cantidad}
    for pais, cantidad in conteo.most_common()
]

with open("resumen_por_pais.json", "w", encoding="utf-8") as f_out:
    json.dump(resultado, f_out, ensure_ascii=False, indent=2)
print("✅ Archivo resumen_por_pais.json creado con éxito.")
