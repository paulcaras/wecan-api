# Generated by Django 3.1.4 on 2022-02-22 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('node', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Readings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.DecimalField(decimal_places=2, max_digits=8)),
                ('turbidity', models.DecimalField(decimal_places=2, max_digits=8)),
                ('ph_level', models.DecimalField(decimal_places=2, max_digits=8)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('node', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='node', to='node.nodes')),
            ],
            options={
                'verbose_name_plural': 'Readings',
                'db_table': 'readings',
            },
        ),
    ]