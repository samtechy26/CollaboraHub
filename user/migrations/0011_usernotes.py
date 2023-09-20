# Generated by Django 4.1 on 2023-01-24 11:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0010_review_bid_review_user_alter_review_employer_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserNotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('priority', models.IntegerField(choices=[(2, 'High'), (1, 'Medium'), (0, 'Low')])),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]