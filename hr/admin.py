from django.contrib import admin

# Register your models here.

from .models import CadEmpresa, CadServico, CadVeiculo

admin.site.register(CadEmpresa)
admin.site.register(CadServico)
admin.site.register(CadVeiculo)