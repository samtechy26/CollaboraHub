# Generated by Django 4.1 on 2022-11-05 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0016_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='has_paid',
            field=models.BooleanField(default=False, verbose_name='Payment Status'),
        ),
        migrations.AddField(
            model_name='bid',
            name='stripe_payment_intent',
            field=models.CharField(default='completed', max_length=200),
        ),
    ]
