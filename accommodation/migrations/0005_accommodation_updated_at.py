# Generated by Django 4.1.2 on 2022-10-30 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accommodation', '0004_remove_accommodation_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='accommodation',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]