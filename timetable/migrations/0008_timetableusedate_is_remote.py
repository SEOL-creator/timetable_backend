# Generated by Django 3.2.9 on 2021-11-07 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0007_rename_timetable_timetableusedate_timetable'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetableusedate',
            name='is_remote',
            field=models.BooleanField(default=False),
        ),
    ]
