from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from .forms import UserForm, EnderecoForm
from .models import Evento, Lote, Usuario, Carrinho, CarrinhoIngresso
import json
from django.core import serializers
from EVento.settings import ALLOWED_HOSTS

# Create your views here.
def home(request):
    temp = loader.get_template('evento_site/pages/home.html')
    return HttpResponse(temp.render({}, request))


def criar_conta(request):
    msg = ''
    # Carregamento do template
    temp = loader.get_template('evento_site/pages/user_register.html')

    if request.method == 'POST':
        post = request.POST
        user_forms = UserForm(post)
        if user_forms.is_valid():
            user_forms.save()
            user_forms = UserForm()
            user_forms.format()
        else:
            msg = user_forms.errors
        None -1
    else:
        user_forms = UserForm()
        user_forms.format()

    end_forms = EnderecoForm()
    test = json.dumps({1:1,2:2})
    return HttpResponse(temp.render({
        'message': msg,
        'user_forms': user_forms,
        'endereco_forms': end_forms,
        'test': test
        }, request))


def build_evento(evento):
    evento_serialized = json.loads(serializers.serialize('json', [evento, ], fields=(
    'status', 'nome', 'banner', 'descricao', 'data_inicio', 'data_fim',)))
    temp_evento_dict = evento_serialized[0]['fields']
    temp_evento_dict['id'] = evento_serialized[0]['pk']
    temp_evento_dict['categoria'] = evento.id_categoria.nome
    return temp_evento_dict


def build_promotor(evento):
    temp_promotor_evento_dict = dict()
    temp_promotor_evento_dict['id'] = evento.id_promotor.id
    temp_promotor_evento_dict['nome'] = evento.id_promotor.first_name + ' ' + evento.id_promotor.last_name
    return temp_promotor_evento_dict


def build_endereco(evento):
    temp_local_evento_dict = dict()
    temp_local_evento_dict["complemento"] = evento.id_endereco.complemento
    temp_local_evento_dict["numero"] = evento.id_endereco.numero
    temp_local_evento_dict["logradouro"] = evento.id_endereco.id_logradouro.nome
    temp_local_evento_dict["bairro"] = evento.id_endereco.id_logradouro.id_bairro.nome
    temp_local_evento_dict["cidade"] = evento.id_endereco.id_logradouro.id_bairro.id_municipio.nome
    temp_local_evento_dict["estado"] = evento.id_endereco.id_logradouro.id_bairro.id_municipio.id_estado.nome
    return temp_local_evento_dict


def build_preco_evento(evento):
    return dict()


def build_evento_list(eventos):
    evento_list = list()
    count = 0
    for evento in eventos:
        evento_dict = dict()

        evento_dict['page'] ='evento/' + str(evento.id)

        # Recuperando informações sobre o evento e inserindo-as em um dicionario
        evento_dict['evento'] = build_evento(evento)

        # Recuperando informações sobre o promotor do evento e inserindo-as em um dicionario
        evento_dict['promotor'] = build_promotor(evento)

        # Recuperando informações sobre o local do evento e inserindo-as em um dicionario
        evento_dict['endereco'] = build_endereco(evento)

        # Recuperando informação sobre o igresso de menor valor
        evento_dict['ingresso'] = build_preco_evento(evento)

        evento_list.append(evento_dict)
    return {'value': evento_list}


def build_evento_json(eventos):
    evento_list = build_evento_list(eventos)
    return json.dumps(evento_list)


def get_eventos(request):
    evento_json = ''
    if request.method == 'GET':
        interval = 20
        id_get = int(request.GET['id'])
        eventos = Evento.objects.filter(status=True)[interval * id_get: (id_get+1) * interval]

        evento_json = build_evento_list(eventos)

    return JsonResponse(evento_json)


def get_evento(requets, id):
    if requets.method == "GET":
        try:
            evento = Evento.objects.get(pk=id)
            temp = loader.get_template('evento_site/pages/evento.html')
            return HttpResponse(temp.render({'evento': evento}, requets))
        except:
            return home(requets)
    elif requets.method == "POST":
        post = requets.POST
        ingresso_list = sorted(post.keys())[:-1]
        user = Usuario.objects.first()
        for meta in ingresso_list:
            if int(post[meta]) > 0:
                id_ingresso, id_lote = meta.split('-')
                lote = Lote.objects.filter(id=id_lote, id_ingresso=id_ingresso).first()
                if lote is not None:
                    carrinho = Carrinho.objects.filter(id_user=user.id, status=True)
                    if len(carrinho) == 0:
                        carrinho = Carrinho(id_user=user, status=True)
                        carrinho.save()
                    else:
                        carrinho = carrinho[0]
                    CarrinhoIngresso(id_lote=lote, id_carrinho=carrinho, qtd_ingresso=int(post[meta])).save()
        requets.method = "GET"
        return redirect(get_carrinho)


def get_carrinho(request):
    if request.method == "GET" or request.method == "DELETE":
        if 'DELETE' in request.GET.keys(): #request.method == 'DELETE':
            id = request.GET['id']
            carrinho = CarrinhoIngresso.objects.filter(id=id).first()
            if carrinho is not None:
                carrinho.delete()

        user = Usuario.objects.first()
        carrinho = Carrinho.objects.filter(id_user=user.id, status=True).first()
        if carrinho is None:
            carrinho = Carrinho(id_user=user.id, status=True)
            carrinho.save()
        carrinho_ingresso = CarrinhoIngresso.objects.filter(id_carrinho=carrinho.id)
        temp = loader.get_template('evento_site/pages/carrinho.html')
        return HttpResponse(temp.render({'carrinho': carrinho, 'carrinho_ingresso': carrinho_ingresso}))
