from .models import *
from django.forms import ModelForm, DateField, Form
from django import forms
from django.forms.widgets import DateInput, TimeInput, Textarea, TextInput, NumberInput, HiddenInput

class UserForm(ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'cpf',
            'data_nasc',
            'genero',
        ]

    def format(self):
        self.fields['password'].widget.input_type = 'password'
        self.fields['email'].widget.input_type = 'email'
        self.fields['data_nasc'].widget.input_type = 'date'


class EnderecoForm(Form):
    cep = forms.CharField(max_length=9, validators=[RegexValidator(regex='\d\d\d\d\d\-d\d\d')])
    logradouro = forms.CharField(max_length=200)
    numero = forms.IntegerField(min_value=0)
    complemento = forms.CharField(max_length=200)
    bairro = forms.CharField(max_length=200)
    cidade = forms.CharField(max_length=200)
    estado = forms.CharField(max_length=2)


class LoginForm(Form):
    user = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)


class EventoForm(ModelForm):
    class Meta:
        model = Evento
        fields = '__all__'
        exclude = ['status', 'id_promotor', 'data_hora_criacao', 'id_endereco', 'id_categoria']
        widgets = {
            'nome': TextInput(attrs={'id': 'evento#nome'}),
            'data_inicio_venda': DateInput(attrs={'class': 'datepicker', 'id': 'evento#data_inicio_venda'}),
            'data_fim_venda': DateInput(attrs={'class': 'datepicker', 'id': 'evento#data_fim_venda'}),
            'hora_inicio_venda': TimeInput(attrs={'class': 'timepicker', 'id': 'evento#hora_inicio_venda'}),
            'hora_fim_venda': TimeInput(attrs={'class': 'timepicker', 'id': 'evento#hora_fim_venda'}),
            'descricao': Textarea(attrs={'class': 'materialize-textarea', 'id': 'evento#descricao'}),
        }

    def format(self):
        #self.fields['data_inicio_venda'].widget.input_type = 'date'
        #self.fields['data_fim_venda'].widget.input_type = 'date'
        pass


class IngressoForm(ModelForm):
    class Meta:
        model = Ingresso
        fields = '__all__'
        exclude = ['id_evento']
        widgets = {
        'tipo': TextInput(attrs={'id': 'ingresso#tipo'})
        }


class LoteForm(ModelForm):
    class Meta:
        model = Lote
        fields = '__all__'
        exclude = ['qtd_vendido', 'id_ingresso']
        widgets = {
            'nome': TextInput(attrs={'id': 'lote#nome'}),
            'qtd_max': NumberInput(attrs={'id': 'lote#qtd_max'}),
            'data_inicio_venda': DateInput(attrs={'class': 'datepicker', 'id': 'lote#data_inicio_venda'}),
            'data_fim_venda': DateInput(attrs={'class': 'datepicker', 'id': 'lote#data_fim_venda'}),
        }

    def as_div(self):
        as_div = self.as_p()
        as_div.replace('p>', 'div>')
        return as_div


class EticketForm(ModelForm):
    id_ingresso = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Eticket
        fields = '__all__'
        exclude = ['id_compra', 'id_ingresso', 'status', 'qr_code', 'codigo']
        widgets = {
            'id_usuario': NumberInput(attrs={'type': 'hidden'})
        }