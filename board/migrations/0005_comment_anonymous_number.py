# Generated by Django 3.2.9 on 2021-12-30 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_auto_20211224_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='anonymous_number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]