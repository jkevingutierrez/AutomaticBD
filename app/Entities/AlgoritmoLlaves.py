from app.Entities.Cierre import Cierre

class AlgoritmoLlaves:

    @staticmethod
    def calculo_llaves(dependencias):
        return dependencias

    @staticmethod
    def validar_z(relacion):
        z = calcular_z(relacion)
        cierre_z = Cierre.calcular_cierre(z, relacion.dependencias)

        print(z)
        print(cierre_z)

        return set(cierre_z) == set(z)


def calcular_w(relacion):
    atributos_implicante = extraer_atributos_implicante(relacion.dependencias)
    return quitar_atributos(relacion.atributos, atributos_implicante)

def calcular_z(relacion):
    atributos_implicado = extraer_atributos_implicado(relacion.dependencias)
    return quitar_atributos(relacion.atributos, atributos_implicado)


def quitar_atributos(atributos_totales, atributos_a_quitar):
    atributos_resultantes = [atributo for atributo in atributos_totales if atributo not in atributos_a_quitar]
    return atributos_resultantes


def extraer_atributos_implicante(dependencias):
    atributos = []
    for dependencia in dependencias:
        for atributo in dependencia.implicante:
            if atributo not in atributos:
                atributos.append(atributo)
    return atributos


def extraer_atributos_implicado(dependencias):
    atributos = []
    for dependencia in dependencias:
        for atributo in dependencia.implicado:
            if atributo not in atributos:
                atributos.append(atributo)
    return atributos

