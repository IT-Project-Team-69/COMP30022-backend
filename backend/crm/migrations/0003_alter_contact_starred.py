# Generated by Django 3.2 on 2021-09-03 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_auto_20210903_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='starred',
            field=models.BooleanField(default=False, verbose_name='Star'),
        ),
    ]