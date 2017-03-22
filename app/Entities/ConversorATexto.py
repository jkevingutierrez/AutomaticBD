class ConversorATexto:
    def transformarDependencias(self, dependencias):
        textoDependencias = []
        for dependencia in dependencias:
            separador = '.'
            texto = separador.join(dependencia.variablesImplicante) + ' -> ' + separador.join(dependencia.variablesImplicado)
            textoDependencias.append(texto)
        return textoDependencias

    def transformarDependencia(self, dependencia):
        separador = '.'
        texto = separador.join(dependencia.variablesImplicante) + ' -> ' + separador.join(dependencia.variablesImplicado)
        return texto