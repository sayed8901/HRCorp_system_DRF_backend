# Generated by Django 4.2.4 on 2024-08-27 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confirmation', '0002_confirmationinfo_entry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmationinfo',
            name='entry_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
