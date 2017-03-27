from app.Entities.DependenciaFuncional import DependenciaFuncional
from app.Entities.RT import RT


class ConversorART:
    def transformar(self, j):
        dependencias = []
        atributos = []
        dependenciasFuncionales = []

        if 't' in j:
            atributos = j['t']
        elif 'atributos' in j:
            atributos = j['atributos']
        if 'l' in j:
            dependencias = j['l']
        elif 'dependencias' in j:
            dependencias = j['dependencias']

        for dependencia in dependencias:
            if 'implicante' in dependencia and 'implicado' in dependencia:
                dependenciaFuncional = DependenciaFuncional(dependencia['implicante'], dependencia['implicado'])
                dependenciasFuncionales.append(dependenciaFuncional)

        rt = RT(atributos, dependenciasFuncionales)
        return rt
