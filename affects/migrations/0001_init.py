# Generated by Django 4.1.3 on 2022-12-04 18:39

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('planets', '0001_init'),
        ('creatures', '0001_init'),
    ]

    operations = [
        migrations.CreateModel(
            name='Effect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('power_affect', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Weapon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('power', models.IntegerField()),
                ('icon', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlanetEffectRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creature_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+',
                                                  to='creatures.creature')),
                ('effect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planets_rules',
                                             to='affects.effect')),
                ('planet',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='planets.planet')),
            ],
        ),
        migrations.CreateModel(
            name='CreatureEffectRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_to_ally', models.BooleanField()),
                ('creature_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+',
                                                    to='creatures.creature')),
                ('creature_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+',
                                                  to='creatures.creature')),
                ('effect',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creatures_rules',
                                   to='affects.effect')),
            ],
        ),
        migrations.AddConstraint(
            model_name='planeteffectrule',
            constraint=models.UniqueConstraint(fields=('planet', 'effect', 'creature_to'),
                                               name='planet_effect_rule_unique'),
        ),
        migrations.AddConstraint(
            model_name='creatureeffectrule',
            constraint=models.UniqueConstraint(fields=('effect', 'creature_from', 'creature_to', 'is_to_ally'),
                                               name='creature_effect_rule_unique'),
        ),
    ]
