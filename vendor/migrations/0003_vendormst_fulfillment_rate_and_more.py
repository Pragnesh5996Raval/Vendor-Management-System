# Generated by Django 5.0.4 on 2024-05-03 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_remove_vendormst_average_response_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendormst',
            name='fulfillment_rate',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='vendormst',
            name='on_time_delivery_rate',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='vendormst',
            name='quality_rating_avg',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='vendormst',
            name='response_time_avg',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='vendormst',
            name='vendor_code',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
