# objetos definidos para el informe usando lib/*.py ...  probablemente
# sea conveniente definirlo in situ en el informe, pero también dejo
# esto para que se pueda hacer un simple 'import informe' en el
# notebook (al menos localmente)

from typing import List
from lib.utils import HS4_Product_Id

from lib.agente import PaisComplejo, PaisNaive
from lib.simulador import SimuladorComplejo, SimuladorEstatico, \
    SimuladorDinamico

__all__ = [
    "PaisNaive",
    "PaisHormiga",
    "PaisCigarra",
    "SimuladorEstatico",
    "SimuladorDinamico",
    "SimuladorComplejo"
]

class PaisHormiga(PaisComplejo):
    def elegir_productos(self) -> List[HS4_Product_Id]:
        #TODO: por qué el 10% y no 1 o config? ... я не знаю, потому
        "selecciona los primeros 10% de productos más complejos de su frontera"
        tiempos = self.tiempos_para_ser_competitivo()
        return tiempos.nlargest(int(len(tiempos) * 0.1)).index.to_list()


class PaisCigarra(PaisComplejo):
    def elegir_productos(self) -> List[HS4_Product_Id]:
        "selecciona los últimos 10% de productos más complejos de su frontera"
        tiempos = self.tiempos_para_ser_competitivo()
        return tiempos.nsmallest(int(len(tiempos) * 0.1)).index.to_list()
