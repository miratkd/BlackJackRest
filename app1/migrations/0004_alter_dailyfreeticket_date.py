# Generated by Django 4.0.1 on 2022-02-09 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_alter_dailyfreeticket_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyfreeticket',
            name='date',
            field=models.DateField(),
        ),
    ]
