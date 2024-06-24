import requests
import pandas as pd
from pandas import DataFrame
from urllib.parse import urlencode
import pickle
from lib.utils import consecutive_pairs

# increiblemente esto funciona; tal vez sean datos falsos?
OEC_TOKEN = "REPLACE_HERE"

DATA_PATH = "../data/"

def encode_url(base_url, params):
    return f"{base_url}?{urlencode(params)}"


def request_data_from(url):
    r = requests.get(url)
    return pd.DataFrame(r.json()["data"])


def _year_list_to_str(*years):
    """consecutivos -> begin-end,
       no consecutivos -> first_second"""
    cns = consecutive_pairs(list(years))
    res = ""
    for beg, end in cns:
        if beg != end:
            res += f"_{beg}-{end}"
        else:
            res += f"_{end}"
    return res[1:]


def get_oec_data_of_years(years, file_name = None):
    "TODO: correct url"
    data = request_data_from(
        encode_url("https://oec.world/api/olap-proxy/data.jsonrecords",
                   {
                       "Year": ",".join(map(str, years)),
                       "cube": "trade_i_baci_a_92",
                       "drilldowns": "Exporter Country,Year,HS4",
                       "measures": "Trade Value",
                       "token": OEC_TOKEN
                   }))
    if file_name is not None:
        save_data_2_pickle(data, years, file_name)
    return data


def filter_biggests(df):
    df = df.copy()
    # Products with more than $1.5B in global exports between 2016-2018
    df_products = df.groupby('HS4 ID')['Trade Value'].sum().reset_index()
    df_products = df_products[df_products['Trade Value'] > 3*500000000]
    # Countries with more than $3B in global exports between 2016-2018
    df_countries = df.groupby('Country ID')['Trade Value'].sum().reset_index()
    df_countries = df_countries[df_countries['Trade Value'] > 3*1000000000]

    df_filter = df[
        (df['Country ID'].isin(df_countries['Country ID'])) &
        (df['HS4 ID'].isin(df_products['HS4 ID']))
    ]
    return df_filter


def build_country_product_values_table(df):
    return pd.pivot_table(df, index=['Country ID'],
                          columns=['HS4 ID'],
                          values='Trade Value')\
             .reset_index()\
             .set_index('Country ID')\
             .dropna(axis=1, how="all")\
             .fillna(0)\
             .astype(float)


DEFAULT_YEARS=[2018,2019,2020]
DEFAULT_OCE_FILE_NAME_PREFIX = f"default_oce_"
DEFAULT_OCE_FILE_NAME = f"{DEFAULT_OCE_FILE_NAME_PREFIX}{_year_list_to_str(*DEFAULT_YEARS)}"

def get_default_oec_rca_raw_data() -> tuple[DataFrame, DataFrame]:
    """ Obtener de la API los años 2018, 2019, 2020, filtrar los
    volumenes más grandes pivotear...
    Devuelve (RCA, Datos Crudos)
    Todo esto debería ir en el informe medianamente justificado """
    try:
        df_raw = load_data_from_pickle()
        print(f"Se encontró una caché para los datos en {DEFAULT_OCE_FILE_NAME_PREFIX}")
    except Exception as e:
        print("Sucedió algo al intentar obtener los datos crudos cacheados:"
              + f"\n{e}"
              + "\n¡Descargando y guardando datos en caché!"
              + "\n... plz be patient ...")
        df_raw = get_oec_data_of_years(DEFAULT_YEARS, DEFAULT_OCE_FILE_NAME_PREFIX)
    df_filtered = filter_biggests(df_raw)
    return build_country_product_values_table(df_filtered), df_raw


def build_M_from(rca):
    return rca.ge(1.0).astype(int)


def save_data_2_pickle(raw_data, years, pkl_file_name = None):
    if pkl_file_name is None:
        raise Exception("hace falta un nombre de archivo")
    pkl_file_full_name = f"{DATA_PATH}{pkl_file_name}{_year_list_to_str(*years)}.pkl"
    with open(pkl_file_full_name, "wb") as out:
        pickle.dump(raw_data, out)
        print(f"datos guardados en {pkl_file_full_name}")


def load_data_from_pickle(pkl_file_name=DEFAULT_OCE_FILE_NAME):
    "TODO: Comprobar si son los datos de la cátedra y ajusta índices"
    with open(DATA_PATH + f"{pkl_file_name}.pkl", "rb") as pkl:
        return pickle.load(pkl)
