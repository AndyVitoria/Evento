from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from django.core.exceptions import ObjectDoesNotExist

from nested_admin.nested import NestedModelAdmin, NestedStackedInline, NestedTabularInline


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


class BannerInline(NestedStackedInline):
    model = Banner
    extra = 0


class NestedLoteInline(NestedTabularInline):
    model = Lote
    extra = 0


class NestedIngressoInline(NestedStackedInline):
    model = Ingresso
    inlines = [NestedLoteInline]
    extra = 0


class EventoAdmin(NestedModelAdmin):
    inlines = [
        NestedIngressoInline,
        BannerInline,
    ]
    filter_horizontal = ['id_categoria']
    exclude = ['id_promotor']

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Evento.objects.all()
        else:
            return Evento.objects.filter(id_promotor=request.user)

    def save_model(self, request, obj, form, change):
        try:
            if obj.id_promotor is None:
                obj.id_promotor = request.user
        except ObjectDoesNotExist:
            obj.id_promotor = request.user
        super().save_model(request, obj, form, change)

'''
class BannerInline(admin.StackedInline):
    model = Banner
    extra = 1

class EventoAdmin(admin.ModelAdmin):
    inlines = [
        BannerInline
    ]

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Evento.objects.all()
        else:
            return Evento.objects.filter(id_promotor=request.user)
'''


class EticketAdmin(admin.ModelAdmin):
    readonly_fields = ['qr_code', 'id_compra', 'id_ingresso', 'id_usuario', 'status']
    def get_queryset(self, request):
        if request.user.is_superuser:

            return Eticket.objects.all()
        else:
            return Eticket.objects.filter(id_usuario=request.user.id)


class FormaPagamentoAdmin(admin.ModelAdmin):
    pass


class CompraAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        if request.user.is_superuser:

            return Compra.objects.all()
        else:
            return Compra.objects.filter(id_user=request.user.id)


admin.site.register(Estado, EstadoAdmin)

admin.site.register(Municipio, MunicipioAdmin)

admin.site.register(Bairro, BairroAdmin)

admin.site.register(Logradouro, LogradouroAdmin)

admin.site.register(Endereco, EnderecoAdmin)

admin.site.register(Usuario, UsuarioAdmin)

admin.site.register(Carrinho, CarrinhoAdmin)

admin.site.register(CarrinhoIngresso, CarrinhoIngressoAdmin)

admin.site.register(Categoria, CategoriaAdmin)

admin.site.register(Evento, EventoAdmin)

#admin.site.register(Ingresso, IngressoAdmin)

#admin.site.register(Lote, LoteAdmin)

admin.site.register(Eticket, EticketAdmin)

admin.site.register(FormaPagamento, FormaPagamentoAdmin)

admin.site.register(Compra, CompraAdmin)