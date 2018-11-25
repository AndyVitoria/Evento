import os
from django.utils.text import slugify

from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone

def upload_to(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    return "media/{evento}/{filename}{extension}".format(
        evento=slugify(instance.id_evento.id),
        filename=slugify(filename_base),
        extension=filename_ext.lower(),
    )

# ========={ Endereço }========== #

class Estado(Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.get_address()

    def get_address(self):
        return self.nome


class Municipio(Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, blank=False)
    id_estado = models.ForeignKey('Estado', on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.get_address()

    def get_estado(self):
        return self.id_estado

    def get_address(self):
        return self.nome + ', ' + self.get_estado().get_address()


class Bairro(Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, blank=False)
    id_municipio = models.ForeignKey('Municipio', on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.get_address()

    def get_estado(self):
        return self.id_municipio.get_estado()

    def get_municipio(self):
        return self.id_municipio

    def get_address(self):
        return self.nome + ', ' + self.get_municipio().get_address()

class Logradouro(Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, blank=False)
    cep = models.CharField(max_length=8, blank=False, validators=[RegexValidator(regex='\d\d\d\d\d\d\d\d')])
    id_bairro = models.ForeignKey('Bairro', on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.get_address()

    def get_estado(self):
        return self.id_bairro.get_estado()

    def get_municipio(self):
        return self.id_bairro.get_municipio()

    def get_bairro(self):
        return self.id_bairro

    def get_address(self):
        return self.nome + ', ' + self.get_bairro().get_address()

class Endereco(Model):
    id = models.AutoField(primary_key=True)
    complemento = models.CharField(max_length=200, blank=True)
    numero = models.PositiveIntegerField(blank=True)
    id_logradouro = models.ForeignKey('Logradouro', on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.get_address()

    def get_estado(self):
        return self.id_logradouro.get_estado()

    def get_municipio(self):
        return self.id_logradouro.get_municipio()

    def get_bairro(self):
        return self.id_logradouro.get_bairro()

    def get_logradouro(self):
        return self.id_logradouro

    def get_address(self):
        if self.numero is not None:
            addr = self.get_logradouro().nome + ' ' + self.numero.__str__() + ', ' + self.get_bairro().get_address()
        else:
            addr = self.get_logradouro().get_address()
        return addr

    def get_endereco_abreviado(self):
        return self.get_municipio().nome + '/' + self.get_estado().nome


# =============={ Usuários }=============#
class Usuario(User):
    cpf = models.CharField(max_length=11,blank=False, validators=[RegexValidator(regex='[\d]+')]) # Verificar se é possivel usar o Regex
    data_nasc = models.DateField(verbose_name='Data de Nascimento', blank=False)
    genero = models.CharField(max_length=5, blank=False, choices=(('M', 'Masculino'), ('F', 'Feminino')))
    id_endereco = models.ForeignKey('Endereco', on_delete=models.CASCADE, blank=True)


class Carrinho(Model):
    id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('Usuario', blank=False, on_delete=models.CASCADE)
    ingressos = models.ManyToManyField('Lote', through='CarrinhoIngresso')
    status = models.BooleanField(default=True)

    def calcular_total(self):
        carrinho_list = CarrinhoIngresso.objects.filter(id_carrinho=self.id)
        total = 0
        for carrinho_item in carrinho_list:
            total += carrinho_item.total()
        return total


class CarrinhoIngresso(Model):
    id = models.AutoField(primary_key=True)
    id_carrinho = models.ForeignKey('Carrinho', on_delete=models.CASCADE, blank=False)
    id_lote = models.ForeignKey('Lote', on_delete=models.CASCADE, blank=False)
    qtd_ingresso = models.PositiveIntegerField(blank=False, validators=[MinValueValidator(1)])

    def total(self):
        return self.id_lote.valor * self.qtd_ingresso


# ============={ Eventos }===============#
class Categoria(Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.nome


class Banner(Model):
    id = models.AutoField(primary_key=True)
    # image_url = models.ImageField(upload_to='media/', default='media/no-img.png')
    image_url = models.ImageField(upload_to=upload_to, default='media/no-img.png')
    id_evento = models.ForeignKey('Evento', on_delete=models.CASCADE, blank=False)


"""
    Status Evento:
    E - Em Análise
    A - Aprovado
    R - Reprovado
    O - Ocorrendo
    F - Finalizado
"""
class Evento(Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(default='E', max_length=1, editable=False)
    id_promotor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    id_categoria = models.ManyToManyField('Categoria',blank=False, verbose_name='Categorias')
    nome = models.CharField(max_length=200, blank=False)
    descricao = models.TextField(blank=False, verbose_name='Descrição')
    id_endereco = models.ForeignKey('Endereco', on_delete=models.CASCADE, blank=True, verbose_name='Endereço')
    data_hora_criacao = models.DateTimeField(auto_now_add=True, editable=False)
    data_inicio_venda = models.DateField(blank=False, verbose_name='Inicio das vendas', default=timezone.now())
    hora_inicio_venda = models.TimeField(blank=False, verbose_name='Inicio das vendas', default=timezone.now())
    data_fim_venda = models.DateField(blank=False, verbose_name='Fim das vendas', default=timezone.now())
    hora_fim_venda = models.TimeField(blank=False, verbose_name='Fim das vendas', default=timezone.now())

    def __str__(self):
        return self.nome

    def get_ingresso(self):
        return Ingresso.objects.filter(id_evento=self.id)

    def get_banners(self):
        return Banner.objects.filter(id_evento=self.id)

    def get_categoria(self):
        return self.id_categoria


class Ingresso(Model):
    id = models.AutoField(primary_key=True)
    id_evento = models.ForeignKey('Evento', on_delete=models.CASCADE, blank=False)
    tipo = models.CharField(max_length=200, blank=False, verbose_name='Tipo de ingresso')

    def __str__(self):
        return self.id_evento.nome + ' - ' + self.tipo

    def get_meta_nome(self):
        lote = self.get_lote()
        if lote is None:
            return self.__str__() + ' - ESGOTADO'
        return self.__str__() + ' - ' + lote.nome

    def get_lote(self):
        lote_list = Lote.objects.filter(id_ingresso=self.id).order_by('nome')
        for lote in lote_list:
            if lote.status():
                return lote
        return None


class Lote(Model):
    id = models.AutoField(primary_key=True)
    id_ingresso = models.ForeignKey('Ingresso', on_delete=models.CASCADE, blank=False)
    nome = models.CharField(max_length=200, verbose_name='Nome do Lote')
    valor = models.FloatField(blank=False, validators=[MinValueValidator(0.0)]) # Adicionar verificação de valor negativo
    qtd_max = models.PositiveIntegerField(blank=False, verbose_name='Quantidade')
    data_inicio_venda = models.DateField(blank=False, verbose_name='Inicio das vendas', default=timezone.now())
    hora_inicio_venda = models.TimeField(blank=False, verbose_name='Inicio das vendas', default=timezone.now())
    data_fim_venda = models.DateField(blank=False, verbose_name='Fim das vendas', default=timezone.now())
    hora_fim_venda = models.TimeField(blank=False, verbose_name='Fim das vendas', default=timezone.now())
    qtd_vendido = models.PositiveIntegerField(blank=False, default=0)

    def __str__(self):
        return self.id_ingresso.id_evento.__str__() + ' | ' + self.id_ingresso.__str__() + ' - ' + self.nome

    def status(self):
        return self.qtd_vendido < self.qtd_max

# Revisar com a Ju e o Caio
class Eticket(Model):
    id = models.AutoField(primary_key=True)
    cpf = models.CharField(max_length=11, blank=False, validators=[RegexValidator(regex='[\d]+')])
    status = models.BooleanField(default=True)
    nome = models.CharField(max_length=200, blank=False)
    codigo = models.TextField(blank=False)
    id_usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, blank=False)
    id_ingresso = models.ForeignKey('Ingresso', on_delete=models.CASCADE, blank=False)
    id_compra = models.ForeignKey('Compra', on_delete=models.CASCADE, blank=False)
    qr_code = models.ImageField(upload_to='qr_code/', default='media/no-img.png')


# ============{ Pagamento }===========
class FormaPagamento(Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.nome

"""
    Status da Compra:
    A - Aguardando Pagamento
    P - Pagamento Efetuado com Sucesso
    N - Pagamento Não Efetuado
"""
class Compra(Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(default='A', max_length=1)
    data_compra = models.DateTimeField(blank=False)
    data_pagamento = models.DateTimeField()
    id_carrinho = models.ForeignKey('Carrinho', on_delete=models.CASCADE, blank=False)
    id_forma_pagamento = models.ForeignKey('FormaPagamento', on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.id_carrinho.id_user.__str__() + ' - ' + self.data_compra.__str__()

    def get_forma_pagamento(self):
        return self.id_forma_pagamento

    # A implementar
    def gerar_eticket(self):
        pass
