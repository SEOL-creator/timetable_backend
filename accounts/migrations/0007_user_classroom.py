# Generated by Django 3.2.9 on 2022-03-03 23:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0024_classtingurl'),
        ('accounts', '0006_alter_user_profilepic'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='classroom',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='timetable.classroom', verbose_name='학급'),
        ),
    ]