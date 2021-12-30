# Generated by Django 3.2.9 on 2021-12-23 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_board_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='type',
            field=models.CharField(choices=[('ALL', '모두 허용'), ('ANON', '익명 전용'), ('REAL', '실명 전용')], default='ALL', max_length=8),
        ),
    ]
