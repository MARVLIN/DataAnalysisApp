# Generated by Django 4.2 on 2023-04-10 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chartjs', '0009_data_mse_data_ssim_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='mse',
            field=models.FloatField(max_length=100),
        ),
        migrations.AlterField(
            model_name='data',
            name='ssim_score',
            field=models.FloatField(max_length=100),
        ),
    ]