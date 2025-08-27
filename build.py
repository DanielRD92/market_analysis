import os
import shutil
from datetime import datetime

from jinja2 import Environment, FileSystemLoader
from data import get_all_data

# --- Configuración ---
TEMPLATE_DIR = 'templates'
OUTPUT_DIR = 'dist'
STATIC_SOURCE_DIR = 'static'

# --- Lógica Principal del Script de Construcción ---

def main():
    print("Iniciando la construcción del sitio estático...")

    try:
        # 1. Recopilar todos los datos
        all_data = get_all_data()
    except Exception as e:
        print(f"\nERROR: No se pudieron obtener los datos. {e}")
        print("Abortando la construcción del sitio.")
        return # Salir del script si los datos fallan

    # 2. Configurar Jinja
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('index.html')

    # 3. Renderizar la plantilla con los datos
    # Usamos el filtro 'tojson' de Jinja para convertir el dict de Python en un objeto JSON seguro para HTML
    today_date = datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')
    html_content = template.render(title='Infografía Financiera', chart_data=all_data, today_date=today_date)

    # 4. Crear directorio de salida y guardar el HTML
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

    # 5. Copiar archivos estáticos (JS, CSS, etc.)
    if os.path.exists(STATIC_SOURCE_DIR):
        shutil.copytree(STATIC_SOURCE_DIR, os.path.join(OUTPUT_DIR, 'static'), dirs_exist_ok=True)

    print(f"¡Sitio generado con éxito en la carpeta '{OUTPUT_DIR}'!")

if __name__ == '__main__':
    main()