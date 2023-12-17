# Generated by Django 4.1.3 on 2023-12-17 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('battles', '0001_init'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battlereffect',
            name='battle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applied_effects', to='battles.battle'),
        ),
        migrations.AlterField(
            model_name='battlereffect',
            name='battler',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='battles.battler'),
        ),
    ]