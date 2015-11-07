from django import forms
from .models import Lead


class LeadForm(forms.ModelForm):
    # colectivo = forms.ChoiceField(widget=forms.RadioSelect())

    class Meta:
        model = Lead
        fields = ('nombre', 'primer_apellido', 'segundo_apellido', 'email', 'codigo_postal', 'colectivo', 'acreditacion')
