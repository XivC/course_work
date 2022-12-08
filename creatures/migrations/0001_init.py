# Generated by Django 4.1.3 on 2022-12-04 18:39

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('planets', '0001_init'),
    ]

    operations = [
        migrations.CreateModel(
            name='Creature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('power', models.PositiveIntegerField()),
                ('icon', models.URLField(blank=True, null=True)),
                ('planet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creatures',
                                             to='planets.planet')),
            ],
        ),
    ]
