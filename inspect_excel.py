import pandas as pd
from pathlib import Path
import sys

def main():
    if len(sys.argv) < 2:
        print("Uso: python inspect_excel.py RUTA_ARCHIVO.xlsx")
        return

    p = Path(sys.argv[1])
    if not p.exists():
        print(f"Archivo no encontrado: {p}")
        return

    xl = pd.ExcelFile(p)
    print("Hojas encontradas:", xl.sheet_names)

    sheet = xl.sheet_names[0]
    print(f"Usando hoja: {sheet}\n")

    # Mostrar primeras filas sin encabezado para ver offset
    df_none = pd.read_excel(p, sheet_name=sheet, header=None, nrows=10)
    print("Primeras 10 filas (header=None):")
    print(df_none.to_string(index=False))
    print('\n---\n')

    # Leer con encabezado por defecto
    df = pd.read_excel(p, sheet_name=sheet)
    print("Columnas detectadas:")
    print(list(df.columns))
    print('\nColumnas (repr):')
    print([repr(c) for c in df.columns])
    print('\nCódigos Unicode por columna:')
    for c in df.columns:
        s = str(c)
        codes = ' '.join(f"U+{ord(ch):04X}" for ch in s)
        print(f"{repr(c)} -> {codes}")

if __name__ == '__main__':
    main()
