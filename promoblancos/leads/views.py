from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView
from .models import Lead


class SolicitarView(CreateView):
    model = Lead
    fields = ['nombre', 'primer_apellido', 'segundo_apellido', 'email', 'codigo_postal', 'colectivo', ]

    template_name = 'leads/solicitar.html'
    success_url = '/ultimo-paso/'

    @method_decorator(xframe_options_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SolicitarView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        self.object.enviar_email_inicial()
        return reverse('segundo_paso', kwargs={'pk': self.object.id})


class SegundoPasoView(UpdateView):
    model = Lead
    fields = ['acreditacion', ]

    template_name = 'leads/segundo_paso.html'
    success_url = '/gracias/'

    @method_decorator(xframe_options_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SegundoPasoView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        self.object.enviar_email_inicial()
        return super(SegundoPasoView, self).get_success_url()


@xframe_options_exempt
def inicio(request):
    return render(request, 'leads/inicio.html')


@xframe_options_exempt
def gracias(request):
    return render(request, 'leads/gracias.html')
