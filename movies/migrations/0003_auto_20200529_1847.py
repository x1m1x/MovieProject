# Generated by Django 3.0.5 on 2020-05-29 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20200527_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='draft',
            field=models.BooleanField(default=False, verbose_name='Черновик'),
        ),
    ]