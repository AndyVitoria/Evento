from .models import *
from django.forms import ModelForm, DateField, Form
from django import forms

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


class EnderecoForm(ModelForm):
    class Meta:
        model = Endereco
        fields = '__all__'


class LoginForm(Form):
    user = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)


class EventoForm(ModelForm):
    class Meta:
        model = Evento
        fields = '__all__'
        exclude = ['status', 'id_promotor', 'data_hora_criacao', 'id_endereco']

    def format(self):
        self.fields['data_inicio_venda'].widget.input_type = 'date'
        self.fields['data_fim_venda'].widget.input_type = 'date'