from django.contrib import admin
from .models import *


class EstadoAdmin(admin.ModelAdmin):
    pass


class MunicipioAdmin(admin.ModelAdmin):
    pass


class BairroAdmin(admin.ModelAdmin):
    pass


class LogradouroAdmin(admin.ModelAdmin):
    pass


class EnderecoAdmin(admin.ModelAdmin):
    pass


class UsuarioAdmin(admin.ModelAdmin):
    pass


class CarrinhoAdmin(admin.ModelAdmin):
    pass


class CarrinhoIngressoAdmin(admin.ModelAdmin):
    pass


class CategoriaAdmin(admin.ModelAdmin):
    pass


class LoteInline(admin.TabularInline):
    model = Lote
    extra = 0


class IngressoInline(admin.TabularInline):
    extra = 0


class IngressoAdmin(admin.ModelAdmin):
    inlines = [
        LoteInline,
    ]


class EventoAdmin(admin.ModelAdmin):
    pass


class EticketAdmin(admin.ModelAdmin):
    pass


class FormaPagamentoAdmin(admin.ModelAdmin):
    pass


class CompraAdmin(admin.ModelAdmin):
    pass



admin.site.register(Estado, EstadoAdmin)

admin.site.register(Municipio, MunicipioAdmin)

admin.site.register(Bairro, BairroAdmin)

admin.site.register(Logradouro, LogradouroAdmin)

admin.site.register(Endereco, EnderecoAdmin)

#admin.site.register(Usuario, UsuarioAdmin)

admin.site.register(Carrinho, CarrinhoAdmin)

admin.site.register(CarrinhoIngresso, CarrinhoIngressoAdmin)

admin.site.register(Categoria, CategoriaAdmin)

admin.site.register(Evento, EventoAdmin)

admin.site.register(Ingresso, IngressoAdmin)

#admin.site.register(Lote, LoteAdmin)

admin.site.register(Eticket, EticketAdmin)

admin.site.register(FormaPagamento, FormaPagamentoAdmin)

admin.site.register(Compra, CompraAdmin)

