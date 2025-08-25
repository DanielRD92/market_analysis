import os
import pandas as pd
from fredapi import Fred
from configurations import FRED_SERIES_IDS

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
def format_series_for_chartjs(series: pd.Series, start_date="2010-01-01"):
    """Filtra, limpia y formatea una serie de Pandas para Chart.js."""
    series = series.loc[start_date:].dropna()
    return {
        "labels": series.index.strftime('%Y-%m-%d').tolist(),
        "data": series.round(2).tolist()
    }

# --- Funciones de Obtención de Datos (PLACEHOLDERS) ---
# NOTA: Aquí es donde integrarás tus funciones reales que obtienen los datos.

def get_m2_liquidity_data():
    """Obtiene el agregado monetario M2."""
    print("Obteniendo datos de M2...")
    m2 = fred.get_series(FRED_SERIES_IDS["M2_SUPPLY"])
    return format_series_for_chartjs(m2)

def get_treasury_spread_data():
    """Calcula el spread entre el bono del tesoro a 10 años y 3 meses."""
    print("Obteniendo datos del Spread del Tesoro...")
    ten_year = fred.get_series(FRED_SERIES_IDS["TEN_YEAR_TREASURY"])
    three_month = fred.get_series(FRED_SERIES_IDS["THREE_MONTH_TREASURY"])
    spread = (ten_year - three_month)
    return format_series_for_chartjs(spread)

def get_fed_funds_vs_10y_data():
    """Obtiene la tasa de fondos federales y el rendimiento del bono a 10 años."""
    print("Obteniendo datos de Fed Funds vs 10-Year...")
    fed_funds = fred.get_series(FRED_SERIES_IDS["FED_FUNDS"], start_date="2010-01-01").dropna()
    ten_year = fred.get_series(FRED_SERIES_IDS["TEN_YEAR_TREASURY"], start_date="2010-01-01").dropna()
    
    # Alinear datos a una frecuencia mensual para la comparación
    df = pd.concat([fed_funds.resample('MS').mean(), ten_year.resample('MS').mean()], axis=1).dropna()
    df.columns = ['fed_funds', 'ten_year']
    
    return {
        "labels": df.index.strftime('%Y-%m').tolist(),
        "fed_funds": df['fed_funds'].round(2).tolist(),
        "ten_year": df['ten_year'].round(2).tolist()
    }

def get_high_yield_index_data():
    """Obtiene el rendimiento del índice de bonos de alto riesgo."""
    print("Obteniendo datos del Índice High-Yield...")
    # ICE BofA US High Yield Index Effective Yield
    high_yield = fred.get_series(FRED_SERIES_IDS["HIGH_YIELD_INDEX"])
    return format_series_for_chartjs(high_yield)

def get_all_data():
    """Recopila y devuelve todos los datos de los indicadores en un único diccionario."""
    if not fred:
        raise Exception("El cliente de FRED no está inicializado. Revisa la variable de entorno FRED_API_KEY.")
    return {
        "m2_liquidity": get_m2_liquidity_data(),
        "treasury_spread": get_treasury_spread_data(),
        "fed_funds_vs_10y": get_fed_funds_vs_10y_data(),
        "high_yield_index": get_high_yield_index_data()
    }