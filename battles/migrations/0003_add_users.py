# Generated by Django 4.1.3 on 2023-12-17 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battles', '0002_adventure_auto_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battle',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
