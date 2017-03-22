class DependenciaFuncional:
    def __init__(self, variablesImplicante, variablesImplicado):
        self.variablesImplicante = variablesImplicante
        self.variablesImplicado = variablesImplicado

        if type(variablesImplicado) is str:
            self.variablesImplicado = []
            self.variablesImplicado.append(variablesImplicado)