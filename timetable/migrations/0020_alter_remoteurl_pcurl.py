# Generated by Django 3.2.9 on 2021-11-15 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0019_rename_url_remoteurl_pcurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remoteurl',
            name='pcurl',
            field=models.CharField(max_length=600, verbose_name='PCURL'),
        ),
    ]
