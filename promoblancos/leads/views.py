from django.shortcuts import render


def inicio(request):
    return render(request, 'leads/inicio.html')


def gracias(request):
    return render(request, 'leads/gracias.html')
