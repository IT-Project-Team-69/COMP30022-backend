# Generated by Django 3.2 on 2021-10-09 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0014_auto_20211002_0042'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='groupOwner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.userprofile'),
        ),
    ]
