class DependenciaFuncional:
    def __init__(self, atributos_implicante, atributos_implicado):
        self.atributos_implicante = atributos_implicante
        self.atributos_implicado = atributos_implicado

        if type(atributos_implicado) is str:
            self.atributos_implicado = []
            self.atributos_implicado.append(atributos_implicado)
