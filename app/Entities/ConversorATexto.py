class ConversorATexto:
    def transformarDependencias(self, dependencias):
        textoDependencias = []
        for dependencia in dependencias:
            separador = '.'
            texto = separador.join(dependencia.atributosImplicante) + ' -> ' + separador.join(dependencia.atributosImplicado)
            textoDependencias.append(texto)
        return textoDependencias

    def transformarDependencia(self, dependencia):
        separador = '.'
        texto = separador.join(dependencia.atributosImplicante) + ' -> ' + separador.join(dependencia.atributosImplicado)
        return texto