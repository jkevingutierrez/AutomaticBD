from app.Entities.DependenciaFuncional import DependenciaFuncional
from app.Entities.Cierre import Cierre
from app.Entities.Archivo import Archivo
from app.Entities.ConversorATexto import ConversorATexto


class RT:
    def __init__(self, t, l):
        self.t = sorted(t)
        self.l = l
        self.l1 = []
        self.l2 = []
        self.l3 = []

    def validarVariables(self):
        for dependencia in self.l:
            for variable in dependencia.variablesImplicado:
                if variable not in self.t:
                    return variable
            for variable in dependencia.variablesImplicante:
                if variable not in self.t:
                    return variable

        return True

    def buscarDependencia(self, dependencia, dependencias):
        for dependenciaActual in dependencias:
            if sorted(dependencia.variablesImplicado) == sorted(dependenciaActual.variablesImplicado) and \
                    sorted(dependencia.variablesImplicante) == sorted(dependenciaActual.variablesImplicante):
                return True

        return False

    def dependenciasElementales(self):
        self.l1 = []
        self.l2 = []
        self.l3 = []

        conversor_text = ConversorATexto()


        archivo = Archivo()
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', 'Paso 1 Agregar Dependencias Elementales:\n\n')

        for dependencia in self.l:
            existeDependencia = self.buscarDependencia(dependencia, self.l1)
            if len(dependencia.variablesImplicado) == 1 and existeDependencia == False:
                archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\tAgregar dependencia elemental: ')
                archivo.escribirSobreArchivoExistente('Recubrimiento.txt', conversor_text.transformarDependencia(dependencia))
                archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\n')
                self.l1.append(dependencia)
            else:
                for variable in dependencia.variablesImplicado:
                    nuevaDependencia = DependenciaFuncional(dependencia.variablesImplicante, variable)
                    existeDependencia = self.buscarDependencia(nuevaDependencia, self.l1)
                    if existeDependencia == False:
                        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\tAgregar dependencia elemental: ')
                        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', conversor_text.transformarDependencia(nuevaDependencia))
                        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\n')
                        self.l1.append(nuevaDependencia)

        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\n')
        return self.l1

    def atributosExtranos(self):
        self.l2 = []
        self.l3 = []

        cierre = Cierre()

        conversor_text = ConversorATexto()

        archivo = Archivo()
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', 'Paso 2 Eliminar Atributos Extraños:\n\n')

        for dependencia in self.l1:
            existeDependencia = self.buscarDependencia(dependencia, self.l2)

            if len(dependencia.variablesImplicante) == 1 and existeDependencia == False:
                self.l2.append(dependencia)
            else:
                variablesAuxiliar = dependencia.variablesImplicante[:]
                for i in reversed(range(len(variablesAuxiliar))):
                    cierreArray = []
                    variable = variablesAuxiliar[i]
                    variablesTemporales = [elem for j, elem in enumerate(variablesAuxiliar) if i != j]
                    if len(variablesTemporales) > 0:
                        cierreArray = cierre.calcularCierre(variablesTemporales, self.l1)


                    contieneVariable = all(elem in cierreArray for elem in dependencia.variablesImplicado)

                    if contieneVariable == True and len(cierreArray) > 0:
                        variablesAuxiliar.pop(i)
                        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\tEliminar variable: ')
                        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', variable)
                        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', ' en ')
                        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', conversor_text.transformarDependencia(dependencia))
                        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\n')

                    nuevaDependencia = DependenciaFuncional(variablesAuxiliar, dependencia.variablesImplicado);
                    existeNuevaDependencia = self.buscarDependencia(nuevaDependencia, self.l2);
                    if existeNuevaDependencia == False:
                        self.l2.append(nuevaDependencia)

        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\n')
        return self.l2

    def dependenciasRedundantes(self):
        self.l3 = []

        l2Auxiliar = self.l2[:]
        l2Auxiliar.reverse()
        cierre = Cierre()

        conversor_text = ConversorATexto()

        archivo = Archivo()
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', 'Paso 3 Eliminar Dependencias Redundantes:\n\n')

        for i in reversed(range(len(self.l2))):
            cierreArray = []
            dependencia = l2Auxiliar[i]
            dependenciasTemporales = [elem for j, elem in enumerate(l2Auxiliar) if i != j]

            if len(dependencia.variablesImplicante) > 0:
                cierreArray = cierre.calcularCierre(dependencia.variablesImplicante, dependenciasTemporales)

            contieneVariable = all(elem in cierreArray for elem in dependencia.variablesImplicado)
            existeDependencia = self.buscarDependencia(dependencia, self.l3)
            if contieneVariable == True and len(cierreArray) > 0:
                l2Auxiliar.pop(i)
                archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\tEliminar dependencia: ')
                archivo.escribirSobreArchivoExistente('Recubrimiento.txt', conversor_text.transformarDependencia(dependencia))
                archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\n')
            elif existeDependencia == False:
                self.l3.append(dependencia)

        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\n')
        return self.l3

