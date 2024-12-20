# Generated by Django 5.1.2 on 2024-10-21 17:26

import tickets.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='response_message',
            field=models.TextField(blank=True, null=True, verbose_name='Response message'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=tickets.models.ticket_picture_upload_path, verbose_name='Picture'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('received', 'Received'), ('investigating', 'Investigating'), ('solved', 'Solved'), ('denied', 'Denied')], default='received', max_length=20, verbose_name='Status'),
        ),
    ]
