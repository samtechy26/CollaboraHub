# Generated by Django 4.1 on 2022-12-02 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0018_alter_bid_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.TextField(max_length=10000),
        ),
    ]
