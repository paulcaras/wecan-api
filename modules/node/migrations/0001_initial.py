# Generated by Django 3.1.4 on 2022-02-22 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Nodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chipid', models.BigIntegerField(blank=True, default=0, null=True)),
                ('name', models.CharField(blank=True, max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Nodes',
                'db_table': 'nodes',
            },
        ),
    ]
