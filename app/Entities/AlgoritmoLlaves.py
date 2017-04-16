from app.Entities.Archivo import Archivo
from app.Entities.Cierre import Cierre
from app.Entities.ConversorATexto import ConversorATexto
from app.Entities.ListHelper import ListHelper


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
        z = sorted(ListHelper.diferencia(relacion.atributos, atributos_implicado))

        Archivo.escribir_sobre_archivo_existente('Salida.txt', '\tZ = [')
        Archivo.escribir_sobre_archivo_existente('Salida.txt', ConversorATexto.transformar_atributos(z))
        Archivo.escribir_sobre_archivo_existente('Salida.txt', ']\n\n')

        return z

    @staticmethod
    def calcular_v(relacion, cierre_z, w):
        Archivo.escribir_sobre_archivo_existente('Salida.txt', 'Paso 4 Calcular V:\n\n')

        cierre_z_union_w = ListHelper.union(cierre_z, w)

        v = sorted(ListHelper.diferencia(relacion.atributos, cierre_z_union_w))

        Archivo.escribir_sobre_archivo_existente('Salida.txt', '\tV = [')
        Archivo.escribir_sobre_archivo_existente('Salida.txt', ConversorATexto.transformar_atributos(v))
        Archivo.escribir_sobre_archivo_existente('Salida.txt', ']\n\n')

        return v

    @staticmethod
    def calcular_w(relacion):
        Archivo.escribir_sobre_archivo_existente('Salida.txt', '\nPaso 3 Calcular W:\n\n')

        atributos_implicante = extraer_atributos_implicante(relacion.dependencias)
        w = ListHelper.diferencia(relacion.atributos, atributos_implicante)

        Archivo.escribir_sobre_archivo_existente('Salida.txt', '\tW = [')
        Archivo.escribir_sobre_archivo_existente('Salida.txt', ConversorATexto.transformar_atributos(w))
        Archivo.escribir_sobre_archivo_existente('Salida.txt', ']\n\n')

        return w

    @staticmethod
    def iterar(v, z, relacion):
        Archivo.escribir_sobre_archivo_existente('Salida.txt', '\nPaso 4 Iterar sobre ZuV:\n\n')
        m1 = []
        m2 = []

        if (len(z) > 0):
            for variable_z in z:
                for variable_v in v:
                    print('Iterando')
                    variables = [variable_z, variable_v]
                    Cierre.calcular_cierre(variables, relacion.dependencias)
                    m1.append(variables)

        else:
            for variable_v in v:
                variables = [variable_v]
                Cierre.calcular_cierre(variables, relacion.dependencias)
                m1.append(variables)

        print('m2:')
        print(m1)
        return m1


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
