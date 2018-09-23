# Generated by Django 2.1.1 on 2018-09-21 11:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('E_Vento', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrinho',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarrinhoIngresso',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('qtd_ingresso', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('id_carrinho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='E_Vento.Carrinho')),
            ],
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=False)),
                ('data_compra', models.DateTimeField()),
                ('data_pagamento', models.DateTimeField()),
                ('id_carrinho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='E_Vento.Carrinho')),
            ],
        ),
        migrations.CreateModel(
            name='Eticket',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cpf', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(regex='[\\d]+')])),
                ('status', models.BooleanField(default=True)),
                ('nome', models.CharField(max_length=200)),
                ('codigo', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='FormaPagamento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Ingresso',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Lote',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('valor', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('qtd_max', models.PositiveIntegerField()),
                ('id_ingresso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='E_Vento.Ingresso')),
            ],
        ),
        migrations.AddField(
            model_name='evento',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='cpf',
            field=models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(regex='[\\d]+')]),
        ),
        migrations.AddField(
            model_name='ingresso',
            name='id_evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='E_Vento.Evento'),
        ),
        migrations.AddField(
            model_name='compra',
            name='id_forma_pagamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='E_Vento.FormaPagamento'),
        ),
        migrations.AddField(
            model_name='carrinhoingresso',
            name='id_ingresso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='E_Vento.Ingresso'),
        ),
        migrations.AddField(
            model_name='carrinho',
            name='id_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='E_Vento.Usuario'),
        ),
        migrations.AddField(
            model_name='carrinho',
            name='ingressos',
            field=models.ManyToManyField(through='E_Vento.CarrinhoIngresso', to='E_Vento.Ingresso'),
        ),
    ]