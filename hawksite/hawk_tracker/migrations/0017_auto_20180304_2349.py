# Generated by Django 2.0.1 on 2018-03-04 23:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hawk_tracker', '0016_query_query_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='query_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
