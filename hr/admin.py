from django.contrib import admin

# Register your models here.

from .models import Cad_empresa, Cad_servico, Cad_veiculo, Person




admin.site.register(Cad_empresa)
admin.site.register(Cad_servico)
admin.site.register(Person)
admin.site.register(Cad_veiculo)