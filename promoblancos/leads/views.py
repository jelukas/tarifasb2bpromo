from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt

from django.views.generic.edit import CreateView
from .models import Lead


class SolicitarView(CreateView):
    model = Lead
    fields = ['nombre', 'primer_apellido', 'segundo_apellido', 'email', 'codigo_postal', 'colectivo', 'acreditacion', ]

    template_name = 'leads/solicitar.html'
    success_url = '/gracias/'

    @method_decorator(xframe_options_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SolicitarView, self).dispatch(*args, **kwargs)


@xframe_options_exempt
def inicio(request):
    return render(request, 'leads/inicio.html')


@xframe_options_exempt
def gracias(request):
    return render(request, 'leads/gracias.html')
