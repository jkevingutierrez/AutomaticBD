from app.Entities.Archivo import Archivo
from app.Entities.ConversorATexto import ConversorATexto

class Cierre:
    def calcularCierre(self, variables, dependencias):

        cierre = []
        longitud = 0

        if type(variables) is list and len(variables) > 0:
            cierre = sorted(variables)[:]
        elif type(variables) is str:
            cierre.append(variables)

        conversor_texto = ConversorATexto()

        separador = ', '
        archivo = Archivo()
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\t\tCierre(')
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', separador.join(variables))
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', ') = [')

        while longitud < len(cierre):
            longitud = len(cierre)
            cierreInicial = cierre[:]

            for dependencia in dependencias:
                contieneVariables = all(elem in cierre for elem in dependencia.variablesImplicante)
                variableImplicado = dependencia.variablesImplicado[0]

                if len(dependencia.variablesImplicante) <= len(cierreInicial) and contieneVariables == True and variableImplicado not in cierre:
                    cierre.extend(dependencia.variablesImplicado)

        cierreOrdenado = sorted(cierre)
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', separador.join(cierreOrdenado))
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '] para ')
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '[')
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', separador.join(conversor_texto.transformarDependencias(dependencias)))
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', ']')
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\n')
        return cierreOrdenado

