from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator


# ========={ Endereço }========== #

class Estado(Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, blank=False)


class Municipio(Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, blank=False)
    id_estado = models.ForeignKey('Estado', on_delete=models.CASCADE, blank=False)


class Bairro(Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, blank=False)
    id_municipio = models.ForeignKey('Municipio', on_delete=models.CASCADE, blank=False)


class Logradouro(Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, blank=False)
    id_bairro = models.ForeignKey('Bairro', on_delete=models.CASCADE, blank=False)


class Endereco(Model):
    id = models.AutoField(primary_key=True)
    complemento = models.CharField(max_length=200, blank=True)
    numero = models.PositiveIntegerField(blank=True)
    id_logradouro = models.ForeignKey('Logradouro', on_delete=models.CASCADE, blank=False)


# =============={ Usuários }=============#
class Usuario(User):
    cpf = models.CharField(max_length=11 ,blank=False,validators=[RegexValidator(regex='[\d]+')]) # Verificar se é possivel usar o Regex
    data_nasc = models.DateField(verbose_name='Data de Nascimento', blank=False)
    genero = models.CharField(max_length=5, blank=False, choices=(('M', 'Masculino'), ('F', 'Feminino')))
    id_endereco = models.ForeignKey('Endereco', on_delete=models.CASCADE, blank=False)


class Carrinho(Model):
    id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('Usuario', blank=False, on_delete=models.CASCADE)
    ingressos = models.ManyToManyField('Ingresso', through='CarrinhoIngresso')
    status = models.BooleanField(default=True)


class CarrinhoIngresso(Model):
    id = models.AutoField(primary_key=True)
    id_carrinho = models.ForeignKey('Carrinho', on_delete=models.CASCADE, blank=False)
    id_ingresso = models.ForeignKey('Ingresso',on_delete=models.CASCADE, blank=False)
    qtd_ingresso = models.PositiveIntegerField(blank=False, validators=[MinValueValidator(1)])


# ============={ Eventos }===============#
class Categoria(Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, blank=False)


class Evento(Model):
    id = models.AutoField(primary_key=True)
    status = models.BooleanField(default=True)
    id_promotor = models.ForeignKey('Usuario', on_delete=models.CASCADE, blank=False)
    id_categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE,blank=False)
    nome = models.CharField(max_length=200, blank=False)
    descricao = models.TextField(blank=False)
    banner = models.FilePathField(blank=False,path=settings.FILE_PATH_FIELD_DIRECTORY) # VERIFICAR O PATH
    id_endereco = models.ForeignKey('Endereco', on_delete=models.CASCADE, blank=False)
    data_cadastro = models.DateTimeField(blank=False)
    data_inicio = models.DateTimeField(blank=False)
    data_fim = models.DateTimeField(blank=False)


class Ingresso(Model):
    id = models.AutoField(primary_key=True)
    id_evento = models.ForeignKey('Evento', on_delete=models.CASCADE, blank=False)
    tipo = models.CharField(max_length=200, blank=False)


class Lote(Model):
    id = models.AutoField(primary_key=True)
    id_ingresso = models.ForeignKey('Ingresso', on_delete=models.CASCADE, blank=False)
    nome = models.CharField(max_length=200)
    valor = models.FloatField(blank=False, validators=[MinValueValidator(0.0)]) # Adicionar verificação de valor negativo
    qtd_max = models.PositiveIntegerField(blank=False)

# Revisar com a Ju e o Caio
class Eticket(Model):
    id = models.AutoField(primary_key=True)
    cpf = models.CharField(max_length=11, blank=False, validators=[RegexValidator(regex='[\d]+')])
    status = models.BooleanField(default=True)
    nome = models.CharField(max_length=200, blank=False)
    codigo = models.TextField(blank=False)


# ============{ Pagamento }===========
class FormaPagamento(Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, blank=False)


class Compra(Model):
    id = models.AutoField(primary_key=True)
    status = models.BooleanField(default=False)
    data_compra = models.DateTimeField(blank=False)
    data_pagamento = models.DateTimeField()
    id_carrinho = models.ForeignKey('Carrinho', on_delete=models.CASCADE, blank=False)
    id_forma_pagamento = models.ForeignKey('FormaPagamento', on_delete=models.CASCADE, blank=False)