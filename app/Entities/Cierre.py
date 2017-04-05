from app.Entities.Archivo import Archivo
from app.Entities.ConversorATexto import ConversorATexto


class Cierre:

    @staticmethod
    def calcular_cierre(atributos, dependencias):

        cierre = []
        longitud = 0

        if type(atributos) is list and len(atributos) > 0:
            cierre = sorted(atributos)[:]
        elif type(atributos) is str:
            cierre.append(atributos)

        separador = ', '
        archivo = Archivo()
        archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', '\t\tCierre(')
        archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', separador.join(atributos))
        archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', ') = [')

        while longitud < len(cierre):
            longitud = len(cierre)
            cierreInicial = cierre[:]

            for dependencia in dependencias:
                contieneAtributos = all(elem in cierre for elem in dependencia.implicante)
                atributoImplicado = dependencia.implicado[0]

                if len(dependencia.implicante) <= len(cierreInicial) and \
                        contieneAtributos is True and \
                        atributoImplicado not in cierre:
                    cierre.extend(dependencia.implicado)

        cierre_ordenado = sorted(cierre)
        archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', separador.join(cierre_ordenado))
        archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', '] en ')
        archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', '[')
        archivo.escribir_sobre_archivo_existente('Recubrimiento.txt',
                                              separador.join(ConversorATexto.transformar_dependencias(dependencias)))
        archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', ']')
        archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', '\n')
        return cierre_ordenado
