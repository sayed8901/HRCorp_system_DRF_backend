# Generated by Django 4.2.4 on 2024-09-09 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0002_rename_step_salaryinfo_salary_step'),
    ]

    operations = [
        migrations.AddField(
            model_name='salaryinfo',
            name='casual_leave_balance',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AddField(
            model_name='salaryinfo',
            name='sick_leave_balance',
            field=models.PositiveIntegerField(default=14),
        ),
    ]
