from .models import *
from django.forms import ModelForm, DateField


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