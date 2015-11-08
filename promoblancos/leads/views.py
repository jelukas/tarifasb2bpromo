from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Lead


class SolicitarView(CreateView):
    model = Lead
    fields = ['nombre', 'primer_apellido', 'segundo_apellido', 'email', 'codigo_postal', 'colectivo', 'acreditacion', ]

    template_name = 'leads/solicitar.html'
    success_url = '/gracias/'


def inicio(request):
    return render(request, 'leads/inicio.html')


def gracias(request):
    return render(request, 'leads/gracias.html')
