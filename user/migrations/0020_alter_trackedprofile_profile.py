# Generated by Django 4.1 on 2023-02-22 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_remove_profile_viewers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackedprofile',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile_viewed', to='user.profile'),
        ),
    ]