# Generated by Django 3.0.6 on 2020-05-18 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20200516_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='country_wise',
            name='full_name',
            field=models.CharField(max_length=110, null=True),
        ),
    ]
