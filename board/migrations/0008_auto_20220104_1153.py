# Generated by Django 3.2.9 on 2022-01-04 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0007_alter_articlevoteitem_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlephoto',
            name='height',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='articlephoto',
            name='orientation',
            field=models.CharField(choices=[('HORIZONTAL', '수평'), ('VERTICAL', '수직'), ('SQUARE', '정사각형')], default='HORIZONTAL', max_length=10),
        ),
        migrations.AddField(
            model_name='articlephoto',
            name='width',
            field=models.IntegerField(default=0),
        ),
    ]