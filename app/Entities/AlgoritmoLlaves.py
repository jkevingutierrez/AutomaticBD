from app.Entities.Cierre import Cierre
from app.Entities.Archivo import Archivo
from app.Entities.ConversorATexto import ConversorATexto


class AlgoritmoLlaves:
    @staticmethod
    def calculo_llaves(dependencias):
        return dependencias

    @staticmethod
    def validar_z(relacion, z):
        archivo = Archivo()
        archivo.escribir_sobre_archivo_existente('Salida.txt', 'Paso 2 Validar cierre de Z:\n\n')

        cierre_z = Cierre.calcular_cierre(z, relacion.dependencias)
        return set(cierre_z) == set(relacion.atributos)

    @staticmethod
    def calcular_z(relacion):
        archivo = Archivo()
        archivo.escribir_sobre_archivo_existente('Salida.txt', 'Paso 1 Calcular Z:\n\n')

        atributos_implicado = extraer_atributos_implicado(relacion.dependencias)
        z = quitar_atributos(relacion.atributos, atributos_implicado)

        archivo.escribir_sobre_archivo_existente('Salida.txt', '\tZ = [')
        archivo.escribir_sobre_archivo_existente('Salida.txt', ConversorATexto.transformar_atributos(z))
        archivo.escribir_sobre_archivo_existente('Salida.txt', ']\n\n')

        return z

    @staticmethod
    def calcular_v(relacion, z, w):
        cierre_z = Cierre.calcular_cierre(z, relacion.dependencias)
        cierre_z_union_w = union(cierre_z, w)
        return quitar_atributos(relacion.atributos, cierre_z_union_w)

    @staticmethod
    def calcular_w(relacion):
        atributos_implicante = extraer_atributos_implicante(relacion.dependencias)
        w = quitar_atributos(relacion.atributos, atributos_implicante)
        return w


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


def union(a, b):
    return list(set(a) | set(b))
