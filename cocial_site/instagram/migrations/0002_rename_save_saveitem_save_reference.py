# Generated by Django 5.1.4 on 2024-12-22 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='saveitem',
            old_name='save',
            new_name='save_reference',
        ),
    ]
