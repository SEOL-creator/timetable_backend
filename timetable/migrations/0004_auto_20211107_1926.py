# Generated by Django 3.2.9 on 2021-11-07 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0003_rename_teachers_class_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='name',
            field=models.CharField(max_length=12, unique=True, verbose_name='수업 이름'),
        ),
        migrations.CreateModel(
            name='RemoteURL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='URL')),
                ('_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.class', verbose_name='수업')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.classroom', verbose_name='학급')),
            ],
        ),
    ]
