# Generated by Django 4.2.4 on 2024-09-10 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0005_rename_npl_deduction_payroll_npl_salary_deduction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payroll',
            name='net_salary',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
