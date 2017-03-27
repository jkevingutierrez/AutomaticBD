class DependenciaFuncional:
    def __init__(self, atributosImplicante, atributosImplicado):
        self.atributosImplicante = atributosImplicante
        self.atributosImplicado = atributosImplicado

        if type(atributosImplicado) is str:
            self.atributosImplicado = []
            self.atributosImplicado.append(atributosImplicado)