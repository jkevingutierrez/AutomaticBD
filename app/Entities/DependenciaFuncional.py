class DependenciaFuncional:
    def __init__(self, implicante, implicado):
        self.implicante = implicante
        self.implicado = implicado

        if type(implicado) is str:
            self.implicado = []
            self.implicado.append(implicado)
