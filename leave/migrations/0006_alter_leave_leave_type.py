# Generated by Django 4.2.4 on 2024-09-10 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0005_alter_leave_entry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='leave_type',
            field=models.CharField(choices=[('Sick', 'Sick'), ('Casual', 'Casual'), ('Non_Paid_Leave', 'Non-Paid Leave')], max_length=20),
        ),
    ]
