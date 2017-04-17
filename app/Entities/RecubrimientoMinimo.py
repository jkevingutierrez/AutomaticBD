from app.Entities.Archivo import Archivo
from app.Entities.Buscador import Buscador
from app.Entities.Cierre import Cierre
from app.Entities.ConversorATexto import ConversorATexto
from app.Entities.DependenciaFuncional import DependenciaFuncional
from app.Entities.ListHelper import ListHelper


class RecubrimientoMinimo:
    @staticmethod
    def dependencias_elementales(dependencias):
        l1 = []

        Archivo.escribir_sobre_archivo_existente('Salida.txt', 'Paso 1 Agregar Dependencias Elementales:\n\n')

        for dependencia in dependencias:
            existe_dependencia = Buscador.buscar_dependencia(dependencia, l1)
            if len(dependencia.implicado) == 1 and existe_dependencia is False and ListHelper.son_iguales(
                    dependencia.implicante,
                    dependencia.implicado) is False:
                Archivo.escribir_sobre_archivo_existente('Salida.txt', '\tAgregar dependencia elemental: ')
                Archivo.escribir_sobre_archivo_existente('Salida.txt',
                                                         ConversorATexto.transformar_dependencia(dependencia))
                Archivo.escribir_sobre_archivo_existente('Salida.txt', '\n\n')

                l1.append(dependencia)
            else:
                for atributo in dependencia.implicado:
                    nueva_dependencia = DependenciaFuncional(dependencia.implicante, atributo)
                    existe_dependencia = Buscador.buscar_dependencia(nueva_dependencia, l1)

                    if existe_dependencia is False and ListHelper.son_iguales(nueva_dependencia.implicante,
                                                                              nueva_dependencia.implicado) is False:
                        Archivo.escribir_sobre_archivo_existente('Salida.txt', '\tAgregar dependencia elemental: ')
                        Archivo.escribir_sobre_archivo_existente('Salida.txt', ConversorATexto.transformar_dependencia(
                            nueva_dependencia))
                        Archivo.escribir_sobre_archivo_existente('Salida.txt', '\n\n')
                        l1.append(nueva_dependencia)

        Archivo.escribir_sobre_archivo_existente('Salida.txt', '\n')
        return l1

    @staticmethod
    def atributos_extranos(dependencias):
        l2 = []

        existe_cierre = {}

        Archivo.escribir_sobre_archivo_existente('Salida.txt', 'Paso 2 Eliminar Atributos Extraños:\n\n')

        for dependencia in dependencias:
            existe_dependencia = Buscador.buscar_dependencia(dependencia, l2)

            if len(dependencia.implicante) == 1 and existe_dependencia is False:
                l2.append(dependencia)
            else:
                atributos_auxiliares = dependencia.implicante[:]
                for i in reversed(range(len(atributos_auxiliares))):
                    cierre_array = []
                    atributo = atributos_auxiliares[i]
                    atributos_temporales = ListHelper.remover_index(atributos_auxiliares, i)
                    llave = '-'.join(atributos_temporales)

                    if len(atributos_temporales) > 0 and llave not in existe_cierre:
                        cierre_array = Cierre.calcular_cierre(atributos_temporales, dependencias)
                        existe_cierre[llave] = cierre_array
                    elif llave:
                        cierre_array = existe_cierre[llave]

                    contiene_atributo = ListHelper.contiene_todos(dependencia.implicado, cierre_array)

                    if contiene_atributo is True and len(cierre_array) > 0:
                        atributos_auxiliares.pop(i)
                        Archivo.escribir_sobre_archivo_existente('Salida.txt', '\n\tEliminar atributo: ')
                        Archivo.escribir_sobre_archivo_existente('Salida.txt', atributo)
                        Archivo.escribir_sobre_archivo_existente('Salida.txt', ' de ')
                        Archivo.escribir_sobre_archivo_existente('Salida.txt',
                                                                 ConversorATexto.transformar_dependencia(dependencia))
                        Archivo.escribir_sobre_archivo_existente('Salida.txt', '\n\n')

                    nueva_dependencia = DependenciaFuncional(atributos_auxiliares, dependencia.implicado)
                    existe_nueva_dependencia = Buscador.buscar_dependencia(nueva_dependencia, l2)
                    if existe_nueva_dependencia is False:
                        l2.append(nueva_dependencia)

        Archivo.escribir_sobre_archivo_existente('Salida.txt', '\n')
        return l2

    @staticmethod
    def dependencias_redundantes(dependencias):
        recubrimiento_minimo = []

        l2_auxiliar = dependencias[:]
        l2_auxiliar.reverse()

        Archivo.escribir_sobre_archivo_existente('Salida.txt', 'Paso 3 Eliminar Dependencias Redundantes:\n\n')

        for i in reversed(range(len(dependencias))):
            cierre_array = []
            dependencia = l2_auxiliar[i]
            dependencias_temporales = ListHelper.remover_index(l2_auxiliar, i)

            if len(dependencia.implicante) > 0:
                cierre_array = Cierre.calcular_cierre(dependencia.implicante, dependencias_temporales)

            contiene_atributo = ListHelper.contiene_todos(dependencia.implicado, cierre_array)
            existe_dependencia = Buscador.buscar_dependencia(dependencia, recubrimiento_minimo)
            if contiene_atributo is True and len(cierre_array) > 0:
                l2_auxiliar.pop(i)
                Archivo.escribir_sobre_archivo_existente('Salida.txt', '\n\tEliminar dependencia: ')
                Archivo.escribir_sobre_archivo_existente('Salida.txt',
                                                         ConversorATexto.transformar_dependencia(dependencia))
                Archivo.escribir_sobre_archivo_existente('Salida.txt', '\n\n')
            elif existe_dependencia is False:
                recubrimiento_minimo.append(dependencia)

        Archivo.escribir_sobre_archivo_existente('Salida.txt', '\n')
        return recubrimiento_minimo
