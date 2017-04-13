class Buscador:
    @staticmethod
    def buscar_dependencia(dependencia, dependencias):
        for dependencia_actual in dependencias:
            if sorted(dependencia.implicado) == sorted(dependencia_actual.implicado) and \
                            sorted(dependencia.implicante) == sorted(dependencia_actual.implicante):
                return True

        return False
