# Generated by Django 4.1 on 2022-09-13 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0010_skills_job_date_created_job_skill'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Skills',
            new_name='Skill',
        ),
    ]