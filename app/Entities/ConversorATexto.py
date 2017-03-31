class ConversorATexto:

    @staticmethod
    def transformarDependencias(dependencias):
        textoDependencias = []
        for dependencia in dependencias:
            separador = '.'
            texto = separador.join(dependencia.atributosImplicante) + ' -> ' + separador.join(dependencia.atributosImplicado)
            textoDependencias.append(texto)
        return textoDependencias

    @staticmethod
    def transformarDependencia(dependencia):
        separador = '.'
        texto = separador.join(dependencia.atributosImplicante) + ' -> ' + separador.join(dependencia.atributosImplicado)
        return texto
