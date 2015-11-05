from django.shortcuts import render
from .models import Lead
from .forms import LeadForm


def inicio(request):
    return render(request, 'leads/inicio.html')


def solicitar(request):
    lead_form = LeadForm()
    context = {"lead_form": lead_form}
    return render(request, 'leads/solicitar.html', context)


def gracias(request):
    return render(request, 'leads/gracias.html')
