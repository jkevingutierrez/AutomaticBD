class ConversorATexto:
    @staticmethod
    def transformar_dependencias(dependencias):
        textoDependencias = []
        for dependencia in dependencias:
            separador = '.'
            texto = separador.join(dependencia.implicante) + ' -> ' + separador.join(dependencia.implicado)
            textoDependencias.append(texto)
        return textoDependencias

    @staticmethod
    def transformar_dependencia(dependencia):
        separador = '.'
        texto = separador.join(dependencia.implicante) + ' -> ' + separador.join(dependencia.implicado)
        return texto

    @staticmethod
    def transformar_atributos(atributos):
        separador = ', '
        texto = separador.join(atributos)
        return texto

    @staticmethod
    def transformar_llaves(llaves):
        texto = '[ '
        separador = ', '
        first = True
        for llave in llaves:
            if isinstance(llave, (list, tuple, set)) and len(llave) > 0:
                if first:
                    first = False
                    texto += '('
                else:
                    texto += ', ('

                texto += separador.join(llave)
                texto += ')'
            elif type(llave) is str:
                texto += separador.join(llaves)
                break

        texto += ' ]'
        return texto
