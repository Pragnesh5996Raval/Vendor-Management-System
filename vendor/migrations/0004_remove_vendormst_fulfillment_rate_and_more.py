# Generated by Django 5.0.4 on 2024-05-05 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0003_vendormst_fulfillment_rate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendormst',
            name='fulfillment_rate',
        ),
        migrations.RemoveField(
            model_name='vendormst',
            name='on_time_delivery_rate',
        ),
        migrations.RemoveField(
            model_name='vendormst',
            name='quality_rating_avg',
        ),
        migrations.RemoveField(
            model_name='vendormst',
            name='response_time_avg',
        ),
        migrations.AlterField(
            model_name='historyperformancemst',
            name='average_response_time',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='historyperformancemst',
            name='fulfillment_rate',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='historyperformancemst',
            name='on_time_delivery_rate',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='historyperformancemst',
            name='quality_rating_avg',
            field=models.FloatField(default=0),
        ),
    ]