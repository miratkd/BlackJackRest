# Generated by Django 4.0.2 on 2022-04-10 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_alter_math_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='math',
            name='active_round',
        ),
        migrations.AddField(
            model_name='card',
            name='img_url',
            field=models.CharField(default='123', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hand',
            name='is_hold',
            field=models.BooleanField(default=False, verbose_name='parou'),
        ),
        migrations.AddField(
            model_name='math',
            name='is_over',
            field=models.BooleanField(default=False, verbose_name='partida finalizada'),
        ),
        migrations.AddField(
            model_name='math',
            name='math_active_round',
            field=models.IntegerField(default=1, verbose_name='round ativo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='math',
            name='rounds_won',
            field=models.IntegerField(default=0, verbose_name='rounds ganhos.'),
            preserve_default=False,
        ),
    ]