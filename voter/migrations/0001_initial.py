# Generated by Django 3.0.6 on 2020-06-17 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('A', models.IntegerField()),
                ('B', models.IntegerField()),
                ('X', models.IntegerField()),
                ('Y', models.IntegerField()),
            ],
        ),
    ]
