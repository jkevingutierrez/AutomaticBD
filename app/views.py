import json
import mimetypes
import os

from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.utils.encoding import smart_str
from django.views.generic import ListView
from django.views.generic.base import View

from app.Entities.AlgoritmoLlaves import AlgoritmoLlaves
from app.Entities.Archivo import Archivo
from app.Entities.Cierre import Cierre
from app.Entities.ConversorART import ConversorART
from app.Entities.ConversorATexto import ConversorATexto
from app.Entities.RecubrimientoMinimo import RecubrimientoMinimo


class NotFoundView(ListView):
    template_name = "404.html"
    queryset = 'AutomaticBD'
    context_object_name = 'projectName'


class IndexView(ListView):
    template_name = "index.html"
    queryset = 'AutomaticBD'
    context_object_name = 'projectName'


class FileView(View):
    @staticmethod
    def post(request):
        print('POST in FileView')

        to_json = json.loads(request.body.decode("utf-8"))

        filename = 'salida.json'
        full_path = smart_str(os.path.join(settings.BASE_DIR, filename))
        with open(full_path, 'w+') as f:
            json.dump(to_json, f)

        with open(full_path, 'r') as f:
            data = f.read()

        response = HttpResponse(data)
        # response['Content-Type'] = 'application/force-download'
        response['Content-Type'] = 'application/json'
        response['Content-Disposition'] = "attachment; filename={0}".format(filename)
        response['Content-Length'] = os.path.getsize(full_path)
        # response['X-Sendfile'] = smart_str(os.path.join(settings.BASE_DIR, filename))

        print('Full File Path:', full_path)
        print('File Size:', os.path.getsize(full_path))
        print('File Mimetypes:', mimetypes.guess_type(full_path))

        return response


class ServiceView(View):
    @staticmethod
    def post(request):
        print('POST in ServiceView')

        separador = ', '

        to_json = json.loads(request.body.decode("utf-8"))

        relacion = ConversorART.transformar(to_json)

        atributos_validos = relacion.validar_atributos()

        if atributos_validos is True:
            archivo = Archivo('Salida.txt')
            archivo.escribir('RECUBRIMIENTO M\u00CDNIMO\n')
            archivo.escribir('____________________\n\n')
            archivo.escribir('Modelo Original:\n')
            archivo.escribir('RT(t, l)=\n')
            archivo.escribir('\tt = [')
            archivo.escribir(separador.join(relacion.atributos))
            archivo.escribir(']\n')
            archivo.escribir('\tl = [')
            archivo.escribir(separador.join(ConversorATexto.transformar_dependencias(relacion.dependencias)))
            archivo.escribir(']\n\n')

            l1 = RecubrimientoMinimo.dependencias_elementales(relacion.dependencias)
            texto_l1 = ConversorATexto.transformar_dependencias(l1)
            archivo.escribir('\tl1 = [')
            archivo.escribir(separador.join(texto_l1))
            archivo.escribir(']\n\n')

            l2 = RecubrimientoMinimo.atributos_extranos(l1)
            texto_l2 = ConversorATexto.transformar_dependencias(l2)
            archivo.escribir('\tl2 = [')
            archivo.escribir(separador.join(texto_l2))
            archivo.escribir(']\n\n')

            l3 = RecubrimientoMinimo.dependencias_redundantes(l2)
            texto_l3 = ConversorATexto.transformar_dependencias(l3)
            archivo.escribir('\tl3 = [')
            archivo.escribir(separador.join(texto_l3))
            archivo.escribir(']\n\n')

            archivo.escribir('RecubrimientoMinimo = [')
            archivo.escribir(separador.join(texto_l3))
            archivo.escribir(']\n\n')

            relacion_recubrimiento = relacion
            relacion_recubrimiento.dependencias = l3

            archivo.escribir('\n\nCALCULO DE LLAVES\n')
            archivo.escribir('____________________\n\n')

            z = AlgoritmoLlaves.calcular_z(relacion_recubrimiento)
            cierre_z = Cierre.calcular_cierre(z, relacion.dependencias, 'Z')

            if AlgoritmoLlaves.validar_cierre_z(relacion_recubrimiento, cierre_z):
                llaves = z
            else:
                w = AlgoritmoLlaves.calcular_w(relacion_recubrimiento)
                v = AlgoritmoLlaves.calcular_v(relacion_recubrimiento, cierre_z, w)
                llaves = AlgoritmoLlaves.iterar(v, z, relacion)

            archivo.escribir('\nLlavesCandidatas = ')
            archivo.escribir(ConversorATexto.transformar_llaves(llaves))

            response = {
                'original': to_json,
                'l1': [],
                'l2': [],
                'l3': [],
                'file': '',
                'keys': llaves
            }

            full_path = smart_str(os.path.join(settings.BASE_DIR, 'Salida.txt'))

            with open(full_path, 'r') as f:
                response['file'] = f.read()

            for dependencia in l1:
                elem = {
                    'implicante': dependencia.implicante,
                    'implicado': dependencia.implicado
                }
                response['l1'].append(elem)

            for dependencia in l2:
                elem = {
                    'implicante': dependencia.implicante,
                    'implicado': dependencia.implicado
                }
                response['l2'].append(elem)

            for dependencia in l3:
                elem = {
                    'implicante': dependencia.implicante,
                    'implicado': dependencia.implicado
                }
                response['l3'].append(elem)

            print("Recubrimiento Minimo:")
            print(response["l3"])

            print("Llaves Candidatas:")
            print(response["keys"])

            return JsonResponse(response)

        return HttpResponseBadRequest('El atributo "' + atributos_validos + '" no se encuentra definido')

        # response_json = json.dumps([ob.__dict__ for ob in l1], sort_keys=True)
        # return JsonResponse(response_json, safe=False)
