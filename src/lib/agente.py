from __future__ import annotations  # para poder type hint la clase
import math

# import economic_complexity as ecplx
# import numpy as np
# import pandas as pd

# esto me hace acordar a primegean seetheando con "no resuelvas
# problemas que todavía no tenés" esto está un poco sobrediseñado

from typing import List, Dict  # , Self # recién en py3.11
from pandas import Index, DataFrame, Series
import pandas as pd
import numpy as np
# import pandera
# from pandera.typing import DataFrame, Series

from lib.utils import SubclassResponsability, \
    HS4_Product_Id, Country_Name, Tiempo


class IPais:
    """
    Se define una interfaz para lo que es un pais.
    Distintos Paises pueden tener
    - distintas estrategias de elección de productos.
    - distintas fronteras de productos.
    - distintos tiempos para alcanzar productos
    """

    def elegir_productos(self) -> List[HS4_Product_Id]:
        """Cada país tiene una forma de elegir los siguientes
        productos a ser producidos, es una lista porque podría haber
        más de uno en un solo turno.  Es la difusión efectiva.
        """
        raise SubclassResponsability

    def tiempo_para_ser_competitivo(self, pid: HS4_Product_Id) -> Tiempo:
        "Cuanto tiempo hasta ser competitivo? no cambia el estado"
        raise SubclassResponsability

    def investigar_producto(self, pid: HS4_Product_Id) -> Tiempo:
        """Usamos la metáfora de investigar, devuelve el tiempo
        necesario para terminar de lograrlo, dado el estado del
        agente
        """
        raise SubclassResponsability

    def frontera_de_productos(self) -> List[HS4_Product_Id]:
        "todos los productos alcanzables"
        raise SubclassResponsability

    def frontera_de_productos_df(self) -> DataFrame:  # DF[HS4_Product_Id]
        "todos los productos alcanzables"
        raise SubclassResponsability

    def es_exportado(self, pid: HS4_Product_Id) -> bool:
        raise SubclassResponsability

    def productos_exportados(self) -> List[HS4_Product_Id]:
        "los productos que ya se exportan"
        raise SubclassResponsability

    def investigando(self) -> List[HS4_Product_Id]:
        "Devuelve los productos actualmente bajo investigación"
        raise SubclassResponsability

    def actualizar_exportaciones(self, pdis: List[HS4_Product_Id]) -> IPais:
        """Modifica las exportaciones, según el estado actual del agente"""
        raise SubclassResponsability

    def conocer_estado_del_mundo(self, **estado_dict):
        "permite settear estados compartidos adicionales"
        raise SubclassResponsability

    def productos_en_investigacion(self) -> List[HS4_Product_Id]:
        raise SubclassResponsability

    def avanzar_tiempo(self) -> List[HS4_Product_Id]:
        """Avanza el tiempo y devuelve la lista de productos
        terminados en este turno"""
        raise SubclassResponsability


# Cada agente debe implementar la interfaz IPais, para que el
# simulador pueda usarlo. (Hay algunos métodos de más)
#
# Pero también hay pequeños objetos que implementan una fracción
# parcial de la misma, de alguna forma dada y reutilizable usando
# multiple herencia, se llaman Mixin. Son un patrón un poco polémico,
# porque vendrían a ser una poor man composition y la herencia múltiple
# suele traer problemas cuando el grafo de herencia crece mucho, pero
# para proyectos chicos a mi me agrada bastante:
#

class PaisBaseMixin:
    """Se encarga de la investigación y la exportación, esto es común
    para cualquier pais En este contexto cada país se encarga de
    actualizar un estado compartido: la matriz M de exportaciones
    competitivas, del resto se encarga el Simulador.  Este es un
    comportamiento base, sobre el cual cada instancia de Pais puede
    desarrollar
    """

    def __init__(self, country_name: str, M: DataFrame):  # DataFrame[bool]
        self.M = M
        self.country_name = country_name
        self._investigando_dict: Dict[HS4_Product_Id, Tiempo] = {}
        # start = time.time()
        # print(f"(PaisBaseMixin.__init__) productos exportados calculados en: {time.time() - start}")  # noqa

    def investigando(self) -> List[HS4_Product_Id]:
        return list(self._investigando_dict.keys())

    def investigar_producto(self, pid: HS4_Product_Id) -> Tiempo:
        if pid in self._investigando_dict:
            return self._investigando_dict[pid]
        tiempo = self.tiempo_para_ser_competitivo(pid)
        self._investigando_dict[pid] = tiempo
        return tiempo

    def productos_en_investigacion(self) -> List[HS4_Product_Id]:
        return list(self._investigando_dict.keys())

    def avanzar_tiempo(self) -> List[HS4_Product_Id]:
        terminados = []
        for pid, tiempo in self._investigando_dict.items():
            if tiempo == 1:
                terminados.append(pid)
            else:
                self._investigando_dict[pid] -= 1
        for pid in terminados:
            del self._investigando_dict[pid]
        return terminados

    def actualizar_exportaciones(self, pids: List[HS4_Product_Id]):
        """Modifica las exportaciones."""
        for pid in pids:
            self.M.loc[self.country_name, pid] = 1
        return self

    def productos_exportados_df(self) -> Index[HS4_Product_Id]:
        productos_pais = self.M.loc[self.country_name]
        return productos_pais[productos_pais == 1].index

    def productos_exportados(self) -> List[HS4_Product_Id]:
        return self.productos_exportados_df().to_list()

    def es_exportado(self, pid: HS4_Product_Id) -> bool:
        return self.M.loc[self.country_name][pid] == 1

    def __str__(self):
        return self.country_name


