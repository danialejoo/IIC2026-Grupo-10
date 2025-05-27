import pandas as pd
import argparse

def convertir_csv_a_json(archivo_csv, archivo_salida="salida.json"):
    df = pd.read_csv(archivo_csv)
    df.to_json(archivo_salida, orient="records", force_ascii=False, lines=True)
    print(f"Archivo JSON generado: {archivo_salida}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convierte un archivo CSV a JSON.")
    parser.add_argument("csv", help="Ruta del archivo CSV de entrada.")
    parser.add_argument("--salida", help="Ruta del archivo JSON de salida.", default="salida.json")

    args = parser.parse_args()
    convertir_csv_a_json(args.csv, args.salida)
    
# python3 traductor.py 'idioma'_test.csv --salida 'idioma'.json