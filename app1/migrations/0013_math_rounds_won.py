# Generated by Django 4.0.1 on 2022-03-06 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_card_img_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='math',
            name='rounds_won',
            field=models.IntegerField(default=0, verbose_name='rounds ganhos.'),
            preserve_default=False,
        ),
    ]
