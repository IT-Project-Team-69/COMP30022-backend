# Generated by Django 3.2.6 on 2021-09-27 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0009_userprofilefield'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofilefield',
            old_name='name',
            new_name='label',
        ),
    ]
