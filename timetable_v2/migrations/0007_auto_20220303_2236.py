# Generated by Django 3.2.9 on 2022-03-03 13:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import timetable_v2.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timetable_v2', '0006_auto_20220303_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classtimetableitem',
            name='class_time',
            field=models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], default='', max_length=1, null=True, verbose_name='타임형 수업'),
        ),
        migrations.AlterField(
            model_name='classtimetabletempitem',
            name='class_time',
            field=models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], default='', max_length=1, null=True, verbose_name='타임형 수업'),
        ),
        migrations.CreateModel(
            name='UserTimeClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], default='A', max_length=1, verbose_name='타임')),
                ('_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable_v2.timeclass', verbose_name='수업')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
            options={
                'unique_together': {('user', 'time')},
            },
        ),
        migrations.CreateModel(
            name='UserClassTimetableItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', timetable_v2.models.DayOfTheWeekField(choices=[(1, '월요일'), (2, '화요일'), (3, '수요일'), (4, '목요일'), (5, '금요일'), (6, '토요일'), (7, '일요일')], verbose_name='요일')),
                ('time', models.IntegerField(verbose_name='교시')),
                ('_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable_v2.flexibleclass', verbose_name='이동 수업')),
                ('timetable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable_v2.classtimetablemaster', verbose_name='시간표')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
            options={
                'unique_together': {('user', 'timetable', 'day_of_week', 'time')},
            },
        ),
    ]
