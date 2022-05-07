# Generated by Django 3.1.4 on 2022-05-06 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nodes',
            name='chipid',
        ),
        migrations.AddField(
            model_name='nodes',
            name='bin_height',
            field=models.DecimalField(blank=True, decimal_places=2, default=60.0, max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='nodes',
            name='bin_offset',
            field=models.DecimalField(blank=True, decimal_places=2, default=10.0, max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='nodes',
            name='c_id',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='nodes',
            name='coord_lat',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='nodes',
            name='coord_lng',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='nodes',
            name='installed_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
