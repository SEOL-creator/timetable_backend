# Generated by Django 3.2.9 on 2021-12-19 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='frontversion',
            name='note',
            field=models.TextField(blank=True),
        ),
    ]
