# Generated by Django 4.1 on 2023-09-17 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0021_userwallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='stripe_connect',
            field=models.BooleanField(default=False),
        ),
    ]
