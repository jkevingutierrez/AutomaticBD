from app.Entities.DependenciaFuncional import DependenciaFuncional
from app.Entities.Cierre import Cierre
from app.Entities.Archivo import Archivo
from app.Entities.ConversorATexto import ConversorATexto
from app.Entities.Buscador import Buscador


class RecubrimientoMinimo:

    @staticmethod
    def dependencias_elementales(dependencias):
        l1 = []

        archivo = Archivo()
        archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', 'Paso 1 Agregar Dependencias Elementales:\n\n')

        for dependencia in dependencias:
            existe_dependencia = Buscador.buscar_dependencia(dependencia, l1)
            if len(dependencia.atributos_implicado) == 1 and existe_dependencia is False:
                archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', '\tAgregar dependencia elemental: ')
                archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', ConversorATexto.transformar_dependencia(dependencia))
                archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', '\n')
                l1.append(dependencia)
            else:
                for atributo in dependencia.atributos_implicado:
                    nueva_dependencia = DependenciaFuncional(dependencia.atributos_implicante, atributo)
                    existe_dependencia = Buscador.buscar_dependencia(nueva_dependencia, l1)
                    if existe_dependencia is False:
                        archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', '\tAgregar dependencia elemental: ')
                        archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', ConversorATexto.transformar_dependencia(nueva_dependencia))
                        archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', '\n')
                        l1.append(nueva_dependencia)

        archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', '\n')
        return l1

    @staticmethod
    def atributos_extranos(dependencias):
        l2 = []

        existe_cierre = {}

        archivo = Archivo()
        archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', 'Paso 2 Eliminar Atributos Extra\u00F1os:\n\n')

        for dependencia in dependencias:
            existe_dependencia = Buscador.buscar_dependencia(dependencia, l2)

            if len(dependencia.atributos_implicante) == 1 and existe_dependencia is False:
                l2.append(dependencia)
            else:
                atributos_auxiliares = dependencia.atributos_implicante[:]
                for i in reversed(range(len(atributos_auxiliares))):
                    cierre_array = []
                    atributo = atributos_auxiliares[i]
                    atributos_temporales = [elem for j, elem in enumerate(atributos_auxiliares) if i != j]
                    llave = '-'.join(atributos_temporales)

                    if len(atributos_temporales) > 0 and llave not in existe_cierre:
                        cierre_array = Cierre.calcular_cierre(atributos_temporales, dependencias)
                        existe_cierre[llave] = cierre_array
                    elif llave:
                        cierre_array = existe_cierre[llave]

                    contiene_atributo = all(elem in cierre_array for elem in dependencia.atributos_implicado)

                    if contiene_atributo is True and len(cierre_array) > 0:
                        atributos_auxiliares.pop(i)
                        archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', '\tEliminar atributo: ')
                        archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', atributo)
                        archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', ' en ')
                        archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', ConversorATexto.transformar_dependencia(dependencia))
                        archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', '\n')

                    nueva_dependencia = DependenciaFuncional(atributos_auxiliares, dependencia.atributos_implicado)
                    existe_nueva_dependencia = Buscador.buscar_dependencia(nueva_dependencia, l2)
                    if existe_nueva_dependencia is False:
                        l2.append(nueva_dependencia)

        archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', '\n')
        return l2

    @staticmethod
    def dependencias_redundantes(dependencias):
        recubrimiento_minimo = []

        l2_auxiliar = dependencias[:]
        l2_auxiliar.reverse()

        archivo = Archivo()
        archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', 'Paso 3 Eliminar Dependencias Redundantes:\n\n')

        for i in reversed(range(len(dependencias))):
            cierre_array = []
            dependencia = l2_auxiliar[i]
            dependencias_temporales = [dependencia for j, dependencia in enumerate(l2_auxiliar) if i != j]

            if len(dependencia.atributos_implicante) > 0:
                cierre_array = Cierre.calcular_cierre(dependencia.atributos_implicante, dependencias_temporales)

            contiene_atributo = all(elem in cierre_array for elem in dependencia.atributos_implicado)
            existe_dependencia = Buscador.buscar_dependencia(dependencia, recubrimiento_minimo)
            if contiene_atributo is True and len(cierre_array) > 0:
                l2_auxiliar.pop(i)
                archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', '\tEliminar dependencia: ')
                archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', ConversorATexto.transformar_dependencia(dependencia))
                archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', '\n')
            elif existe_dependencia is False:
                recubrimiento_minimo.append(dependencia)

        archivo.escribir_sobre_archivo_existente('Recubrimiento.txt', '\n')
        return recubrimiento_minimo
