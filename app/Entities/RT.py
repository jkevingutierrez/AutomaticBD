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

    def validarAtributos(self):
        for dependencia in self.l:
            for atributo in dependencia.atributosImplicado:
                if atributo not in self.t:
                    return atributo
            for atributo in dependencia.atributosImplicante:
                if atributo not in self.t:
                    return atributo

        return True

    def buscarDependencia(self, dependencia, dependencias):
        for dependenciaActual in dependencias:
            if sorted(dependencia.atributosImplicado) == sorted(dependenciaActual.atributosImplicado) and \
                    sorted(dependencia.atributosImplicante) == sorted(dependenciaActual.atributosImplicante):
                return True

        return False

    def dependenciasElementales(self):
        self.l1 = []
        self.l2 = []
        self.l3 = []

        archivo = Archivo()
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', 'Paso 1 Agregar Dependencias Elementales:\n\n')

        for dependencia in self.l:
            existeDependencia = self.buscarDependencia(dependencia, self.l1)
            if len(dependencia.atributosImplicado) == 1 and existeDependencia is False:
                archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\tAgregar dependencia elemental: ')
                archivo.escribirSobreArchivoExistente('Recubrimiento.txt', ConversorATexto.transformarDependencia(dependencia))
                archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\n')
                self.l1.append(dependencia)
            else:
                for atributo in dependencia.atributosImplicado:
                    nuevaDependencia = DependenciaFuncional(dependencia.atributosImplicante, atributo)
                    existeDependencia = self.buscarDependencia(nuevaDependencia, self.l1)
                    if existeDependencia is False:
                        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\tAgregar dependencia elemental: ')
                        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', ConversorATexto.transformarDependencia(nuevaDependencia))
                        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\n')
                        self.l1.append(nuevaDependencia)

        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\n')
        return self.l1

    def atributosExtranos(self):
        self.l2 = []
        self.l3 = []

        existeCierre = {}

        llave = ''

        archivo = Archivo()
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', 'Paso 2 Eliminar Atributos Extra\u00F1os:\n\n')

        for dependencia in self.l1:
            existeDependencia = self.buscarDependencia(dependencia, self.l2)

            if len(dependencia.atributosImplicante) == 1 and existeDependencia is False:
                self.l2.append(dependencia)
            else:
                atributosAuxiliar = dependencia.atributosImplicante[:]
                for i in reversed(range(len(atributosAuxiliar))):
                    cierreArray = []
                    atributo = atributosAuxiliar[i]
                    atributosTemporales = [elem for j, elem in enumerate(atributosAuxiliar) if i != j]
                    llave = '-'.join(atributosTemporales)

                    if len(atributosTemporales) > 0 and llave not in existeCierre:
                        cierreArray = Cierre.calcularCierre(atributosTemporales, self.l1)
                        existeCierre[llave] = cierreArray
                    elif not llave:
                        cierreArray = existeCierre[llave]

                    contieneAtributo = all(elem in cierreArray for elem in dependencia.atributosImplicado)

                    if contieneAtributo is True and len(cierreArray) > 0:
                        atributosAuxiliar.pop(i)
                        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\tEliminar atributo: ')
                        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', atributo)
                        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', ' en ')
                        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', ConversorATexto.transformarDependencia(dependencia))
                        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\n')

                    nuevaDependencia = DependenciaFuncional(atributosAuxiliar, dependencia.atributosImplicado)
                    existeNuevaDependencia = self.buscarDependencia(nuevaDependencia, self.l2)
                    if existeNuevaDependencia is False:
                        self.l2.append(nuevaDependencia)

        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\n')
        return self.l2

    def dependenciasRedundantes(self):
        self.l3 = []

        l2Auxiliar = self.l2[:]
        l2Auxiliar.reverse()

        archivo = Archivo()
        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', 'Paso 3 Eliminar Dependencias Redundantes:\n\n')

        for i in reversed(range(len(self.l2))):
            cierreArray = []
            dependencia = l2Auxiliar[i]
            dependenciasTemporales = [elem for j, elem in enumerate(l2Auxiliar) if i != j]

            if len(dependencia.atributosImplicante) > 0:
                cierreArray = Cierre.calcularCierre(dependencia.atributosImplicante, dependenciasTemporales)

            contieneAtributo = all(elem in cierreArray for elem in dependencia.atributosImplicado)
            existeDependencia = self.buscarDependencia(dependencia, self.l3)
            if contieneAtributo is True and len(cierreArray) > 0:
                l2Auxiliar.pop(i)
                archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\tEliminar dependencia: ')
                archivo.escribirSobreArchivoExistente('Recubrimiento.txt', ConversorATexto.transformarDependencia(dependencia))
                archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\n')
            elif existeDependencia is False:
                self.l3.append(dependencia)

        archivo.escribirSobreArchivoExistente('Recubrimiento.txt', '\n')
        return self.l3
