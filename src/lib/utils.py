from pandas import DataFrame
import time
from typing import List, Dict  # , Self # recién en py3.11
import numpy as np

HS4_Product_Id = int
Country_Id = str  # deprecado
Country_Name = str
Tiempo = int


class SubclassResponsability(Exception):
    def __init__(self):
        super().__init__("Subclass Responsability: este método tiene que ser implementado por una subclase")  # noqa


def print_m(msg, mostrar=True):
    if mostrar:
        print(msg)

def epoch_2_date_str(epoch):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))


def default_collector(output, pais, productos_terminados):
    output[pais.country_name] = productos_terminados


def pais_collector(output, pais, productos_terminados):
    output[pais] = productos_terminados


def default_formatter(pais, prod_terminados, pad):
    return f"\t{str(pais):-<{pad}}> descubrió {len(prod_terminados)}"


def pais_con_producciones_e_investigaciones_formatter(pais, prod_terminados, pad):
    return f"\t{str(pais):-<{pad}}> descubrió {len(prod_terminados)} en investigación: {len(pais.productos_en_investigacion())}"


def correr_simulacion_mostrando(sim, mostrar=True, pad=40,
                                collector=default_collector,
                                formatter=default_formatter) -> List[Dict[Country_Name, List[HS4_Product_Id]]]:
    res = []
    start = time.time()
    it_start = time.time()
    print_m(f"empezando simulación: {epoch_2_date_str(start)}")
    for d in sim.iterar_simulacion(collector):
        res.append(d)
        print_m(f"iteración: {sim.current_step}", mostrar)
        for pais, productos in d.items():
            print_m(formatter(pais, productos, pad), mostrar) # noqa
        print_m(f"tiempo iteración: {time.time() - it_start}", mostrar)
        it_start = time.time()
    print_m(f"tiempo total: {time.time() - start}", mostrar)
    return res


def get_country_name(country_name, df: DataFrame):
    return df[df["Country ID"] == country_name]["Country"].values[0]


def consecutive_pairs(lst) -> list[tuple[int, int]]:
    pairs = zip(lst[:-1], lst[1:])
    res = []
    beg = lst[0]
    for c, n in pairs:
        if n > c + 1:
            res.append((beg, c))
            beg = n
    res.append((beg, lst[-1]))
    return res


def cantidad_descubrimientos_iteracion(historia, paises = None):
    return np.array(
        [ np.sum([len(descubrimientos) \
                  for p_name, descubrimientos in d.items() if not paises or p_name in paises]) \
          for d in historia ])


def cantidad_descubrimientos_paises(historia) -> dict[str]:
    res = {}
    for h in historia:
        for pais, productos in h.items():
            acc = res.get(pais,0) 
            acc += len(productos)
            res[pais] = acc
    return res
