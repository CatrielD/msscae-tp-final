from pandas import DataFrame
import time
from typing import List, Dict  # , Self # recién en py3.11


HS4_Product_Id = int
Country_Id = str
Tiempo = int


class SubclassResponsability(Exception):
    def __init__(self):
        super().__init__("Subclass Responsability: este método tiene que ser implementado por una subclase")  # noqa


def print_m(msg, mostrar=True):
    if mostrar:
        print(msg)


def correr_simulacion_mostrando(sim, mostrar=True)\
        -> List[Dict[Country_Id, List[HS4_Product_Id]]]:
    "horrible esta función"
    res = []
    start = time.time()
    it_start = time.time()
    for d in sim.iterar_simulacion():
        res.append(d)
        print_m(f"iteración: {sim.current_step}", mostrar)
        for pais, productos in d.items():
            print_m(f"\t{pais.country_id}: descubrió {len(productos)}\t({pais})", mostrar) # noqa
        print_m(f"tiempo iteración: {time.time() - it_start}", mostrar)
        it_start = time.time()
    print_m(f"tiempo total: {time.time() - start}", mostrar)
    return res


def get_country_name(country_id, df: DataFrame):
    return df[df["Country ID"] == country_id]["Country"].values[0]


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
