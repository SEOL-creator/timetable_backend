# Generated by Django 3.2.9 on 2021-11-26 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0021_remoteurl_mobileurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='color',
            field=models.CharField(choices=[('#eb514a', 'Classic Red 1'), ('#cc3333', 'Classic Red 2'), ('#ac1921', 'Classic Red 3'), ('#feb42f', 'Classic Orange 1'), ('#fe9912', 'Classic Orange 2'), ('#de7f0d', 'Classic Orange 3'), ('#fee851', 'Classic Yellow 1'), ('#fecc33', 'Classic Yellow 2'), ('#e0b018', 'Classic Yellow 3'), ('#8fe03c', 'Classic Green 1'), ('#72c41f', 'Classic Green 2'), ('#54a807', 'Classic Green 3'), ('#75c7e2', 'Classic Skyblue 1'), ('#58acc6', 'Classic Skyblue 2'), ('#3991aa', 'Classic Skyblue 3'), ('#628efd', 'Classic Blue 1'), ('#4075e1', 'Classic Blue 2'), ('#195dc4', 'Classic Blue 3'), ('#c87cfe', 'Classic Purple 1'), ('#ab62e2', 'Classic Purple 2'), ('#8e48c6', 'Classic Purple 3'), ('#f87ec2', 'Classic Pink 1'), ('#db63a7', 'Classic Pink 2'), ('#be478c', 'Classic Pink 3'), ('#919191', 'Classic Gray 1'), ('#787878', 'Classic Gray 2'), ('#5f5f5f', 'Classic Gray 3')], max_length=7, verbose_name='색상'),
        ),
    ]
