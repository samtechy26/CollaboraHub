# Generated by Django 4.1 on 2023-03-02 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0028_job_active_job_expiry_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='img',
        ),
    ]
