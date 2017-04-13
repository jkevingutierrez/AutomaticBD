from app.Entities.DependenciaFuncional import DependenciaFuncional
from app.Entities.Relacion import Relacion


class ConversorART:
    @staticmethod
    def transformar(json):
        dependencias = []
        atributos = []
        dependencias_funcionales = []

        if 'atributos' in json:
            atributos = json['atributos']
        if 'dependencias' in json:
            dependencias = json['dependencias']

        for dependencia in dependencias:
            if 'implicante' in dependencia and 'implicado' in dependencia:
                dependencia_funcional = DependenciaFuncional(dependencia['implicante'], dependencia['implicado'])
                dependencias_funcionales.append(dependencia_funcional)

        relacion = Relacion(atributos, dependencias_funcionales)
        return relacion
