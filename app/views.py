import json
import os
import mimetypes
from django.views.generic import ListView
from django.views.generic.base import View
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.utils.encoding import smart_str
from django.conf import settings
from app.Entities.ConversorART import ConversorART
from app.Entities.ConversorATexto import ConversorATexto
from app.Entities.Archivo import Archivo


class IndexView(ListView):
    template_name = "index.html"
    queryset = 'AutomaticBD'
    context_object_name = 'projectName'


class FileView(View):

    @staticmethod
    def post(request, *args, **kwargs):
        print('POST in FileView')

        to_json = json.loads(request.body)
        filename = 'salida.json'
        full_path = smart_str(os.path.join(settings.BASE_DIR, filename))
        with open(filename, 'w+') as f:
            json.dump(to_json, f)

        with open(full_path, 'r') as f:
            data = f.read()

        response = HttpResponse(data, content_type=mimetypes.guess_type(full_path)[0])
        #response['Content-Type'] = 'application/force-download'
        response['Content-Disposition'] = "attachment; filename={0}".format(filename)
        response['Content-Length'] = os.path.getsize(full_path)
        #response['X-Sendfile'] = smart_str(os.path.join(settings.BASE_DIR, filename))

        print(full_path)
        print(os.path.getsize(full_path))
        print(mimetypes.guess_type(full_path))

        return response


class ServiceView(View):

    @staticmethod
    def get(request):
        print('GET in ServiceView')

        to_json = {
            "key1": "value1",
            "key2": "value2"
        }
        return JsonResponse(to_json)

    @staticmethod
    def post(request, *args, **kwargs):
        print('POST in ServiceView')

        separador = ', '

        conversor_art = ConversorART()
        conversor_texto = ConversorATexto()
        # print('Raw Data: "%s"' % request.META)
        to_json = json.loads(request.body)

        rt = conversor_art.transformar(to_json)

        variableInvalida = rt.validarVariables()

        if variableInvalida == True:
            archivo = Archivo('Recubrimiento.txt')
            archivo.escribir('RECUBRIMIENTO MÍNIMO\n')
            archivo.escribir('____________________\n\n')
            archivo.escribir('Modelo Original:\n')
            archivo.escribir('RT(t, l)=\n')
            archivo.escribir('\tt = [')
            archivo.escribir(separador.join(rt.t))
            archivo.escribir(']\n')
            archivo.escribir('\tl = [')
            archivo.escribir(separador.join(conversor_texto.transformarDependencias(rt.l)))
            archivo.escribir(']\n\n')

            l1 = rt.dependenciasElementales()
            texto_l1 = conversor_texto.transformarDependencias(l1)
            archivo.escribir('\tl1 = [')
            archivo.escribir(separador.join(texto_l1))
            archivo.escribir(']\n\n')

            l2 = rt.atributosExtranos()
            texto_l2 = conversor_texto.transformarDependencias(l2)
            archivo.escribir('\tl2 = [')
            archivo.escribir(separador.join(texto_l2))
            archivo.escribir(']\n\n')

            l3 = rt.dependenciasRedundantes()
            texto_l3 = conversor_texto.transformarDependencias(l3)
            archivo.escribir('\tl3 = [')
            archivo.escribir(separador.join(texto_l3))
            archivo.escribir(']\n\n')

            response = {
                'original' : to_json,
                'l1': [],
                'l2': [],
                'l3': [],
                'file': ''
            }

            full_path = smart_str(os.path.join(settings.BASE_DIR, 'Recubrimiento.txt'))

            with open(full_path, 'r') as f:
                response['file'] = f.read()

            for dependencia in l1:
                elem = {
                    'variablesImplicado': dependencia.variablesImplicado,
                    'variablesImplicante': dependencia.variablesImplicante
                }
                response['l1'].append(elem)

            for dependencia in l2:
                elem = {
                    'variablesImplicado': dependencia.variablesImplicado,
                    'variablesImplicante': dependencia.variablesImplicante
                }
                response['l2'].append(elem)

            for dependencia in l3:
                elem = {
                    'variablesImplicado': dependencia.variablesImplicado,
                    'variablesImplicante': dependencia.variablesImplicante
                }
                response['l3'].append(elem)

            return JsonResponse(response)

        return HttpResponseBadRequest('La variable "' + variableInvalida + '" no se encuentra definida')

        # response_json = json.dumps([ob.__dict__ for ob in l1], sort_keys=True)
        # return JsonResponse(response_json, safe=False)
