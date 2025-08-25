import json
import os
import shutil
import random
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader

# --- Configuración ---
TEMPLATE_DIR = 'templates'
OUTPUT_DIR = 'dist'
STATIC_SOURCE_DIR = 'static'

# --- Funciones de Obtención de Datos (PLACEHOLDERS) ---
# NOTA: Aquí es donde integrarás tus funciones reales que obtienen los datos.

def generate_time_series_data(points=50, start_val=100, volatility=2):
    """Genera datos de series temporales de ejemplo."""
    labels = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(points)][::-1]
    data = []
    current_val = start_val
    for _ in range(points):
        current_val += random.uniform(-volatility, volatility)
        data.append(round(current_val, 2))
    return {"labels": labels, "data": data}

def get_m2_liquidity_data():
    """Placeholder para obtener datos de liquidez M2."""
    return generate_time_series_data(points=100, start_val=20000, volatility=50)

def get_treasury_spread_data():
    """Placeholder para obtener datos del spread 10Y-3M."""
    return generate_time_series_data(points=100, start_val=1.5, volatility=0.1)

def get_fed_funds_vs_10y_data():
    """Placeholder para obtener datos de Fed Funds vs 10-year Treasury."""
    labels = [(datetime.now() - timedelta(days=i*30)).strftime('%b %Y') for i in range(24)][::-1]
    fed_funds = [round(5.25 + random.uniform(-0.5, 0.5), 2) for _ in labels]
    ten_year = [round(4.5 + random.uniform(-0.8, 0.8), 2) for _ in labels]
    return {"labels": labels, "fed_funds": fed_funds, "ten_year": ten_year}

def get_hyg_price_data():
    """Placeholder para obtener el precio del stock HYG."""
    return generate_time_series_data(points=100, start_val=75, volatility=0.5)

# --- Lógica Principal del Script de Construcción ---

def main():
    print("Iniciando la construcción del sitio estático...")

    # 1. Recopilar todos los datos
    all_data = {
        "m2_liquidity": get_m2_liquidity_data(),
        "treasury_spread": get_treasury_spread_data(),
        "fed_funds_vs_10y": get_fed_funds_vs_10y_data(),
        "hyg_price": get_hyg_price_data()
    }

    # 2. Configurar Jinja
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('index.html')

    # 3. Renderizar la plantilla con los datos
    # Usamos el filtro 'tojson' de Jinja para convertir el dict de Python en un objeto JSON seguro para HTML
    html_content = template.render(title='Infografía Financiera', chart_data=all_data)

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