# Generated by Django 3.1.4 on 2022-05-28 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read', '0004_auto_20220510_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='readingssensor',
            name='stat',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]