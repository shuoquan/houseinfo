# Generated by Django 2.1.7 on 2019-03-14 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Count',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('areaName', models.CharField(max_length=10)),
                ('total', models.IntegerField()),
            ],
        ),
    ]