# Generated by Django 4.1 on 2022-09-05 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_job_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='creator',
        ),
    ]
