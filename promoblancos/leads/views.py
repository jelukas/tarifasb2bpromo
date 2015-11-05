from django.shortcuts import render
from .forms import LeadForm
from django.views.generic.edit import FormView


class SolicitarView(FormView):
    template_name = 'leads/solicitar.html'
    form_class = LeadForm
    success_url = '/gracias/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super(SolicitarView, self).form_valid(form)


def inicio(request):
    return render(request, 'leads/inicio.html')


def gracias(request):
    return render(request, 'leads/gracias.html')
