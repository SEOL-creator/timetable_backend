# Generated by Django 3.2.9 on 2022-03-05 01:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable_v2', '0009_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='color',
            old_name='color_code_hex',
            new_name='color',
        ),
    ]
