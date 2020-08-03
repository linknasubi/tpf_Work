from django import forms
from .models import Person, Cad_servico, Cad_veiculo

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('cad_empresa', 'cad_servico', 'cad_veiculo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['cad_servico'].queryset = Cad_servico.objects.none()

        

        if 'cad_empresa' in self.data:
            try: 
                cad_empresa_id = int(self.data.get('cad_empresa'))
                self.fields['cad_servico'].queryset = Cad_servico.objects.filter(cad_empresa_id=cad_empresa_id).order_by('nome')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['cad_servico'].queryset = self.instance.cad_empresa.cad_servico_set.order_by('nome')

        self.fields['cad_veiculo'].queryset = Cad_servico.objects.none()
        if 'cad_servico' in self.data:
            try:
                cad_servico_id = int(self.data.get('cad_servico'))
                self.fields['cad_veiculo'].queryset = Cad_veiculo.objects.filter(cad_servico_id=cad_servico_id).order_by('nome')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['cad_veiculo'].queryset = self.instance.cad_empresa.cad_servico.cad_veiculo_set.order_by('nome')