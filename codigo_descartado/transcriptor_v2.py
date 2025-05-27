import json
import pycountry

# Paso 1: Cargar archivo resumen_por_pais.json
with open("resumen_por_pais.json", "r", encoding="utf-8") as f:
    datos = json.load(f)

# Paso 2: Calcular total de tweets
total = sum(item["cantidad"] for item in datos)

# Paso 3: Función para obtener el nombre del país desde el código
def nombre_pais(codigo):
    try:
        return pycountry.countries.get(alpha_2=codigo.upper()).name
    except:
        return codigo.upper()

# Paso 4: Agregar porcentaje y nombre de país
resultado = []
for item in datos:
    codigo = item["pais"].lower()
    cantidad = item["cantidad"]
    resultado.append({
        "pais": nombre_pais(codigo),
        "codigo": codigo.upper(),
        "cantidad": cantidad,
        "porcentaje": round((cantidad / total) * 100, 2)
    })

# Paso 5: Guardar en nuevo archivo
with open("resumen_por_pais_con_porcentaje.json", "w", encoding="utf-8") as f_out:
    json.dump(resultado, f_out, ensure_ascii=False, indent=2)

print("✅ Archivo resumen_por_pais_con_porcentaje.json creado con éxito.")

