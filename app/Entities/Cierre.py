from app.Entities.Archivo import Archivo
from app.Entities.ConversorATexto import ConversorATexto

class Cierre:
    def calcularCierre(self, atributos, dependencias):

        cierre = []
        longitud = 0

        if type(atributos) is list and len(atributos) > 0:
            cierre = sorted(atributos)[:]
        elif type(atributos) is str:
            cierre.append(atributos)

        conversor_texto = ConversorATexto()

        separador = ', '
        archivo = Archivo()
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\t\tCierre(')
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', separador.join(atributos))
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', ') = [')

        while longitud < len(cierre):
            longitud = len(cierre)
            cierreInicial = cierre[:]

            for dependencia in dependencias:
                contieneAtributos = all(elem in cierre for elem in dependencia.atributosImplicante)
                atributoImplicado = dependencia.atributosImplicado[0]

                if len(dependencia.atributosImplicante) <= len(cierreInicial) and contieneAtributos == True and atributoImplicado not in cierre:
                    cierre.extend(dependencia.atributosImplicado)

        cierreOrdenado = sorted(cierre)
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', separador.join(cierreOrdenado))
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '] para ')
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '[')
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', separador.join(conversor_texto.transformarDependencias(dependencias)))
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', ']')
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\n')
        return cierreOrdenado

