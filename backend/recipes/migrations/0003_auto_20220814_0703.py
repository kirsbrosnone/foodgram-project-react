# Generated by Django 2.2.16 on 2022-08-14 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20220813_1435'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favouriterecipe',
            options={'verbose_name': 'Избранное', 'verbose_name_plural': 'Избранное'},
        ),
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'verbose_name': 'Корзина', 'verbose_name_plural': 'Корзина'},
        ),
    ]