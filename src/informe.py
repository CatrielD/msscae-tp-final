# objetos definidos para el informe usando lib/*.py ...  probablemente
# sea conveniente definirlo in situ en el informe, pero también dejo
# esto para que se pueda hacer un simple 'import informe' en el
# notebook (al menos localmente) o se puedan usar desde otro lado

from typing import List, Dict
from lib.utils import HS4_Product_Id, Country_Name

from lib.agente import PaisComplejo, PaisNaive
from lib.simulador import SimuladorComplejo, SimuladorEstatico, \
    SimuladorDinamico, SimuladorProductSpace

__all__ = [
    "PaisNaive",
    "PaisComplejo",
    "PaisHormiga",
    "PaisCigarra",
    "SimuladorEstatico",
    "SimuladorDinamico",
    "SimuladorComplejo",
    "SimuladorComplejoEstatico"
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


class SimuladorComplejoEstatico(SimuladorComplejo):
    def _actualizar_estado(self, output_iteracion: Dict[Country_Name, HS4_Product_Id]):
        self.current_step += 1

    def _notificar_paises(self):
        pass
