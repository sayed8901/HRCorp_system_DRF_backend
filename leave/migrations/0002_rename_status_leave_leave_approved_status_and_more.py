# Generated by Django 4.2.4 on 2024-09-09 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leave',
            old_name='status',
            new_name='leave_approved_status',
        ),
        migrations.RemoveField(
            model_name='leave',
            name='days_taken',
        ),
    ]