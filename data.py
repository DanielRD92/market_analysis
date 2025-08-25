import os
import pandas as pd
from datetime import datetime, timedelta
from fredapi import Fred
from configurations import FRED_SERIES_IDS, DATA_YEARS_RANGE

# --- Cálculo de Fechas ---
# Se calcula la fecha de inicio restando los años definidos en la configuración.
end_date = datetime.now()
start_date = (end_date - timedelta(days=365 * DATA_YEARS_RANGE)).strftime('%Y-%m-%d')

# --- Configuración del Cliente FRED ---
# La clave se obtiene de una variable de entorno, ideal para GitHub Actions Secrets.
FRED_API_KEY = os.getenv('FRED_API_KEY')

if not FRED_API_KEY:
    # Si la clave no está, no podemos continuar. El script fallará.
    fred = None
    print("Error de configuración: La variable de entorno FRED_API_KEY no está definida.")
    print("Asegúrate de configurar el secret en tu repositorio de GitHub.")
else:
    fred = Fred(api_key=FRED_API_KEY)

# --- Funciones de Ayuda ---
def format_series_for_chartjs(series: pd.Series):
    """Limpia y formatea una serie de Pandas para Chart.js después de haber sido filtrada por fecha."""
    series = series.dropna()
    return {
        "labels": series.index.strftime('%Y-%m-%d').tolist(),
        "data": series.round(2).tolist()
    }

# --- Funciones de Obtención de Datos ---

def get_kpi_data():
    """Obtiene los datos para los KPIs principales usando datos reales de FRED."""
    print("Obteniendo datos de KPIs...")

    # 1. Crecimiento del PIB (último dato trimestral)
    gdp_series = fred.get_series_latest_release(FRED_SERIES_IDS["GDP_GROWTH"])
    gdp_value = gdp_series.iloc[-1]
    gdp_date = gdp_series.index[-1]
    gdp_data = {
        "value": f"{gdp_value:.1f}%",
        "note": f"Crecimiento trimestral Q{gdp_date.quarter} {gdp_date.year}."
    }

    # 2. Tasa de Inflación (último dato interanual)
    inflation_series = fred.get_series_latest_release(FRED_SERIES_IDS["INFLATION_RATE"])
    inflation_value = inflation_series.iloc[-1]
    inflation_date = inflation_series.index[-1]
    inflation_data = {
        "value": f"{inflation_value:.1f}%",
        "note": f"Variación interanual (PCE) Q{inflation_date.quarter} {inflation_date.year}."
    }

    # 3. Tasa de Interés de Referencia (Fed Funds Rate)
    interest_rate_series = fred.get_series_latest_release(FRED_SERIES_IDS["FED_FUNDS"])
    interest_rate_value = interest_rate_series.iloc[-1]
    interest_rate_date = interest_rate_series.index[-1]
    interest_rate_data = {
        "value": f"{interest_rate_value:.2f}%",
        "note": f"Tasa efectiva de Fondos Federales (Fed Funds) Q{interest_rate_date.quarter} {interest_rate_date.year}."
    }

    return {
        "gdp_growth": gdp_data,
        "inflation_rate": inflation_data,
        "interest_rate": interest_rate_data
    }

def get_m2_liquidity_data():
    """Obtiene el agregado monetario M2."""
    print(f"Obteniendo datos de M2 desde {start_date}...")
    m2 = fred.get_series(FRED_SERIES_IDS["M2_SUPPLY"], observation_start=start_date)
    return format_series_for_chartjs(m2)

def get_treasury_spread_data():
    """Calcula el spread entre el bono del tesoro a 10 años y 3 meses."""
    print(f"Obteniendo datos del Spread del Tesoro desde {start_date}...")
    ten_year = fred.get_series(FRED_SERIES_IDS["TEN_YEAR_TREASURY"], observation_start=start_date)
    three_month = fred.get_series(FRED_SERIES_IDS["THREE_MONTH_TREASURY"], observation_start=start_date)
    spread = (ten_year - three_month)
    return format_series_for_chartjs(spread)

def get_fed_funds_vs_10y_data():
    """Obtiene la tasa de fondos federales y el rendimiento del bono a 10 años."""
    print(f"Obteniendo datos de Fed Funds vs 10-Year desde {start_date}...")
    fed_funds = fred.get_series(FRED_SERIES_IDS["FED_FUNDS"], observation_start=start_date).dropna()
    ten_year = fred.get_series(FRED_SERIES_IDS["TEN_YEAR_TREASURY"], observation_start=start_date).dropna()
    
    # Alinear datos a una frecuencia mensual para la comparación
    df = pd.concat([fed_funds.resample('MS').mean(), ten_year.resample('MS').mean()], axis=1).dropna()
    df.columns = ['fed_funds', 'ten_year']
    
    return {
        "labels": df.index.strftime('%Y-%m-%d').tolist(),
        "fed_funds": df['fed_funds'].round(2).tolist(),
        "ten_year": df['ten_year'].round(2).tolist()
    }

def get_high_yield_index_data():
    """Obtiene el rendimiento del índice de bonos de alto riesgo."""
    print(f"Obteniendo datos del Índice High-Yield desde {start_date}...")
    # ICE BofA US High Yield Index Effective Yield
    high_yield = fred.get_series(FRED_SERIES_IDS["HIGH_YIELD_INDEX"], observation_start=start_date)
    return format_series_for_chartjs(high_yield)

def get_all_data():
    """Recopila y devuelve todos los datos de los indicadores en un único diccionario."""
    if not fred:
        raise Exception("El cliente de FRED no está inicializado. Revisa la variable de entorno FRED_API_KEY.")
    return {
        "kpi_data": get_kpi_data(),
        "m2_liquidity": get_m2_liquidity_data(),
        "treasury_spread": get_treasury_spread_data(),
        "fed_funds_vs_10y": get_fed_funds_vs_10y_data(),
        "high_yield_index": get_high_yield_index_data()
    }