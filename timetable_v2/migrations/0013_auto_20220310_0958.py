# Generated by Django 3.2.9 on 2022-03-10 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0024_classtingurl'),
        ('timetable_v2', '0012_auto_20220309_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staticclass',
            name='name',
            field=models.CharField(max_length=12, verbose_name='수업 이름'),
        ),
        migrations.AlterField(
            model_name='timeclass',
            name='name',
            field=models.CharField(max_length=12, verbose_name='수업 이름'),
        ),
        migrations.AlterUniqueTogether(
            name='staticclass',
            unique_together={('name', 'teacher')},
        ),
    ]
