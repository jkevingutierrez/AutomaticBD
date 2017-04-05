class ConversorATexto:

    @staticmethod
    def transformar_dependencias(dependencias):
        textoDependencias = []
        for dependencia in dependencias:
            separador = '.'
            texto = separador.join(dependencia.atributos_implicante) + ' -> ' + separador.join(dependencia.atributos_implicado)
            textoDependencias.append(texto)
        return textoDependencias

    @staticmethod
    def transformar_dependencia(dependencia):
        separador = '.'
        texto = separador.join(dependencia.atributos_implicante) + ' -> ' + separador.join(dependencia.atributos_implicado)
        return texto
