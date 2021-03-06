# Generated by Django 4.0.1 on 2022-02-12 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_alter_dailyfreeticket_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='Math',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prize', models.IntegerField(verbose_name='premio')),
                ('date', models.DateField(verbose_name='data')),
                ('active_round', models.DateTimeField(verbose_name='round ativo')),
                ('is_win', models.BooleanField(default=False, verbose_name='ganhou')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maths', to='app1.account', verbose_name='conta')),
            ],
            options={
                'verbose_name': 'partida',
                'verbose_name_plural': 'partidas',
            },
        ),
        migrations.CreateModel(
            name='Hand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.IntegerField()),
                ('total_point', models.IntegerField(verbose_name='pontos')),
                ('is_out', models.BooleanField(verbose_name='bateu')),
                ('is_player_hand', models.BooleanField(verbose_name='jogador')),
                ('math', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rounds', to='app1.math', verbose_name='partida')),
            ],
            options={
                'verbose_name': 'mao',
                'verbose_name_plural': 'maos',
            },
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(verbose_name='valor')),
                ('position', models.IntegerField(verbose_name='posicao')),
                ('hand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='app1.hand', verbose_name='mao')),
            ],
            options={
                'verbose_name': 'mao',
                'verbose_name_plural': 'maos',
            },
        ),
    ]
