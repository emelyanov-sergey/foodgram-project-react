# Generated by Django 3.2 on 2023-08-03 22:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Inredient',
            new_name='Ingredient',
        ),
    ]