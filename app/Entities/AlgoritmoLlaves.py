from app.Entities.Archivo import Archivo
from app.Entities.ConversorATexto import ConversorATexto


class AlgoritmoLlaves:
    @staticmethod
    def calculo_llaves(dependencias):
        return dependencias

    @staticmethod
    def validar_cierre_z(relacion, cierre_z):
        Archivo.escribir_sobre_archivo_existente('Salida.txt', 'Paso 2 Validar cierre de Z:\n\n')

        es_igual = set(cierre_z) == set(relacion.atributos)

        if es_igual:
            Archivo.escribir_sobre_archivo_existente('Salida.txt', '\tCierre(Z) == atributos\n\n')
        else:
            Archivo.escribir_sobre_archivo_existente('Salida.txt', '\tCierre(Z) != atributos\n\n')

        return es_igual

    @staticmethod
    def calcular_z(relacion):
        Archivo.escribir_sobre_archivo_existente('Salida.txt', 'Paso 1 Calcular Z:\n\n')

        atributos_implicado = extraer_atributos_implicado(relacion.dependencias)
        z = quitar_atributos(relacion.atributos, atributos_implicado)

        Archivo.escribir_sobre_archivo_existente('Salida.txt', '\tZ = [')
        Archivo.escribir_sobre_archivo_existente('Salida.txt', ConversorATexto.transformar_atributos(z))
        Archivo.escribir_sobre_archivo_existente('Salida.txt', ']\n\n')

        return z

    @staticmethod
    def calcular_v(relacion, cierre_z, w):
        Archivo.escribir_sobre_archivo_existente('Salida.txt', 'Paso 4 Calcular V:\n\n')

        cierre_z_union_w = union(cierre_z, w)

        v = sorted(quitar_atributos(relacion.atributos, cierre_z_union_w))

        Archivo.escribir_sobre_archivo_existente('Salida.txt', '\tV = [')
        Archivo.escribir_sobre_archivo_existente('Salida.txt', ConversorATexto.transformar_atributos(v))
        Archivo.escribir_sobre_archivo_existente('Salida.txt', ']\n\n')

        return v

    @staticmethod
    def calcular_w(relacion):
        Archivo.escribir_sobre_archivo_existente('Salida.txt', '\nPaso 3 Calcular W:\n\n')

        atributos_implicante = extraer_atributos_implicante(relacion.dependencias)
        w = quitar_atributos(relacion.atributos, atributos_implicante)

        Archivo.escribir_sobre_archivo_existente('Salida.txt', '\tW = [')
        Archivo.escribir_sobre_archivo_existente('Salida.txt', ConversorATexto.transformar_atributos(w))
        Archivo.escribir_sobre_archivo_existente('Salida.txt', ']\n\n')

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