class PaisConCotaProximidadMixin:
    """Por ejemplo, un Pais en un mundo simple o inocente logra
    siempre lo que quiere, en cada paso de la simulación, siempre y
    cuando el producto esté a su alcance
    """

    def __init__(self,
                 M: DataFrame,  # [int]
                 proximity: DataFrame,  # [float]
                 omega: float):
        self.proximity = proximity
        self.omega = omega

    def frontera_de_productos_df(self) -> DataFrame:  # [HS4_Product_Id]
        "Todos los productos alcanzables, devuelve una máscara"
        productos_pais = self.M.loc[self.country_name]
        exportados = productos_pais[productos_pais == 1]
        no_exportados = productos_pais[productos_pais == 0]

        frontera = (self.proximity.loc[exportados.index][no_exportados.index] > self.omega) # noqa
        frontera = frontera.any(axis='rows')
        frontera = frontera[frontera]
        frontera = frontera[~ frontera.index.isin(self.productos_en_investigacion())].index
        return frontera

    def frontera_de_productos(self) -> List[HS4_Product_Id]:
        return self.frontera_de_productos_df().to_list()

    def elegir_productos(self) -> List[HS4_Product_Id]:
        return self.frontera_de_productos()

    def conocer_estado_del_mundo(self, **kwargs):
        self.proximity = kwargs["proximidad"]


class PaisNaive(PaisBaseMixin, PaisConCotaProximidadMixin, IPais):
    """Y por ejemplo ahora podemos definir un pais simple como una
    combinación de mixins tener cuidado con el orden de los
    mixins...

    Este pais logra en cada iteración accede a ser competitivo, en un
    turno a todos los productos que estén a su alcance.
    """
    def __init__(self, country_name: str,
                 M: DataFrame, proximidad: DataFrame, omega: float):
        "el constructor aglutina todo"
        PaisBaseMixin.__init__(self, country_name, M)
        PaisConCotaProximidadMixin.__init__(self, M, proximidad, omega)

    def tiempo_para_ser_competitivo(self, pid: HS4_Product_Id) -> Tiempo:
        return 1


# TODO, criterio de parada térmico (que frene cuando los cambios sean pocos)
#       (esa idea es para el simulador)
class PaisComplejo(PaisNaive, IPais):
    """Ok, este es el problema de los frameworks de subclasificación,
    esto no es un pais Naive, es todo lo contrario, sin embargo subclasifica
    porque es cómodo por el código compartido"""
    def __init__(self, country_name: str,
                 M: DataFrame,
                 proximidad: DataFrame,
                 eci, PCI,
                 omega: float,
                 tiempo_maximo = 10):
        self.tiempo_maximo = tiempo_maximo
        self.mi_eci = eci
        self.PCI = PCI
        self.min_pci = self.PCI.min()
        self.max_pci = self.PCI.max() + np.abs(self.min_pci)

        PaisNaive.__init__(self, country_name, M, proximidad, omega)

    def tiempo_para_ser_competitivo(self, pid: HS4_Product_Id) -> Tiempo:
        #"""TODO: discutir esto. además no se porque ECI y PCI dan negativos (ver más arriba)
        #esto es muy similar al cálculo de proximidad, pero en vez del máximo como define el paper se calcula el mínimo
        #(nosotros no calculamos el máximo, porque como es un umbral usamos .any(), ver el método frontera_de_productos_df)
        #"""
        # complejidad = self.PCI[pid]
        # return math.ceil(abs((complejidad / self.mi_eci)))
        """ basicamente tomo las complejidades de productos y mapeo linealmente entre 0 y 10.
             es decir el producto mas sencillo tarda 0 iteraciones, el mas complejo 10. """
        return np.ceil( self.tiempo_maximo * ( self.PCI.loc[pid] + np.abs(self.min_pci) ) / self.max_pci )

    def tiempos_para_ser_competitivo(self) -> Series[Tiempo]:
        frontera = self.frontera_de_productos()
        tiempos = [ self.tiempo_para_ser_competitivo(pid) for pid in frontera ]
        return pd.Series( tiempos, index=frontera)


######################################################################
###                                                                ###
###            Finalmente los que usamos en el informe,            ###
###       se definen en ../informe.py o en el informe in situ      ###
###                                                                ###
######################################################################
