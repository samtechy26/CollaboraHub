# Generated by Django 4.1 on 2022-09-04 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('minimun_salary', models.CharField(max_length=200)),
                ('maximum_salary', models.CharField(max_length=200)),
                ('years_of_experience', models.CharField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49), (50, 50), (51, 51), (52, 52), (53, 53), (54, 54), (55, 55), (56, 56), (57, 57), (58, 58), (59, 59)], default=1, max_length=200)),
                ('website', models.CharField(max_length=300)),
                ('email_address', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female'), ('Any', 'Any')], default='Any', max_length=200)),
                ('shift', models.CharField(choices=[('Day', 'Day'), ('Night', 'Night'), ('Any', 'Any')], default='Day', max_length=200)),
                ('description', models.CharField(max_length=1000)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='job.country')),
                ('job_category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='job.category')),
                ('job_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='job.type')),
                ('level_of_education', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='job.education')),
            ],
        ),
    ]