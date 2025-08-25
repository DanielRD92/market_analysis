import random
from datetime import datetime, timedelta

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

def get_all_data():
    """Recopila y devuelve todos los datos de los indicadores en un único diccionario."""
    return {
        "m2_liquidity": get_m2_liquidity_data(),
        "treasury_spread": get_treasury_spread_data(),
        "fed_funds_vs_10y": get_fed_funds_vs_10y_data(),
        "hyg_price": get_hyg_price_data()
    }