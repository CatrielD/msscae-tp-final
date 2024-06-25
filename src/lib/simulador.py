from typing import Iterator, Callable, Dict
from pandas import DataFrame
import economic_complexity as ecplx
from lib.utils import Country_Name, HS4_Product_Id, SubclassResponsability
import time

from lib.agente import PaisNaive, IPais

######################################################################
### Un coordinador de simulación es un sistema que:                ###
### - toma datos e inicializa agentes                              ###
### - itera hasta encontrar un criterio de parada.                 ###
### - En cada iteración:                                           ###
###   - le indica a cada agente que elija un producto a investigar ###
###   - coordina cuando se actualiza el estado del mundo compartido###
######################################################################


class Simulador:
    """framework de caja blanca ... HW cry me a river,
    en fin, el simulador ... ejem... simula, debería ser self explanatory"""

    def __init__(self,
                 criterio_parada: Callable[..., bool],
                 clase_pais: Callable[..., IPais]):
        self.criterio_parada = criterio_parada
        self._estado_inicial_de_parada()
        start = time.time()
        self._paises = self._crear_paises(clase_pais)
        print(f"paises creados en: {time.time() - start}")

    def simular(self):
        for _ in self.iterar_simulacion():
            continue

    def paises(self):
        return self._paises.values()

    # TODO: que devuelva lo que usa para contar el criterio de parada,
    # un counter, indice gini, etc
    def iterar_simulacion(self) -> Iterator[Dict[Country_Name, HS4_Product_Id]]:
        """Devuelve un iterador para poder simularlo por pasos y
        obtener para cada país que productos alcanzaron
        competitividad
        """
        while not self.es_fin_de_simulacion():
            output = {}
            # fase de decisiones
            for pais in self.paises():
                nuevos_productos = pais.elegir_productos()
                for pid in nuevos_productos:
                    pais.investigar_producto(pid)
            # fase de acciones
            for pais in self.paises():
                terminados = pais.avanzar_tiempo()
                output[pais.country_name] = terminados # como se podría generalizar lo que devuelve?
                pais.actualizar_exportaciones(terminados)

            self._actualizar_estado(output)
            self._notificar_paises()
            yield output

    def es_fin_de_simulacion(self) -> bool:
        raise SubclassResponsability

    ######################################################################
    ###                                                                ###
    ###                       privadas/protegidas                      ###
    ###                                                                ###
    ######################################################################

    def _crear_paises(self, clase_pais: Callable[..., IPais]) -> Dict[Country_Name, IPais]:
        raise SubclassResponsability

    def _actualizar_estado(self,
                           output_iteracion: Dict[Country_Name, HS4_Product_Id]):
        """se encarga del book keeping y la transiciones de estado que
        no sean, responsabilidad del país. Entre ellas, el conteo de
        pasos por ejemplo
        """
        raise SubclassResponsability

    def _notificar_paises(self):
        """cuando el estado del mundo cambia los paises deben
        enterarse para actualizar de ser necesario algún estado
        interno adicional a las exportaciones
        """
        raise SubclassResponsability

    def _estado_inicial_de_parada(self):
        raise SubclassResponsability


class SimuladorProductSpace(Simulador):
    """Simulador base, con paises Naive que opera sobre el grafo de
    proximidades, -mal llamado- product space
    """

    def __init__(self,
                 criterio_parada: Callable[..., bool],
                 clase_pais: Callable[..., IPais],
                 M: DataFrame, omega=0.4):
        self.M = M
        self.omega = omega
        start = time.time()
        self.proximidad = ecplx.proximity(M)
        print(f"proximidad calculada en: {time.time() - start}")
        # llamar al constructor de las super clases al final
        super().__init__(criterio_parada, clase_pais)

    # TODO tal vez un diseño mediante wrappers sería mejor? así puedo
    # cambiar facilmente el tipo de país y puedo sacar del constructor
    # el omega, podría tener una simulación con toda esta lógica pero
    # que no use omega
    def _crear_paises(self, clase_pais: Callable[..., IPais]):
        return {country_name:
                clase_pais(
                    country_name, self.M, self.proximidad, self.omega)
                for country_name in self.M.index}

    def _estado_inicial_de_parada(self):
        self.current_step = 0

    def _actualizar_estado(self, _):
        "este simulador no actualiza nada más que el contador de iteraciones"
        self.current_step += 1

    def es_fin_de_simulacion(self):
        return self.criterio_parada(self.current_step)


class SimuladorEstatico(SimuladorProductSpace):
    def _notificar_paises(self):
        pass  # no hace falta hacer nada, porque no hay modificación


class SimuladorDinamico(SimuladorProductSpace):
    def _actualizar_estado(self, _):
        self.proximidad = ecplx.proximity(self.M)
        super()._actualizar_estado(_)

    def _notificar_paises(self):
        for p in self.paises():
            # se podría pasar directamente por eficiencia, pero interfaz
            p.conocer_estado_del_mundo(proximidad=self.proximidad)


class SimuladorComplejo(SimuladorProductSpace):
    """Un simulador complejo tiene paises que consideran su complejidad"""
    def __init__(self,
                 criterio_parada: Callable[..., bool],
                 clase_pais: Callable[..., IPais],
                 M: DataFrame, omega=0.4):
        self.ECI, self.PCI = ecplx.complexity(M)
        super().__init__(criterio_parada, clase_pais, M, omega)

    def _actualizar_estado(self, output_iteracion: Dict[Country_Name, HS4_Product_Id]):
        self.ECI, self.PCI = ecplx.complexity(self.M)
        super()._actualizar_estado(output_iteracion)

    def _notificar_paises(self):
        for p in self.paises():
            p.conocer_estado_del_mundo(
                proximidad=self.proximidad,
                eci=self.ECI[p.country_name], PCI=self.PCI)

    def _crear_paises(self, clase_pais):
        return {country_name:
                clase_pais(
                    country_name, self.M,
                    self.proximidad,
                    self.ECI[country_name],
                    self.PCI,
                    self.omega)
                for country_name in self.M.index}

######################################################################
###                                                                ###
###            Finalmente los que usamos en el informe,            ###
###       se definen en ../informe.py o en el informe in situ      ###
###                                                                ###
######################################################################
