import os
import shutil
import re
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

    # --- Lógica de archivado de informes anteriores ---
    output_index_path = os.path.join(OUTPUT_DIR, 'index.html')
    current_month_str = datetime.now().strftime('%Y-%m')

    if os.path.exists(output_index_path):
        try:
            # Leer el contenido del index.html existente
            with open(output_index_path, 'r', encoding='utf-8') as f:
                existing_html_content = f.read()

            # Expresión regular para encontrar la fecha en el footer
            # Formato esperado: "Datos actualizados a fecha YYYY-MM-DD HH:MM TZ. Generado estáticamente."
            date_pattern = r"Datos actualizados a fecha (.*?)\. Generado estáticamente\."
            match = re.search(date_pattern, existing_html_content)

            old_report_month_str = None
            if match:
                date_str_from_footer = match.group(1).strip()
                try:
                    # Extraer la parte de fecha y hora, ignorando la abreviatura de zona horaria para el parseo
                    date_time_part = " ".join(date_str_from_footer.split(' ')[:2])
                    old_report_date = datetime.strptime(date_time_part, '%Y-%m-%d %H:%M')
                    old_report_month_str = old_report_date.strftime('%Y-%m')
                except ValueError:
                    print(f"Advertencia: No se pudo parsear la fecha '{date_str_from_footer}' del footer. Usando la fecha de modificación del archivo como fallback.")
                    # Fallback a la fecha de modificación si el parseo falla
                    mod_time = os.path.getmtime(output_index_path)
                    old_report_month_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m')
            else:
                print("Advertencia: No se encontró la fecha en el footer del index.html existente. Usando la fecha de modificación del archivo como fallback.")
                # Fallback a la fecha de modificación si el patrón no se encuentra
                mod_time = os.path.getmtime(output_index_path)
                old_report_month_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m')

            # Si el mes del informe es diferente al actual, lo archivamos
            if old_report_month_str != current_month_str:
                archive_name = f"{old_report_month_str}.html"
                archive_path = os.path.join(OUTPUT_DIR, archive_name)
                print(f"Archivando informe anterior como '{archive_name}'...")
                shutil.move(output_index_path, archive_path)

        except FileNotFoundError:
            # Esto solo pasaría si el archivo se elimina entre el 'exists' y el 'getmtime'
            pass
        except Exception as e:
            print(f"Error durante el procesamiento del archivo existente: {e}. Procediendo con la construcción normal.")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # --- Fin de la lógica de archivado ---

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

    # Buscar informes archivados para pasarlos a la plantilla
    archive_regex = re.compile(r'^\d{4}-\d{2}\.html$')
    archived_reports = sorted(
        [f for f in os.listdir(OUTPUT_DIR) if archive_regex.match(f)],
        reverse=True
    )

    # 3. Renderizar la plantilla con los datos
    # Usamos el filtro 'tojson' de Jinja para convertir el dict de Python en un objeto JSON seguro para HTML
    today_date = datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')
    html_content = template.render(
        title='Infografía Financiera',
        chart_data=all_data,
        today_date=today_date,
        archived_reports=archived_reports
    )

    # 4. Crear directorio de salida y guardar el HTML
    with open(output_index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # 5. Copiar archivos estáticos (JS, CSS, etc.)
    if os.path.exists(STATIC_SOURCE_DIR):
        shutil.copytree(STATIC_SOURCE_DIR, os.path.join(OUTPUT_DIR, 'static'), dirs_exist_ok=True)

    print(f"¡Sitio generado con éxito en la carpeta '{OUTPUT_DIR}'!")

if __name__ == '__main__':
    main()