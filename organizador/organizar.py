"""
File Organizer Automation Script
--------------------------------
Organiza archivos automáticamente por categoría según su extensión.

Incluye:
- Mapeo dinámico de extensiones
- Manejo de errores
- Logging estructurado
- Modo simulación (dry-run)

Autor: César Luna
"""

import logging

from pathlib import Path 

from typing import Dict

# -----------------------------
# Configuración de logging
# -----------------------------

logging.basicConfig(
    level = logging.INFO,
    format="%(levelname)s - %(message)s"
)

# -----------------------------
# Configuración de categorías
# -----------------------------

CATEGORIAS: Dict[str, list] = {

    "Imagenes": [".png", ".jpg", ".jpeg", ".gif"],
    "Documentos": [".pdf", ".docx", ".txt", ".xlsx"],
    "Videos": [".mp4", ".avi", ".mkv"],
    "Musica": [".mp3", ".wav"]
}

CATEGORIA_DEFAULT = "Otros"

# -----------------------------
# Funciones principales
# -----------------------------

def construir_mapa_extensiones(categorias: Dict[str, list]) -> Dict[str, str]:
    """
    Construye un diccionario que relaciona extensión -> categoría.
    """

    extension_map = {}

    for categoria, extensiones in categorias.items():
        for ext in extensiones:
            extension_map[ext.lower()] = categoria 

    return extension_map

def obtener_archivos(carpeta: Path):
    """
    Obtiene todos los archivos regulares de la carpeta.
    Excluye archivos ocultos del sistema.
    """

    return [
        f for f in carpeta.iterdir()
        if f.is_file() and not f.name.startswith("NTUSER")
    ]

def organizar_archivos(carpeta: Path, extension_map: Dict[str, str], dry_run: bool = False):
    """
    Organiza los archivos según su extensión.
    
    Parámetros:
    - carpeta: Ruta objetivo
    - extension_map: Diccionario extensión -> categoría
    - dry_run: Si es True, solo simula movimientos
    """

    archivos = obtener_archivos(carpeta)

    for archivo in archivos:
        try:
            ext = archivo.suffix.lower()
            categoria = extension_map.get(ext, CATEGORIA_DEFAULT)

            destino_dir = carpeta / categoria
            destino_path = destino_dir / archivo.name

            if dry_run:
                logging.info(f"[SIMULACION] {archivo.name} → {categoria}/")
                continue

            destino_dir.mkdir(exist_ok=True)
            archivo.rename(destino_path)
        
        except PermissionError:
            logging.warning(f"No se pudo mover {archivo.name} dado que es un archivo en uso o protegido")

        except Exception as e:
            logging.error(f"Error moviendo {archivo.name}: {e}")

# -----------------------------
# Punto de entrada
# -----------------------------

def main():
    """
    Flujo principal del programa.
    """

    carpeta_objetivo = Path (r"C:\Users\arkan\OneDrive\Escritorio\Labo\Python")
    # carpeta_objetivo = Path.home() / "Downloads"  # modificar ruta a su gusto

    if not carpeta_objetivo.exists():
        logging.error("La carpeta elegida no existe")
        return
    
    extension_map = construir_mapa_extensiones(CATEGORIAS)

    logging.info("Iniciando organización de archivos...")

    organizar_archivos(carpeta_objetivo, extension_map, dry_run=False)

    logging.info("Proceso finalizado")


if __name__ == "__main__":
    main()