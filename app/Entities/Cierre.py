from app.Entities.Archivo import Archivo
from app.Entities.ConversorATexto import ConversorATexto
from app.Entities.ListHelper import ListHelper


class Cierre:
    @staticmethod
    def calcular_cierre(atributos, dependencias, nombre=''):
        separador = ', '
        cierre = []

        if (type(atributos) is str or len(atributos) > 0) and len(dependencias) > 0:
            longitud = 0

            Archivo.escribir_sobre_archivo_existente('Salida.txt', '\t\tCierre(')
            Archivo.escribir_sobre_archivo_existente('Salida.txt', separador.join(atributos))
            Archivo.escribir_sobre_archivo_existente('Salida.txt', ') = [')

            if type(atributos) is list and len(atributos) > 0:
                cierre = sorted(atributos)[:]
            elif type(atributos) is str:
                cierre.append(atributos)

            while longitud < len(cierre):
                longitud = len(cierre)
                cierreInicial = cierre[:]

                for dependencia in dependencias:
                    contieneAtributos = ListHelper.contiene_todos(dependencia.implicante, cierre)
                    atributoImplicado = dependencia.implicado[0]

                    if len(dependencia.implicante) <= len(cierreInicial) and \
                                    contieneAtributos is True and \
                                    atributoImplicado not in cierre:
                        cierre.extend(dependencia.implicado)

            cierre_ordenado = sorted(cierre)
            Archivo.escribir_sobre_archivo_existente('Salida.txt', separador.join(cierre_ordenado))
            Archivo.escribir_sobre_archivo_existente('Salida.txt', '] en [')
            Archivo.escribir_sobre_archivo_existente('Salida.txt',
                                                     separador.join(
                                                         ConversorATexto.transformar_dependencias(dependencias)))
            Archivo.escribir_sobre_archivo_existente('Salida.txt', ']\n')
            return cierre_ordenado
        else:
            Archivo.escribir_sobre_archivo_existente('Salida.txt', '\t\tCierre(')
            Archivo.escribir_sobre_archivo_existente('Salida.txt', nombre)
            Archivo.escribir_sobre_archivo_existente('Salida.txt', ') = []\n')
            return cierre
