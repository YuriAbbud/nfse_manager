from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Cliente, NotaFiscal


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf_cnpj', 'email', 'criado_em']
    search_fields = ['nome', 'cpf_cnpj', 'email']


@admin.register(NotaFiscal)
class NotaFiscalAdmin(admin.ModelAdmin):
    list_display = ['pk', 'cliente', 'valor_bruto', 'valor_iss', 'emitida_em']
    search_fields = ['cliente__nome']