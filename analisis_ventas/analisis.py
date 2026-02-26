"""
Análisis de Ventas
------------------
Script para análisis mensual de ventas y rendimiento de productos.

Incluye:
- Limpieza básica de datos
- Validaciones
- Agregaciones
- Visualizaciones
- Exportación de resultados

Autor: César Luna
"""

import pandas as pd
import matplotlib.pyplot as plt
import logging
from pathlib import Path

""" Configuración básica de logging """

logging.basicConfig(level = logging.INFO, format = "%(levelname)s: %(message)s")

def cargar_datos(ruta_csv: str) -> pd.DataFrame:
    """ Carga y valida el archivo CSV """

    if not Path(ruta_csv).exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_csv}")

    df = pd.read_csv(ruta_csv)

    columnas_requeridas = {'fecha', 'producto', 'cantidad', 'precio'}
    if not columnas_requeridas.issubset(df.columns):
        raise ValueError(f"El CSV debe contener columnas: {columnas_requeridas}")
    
    logging.info("Archivo cargado correctamente")

    return df

def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """ Realiza la limpieza basica y conversión de datos para evitar errores de formato """

    df = df.copy()

    df['fecha'] = pd.to_datetime(df['fecha'],  errors = 'coerce')

    df = df.dropna(subset=['fecha'])

    df['cantidad'] = pd.to_numeric(df['cantidad'], errors = 'coerce')

    df['precio'] = pd.to_numeric(df['precio'], errors = 'coerce')

    logging.info("Datos correctamente validados")

    return df

def analizar_ventas(df: pd.DataFrame):
    """ Ahora si a realizar calculos """

    df['ingresos'] = df['cantidad'] * df['precio']

    """ Ventas por mes """

    df['mes'] = df['fecha'].dt.to_period('M')

    ventas_por_mes = (
        df.groupby('mes')['ingresos']
        .sum()
        .sort_index()
    )

    """ Ventas por producto """

    ventas_prod = (
        df.groupby('producto')
        .agg({
            'cantidad': 'sum',
            'ingresos': 'sum'
        })
    )

    return ventas_por_mes, ventas_prod

def mostrar_resultados(ventas_por_mes, ventas_prod):
    """ Ahora imprimimos los resultados de arriba """

    print("\nVentas por mes: ")
    print(ventas_por_mes)

    mas_vendido = ventas_prod['cantidad'].idxmax()
    mayor_ingreso = ventas_prod['ingresos'].idxmax()

    print(f"\nProducto mpas vendido en unidades: {mas_vendido}"
        f"(total {ventas_prod.loc[mas_vendido, 'cantidad']})")

    print(f"Producto con mayores ingresos: {mayor_ingreso}"
        f"(total {ventas_prod.loc[mayor_ingreso, 'ingresos']:.2f} $)")

def graficar_ventas(ventas_por_mes, ventas_prod):
    """ Ahora toca visualizar los resultados y guardarlos como un png """

    # Graficar por mes
    ventas_por_mes.index = ventas_por_mes.index.astype(str)

    plt.figure(figsize = (8, 5))
    ventas_por_mes.plot(kind = 'bar')
    plt.title("Ventas por Mes")
    plt.xlabel("Mes")
    plt.ylabel("Ventas ($)")
    plt.tight_layout()
    plt.savefig("ventas_por_mes.png")
    plt.close()

    # Graficar top 5 productos por ingresos
    top5 = ventas_prod.nlargest(5, 'ingresos')

    plt.figure(figsize=(8,5))
    plt.bar(top5.index, top5['ingresos'])
    plt.title("Top 5 Productos por Ingresos")
    plt.xlabel("Producto")
    plt.ylabel("Ingresos ($)")
    plt.xticks(rotation = 45)
    plt.tight_layout()
    plt.savefig("top5_productos.png")
    plt.close()

    logging.info("Graficos generados correctamente")

def main():
        """ Flujo principal del analisis """

        try:
            df = cargar_datos("ventas.csv")
            df = limpiar_datos(df)

            ventas_por_mes, ventas_prod = analizar_ventas(df)

            mostrar_resultados(ventas_por_mes, ventas_prod)
            graficar_ventas(ventas_por_mes, ventas_prod)

            logging.info("Analisis completado con exito")

        except Exception as e:
            logging.error(f"Ocurrió un error {e}")

if __name__ == "__main__":
    main()