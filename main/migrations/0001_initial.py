# Generated by Django 4.1.7 on 2024-06-06 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('mail_address', models.CharField(max_length=200)),
                ('creditcard_number', models.CharField(max_length=200)),
                ('creditcard_name', models.CharField(max_length=200)),
                ('security_code', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('restaurantid', models.PositiveIntegerField()),
                ('reservationdate', models.CharField(max_length=10)),
                ('numberofpeople', models.PositiveIntegerField()),
                ('starttime', models.CharField(max_length=10)),
                ('endtime', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('evaluation', models.CharField(max_length=10)),
                ('budget', models.PositiveIntegerField()),
                ('regularholiday', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurantid', models.PositiveIntegerField(default=0)),
                ('datetime', models.CharField(max_length=200)),
                ('username', models.CharField(max_length=200)),
                ('evaluation', models.CharField(max_length=10)),
                ('postcontent', models.CharField(max_length=2000)),
            ],
        ),
    ]
