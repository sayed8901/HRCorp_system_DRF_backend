# Generated by Django 4.2.4 on 2024-08-26 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employment', '0010_alter_personalinfo_email'),
        ('transfer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transferinfo',
            name='transfer_from_department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfer_from_department', to='employment.department'),
        ),
        migrations.AddField(
            model_name='transferinfo',
            name='transfer_from_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transfer_from_location', to='employment.joblocation'),
        ),
    ]
