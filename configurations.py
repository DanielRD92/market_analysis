# FRED Series IDs para los indicadores.
# Centralizar estos IDs aquí hace que el script de datos sea más fácil de leer y mantener.
FRED_SERIES_IDS = {
    "M2_SUPPLY": "M2SL",
    "TEN_YEAR_TREASURY": "DGS10",
    "THREE_MONTH_TREASURY": "DTB3",
    "FED_FUNDS": "FEDFUNDS",
    "HIGH_YIELD_INDEX": "BAMLH0A0HYM2EY",
    # KPIs
    "GDP_GROWTH": "A191RL1Q225SBEA", # Crecimiento del PIB Real, % trimestral
    "INFLATION_RATE": "DPCCRV1Q225SBEA", # Inflación CPI, % interanual
}

# Rango de años para obtener los datos históricos.
DATA_YEARS_RANGE = 5