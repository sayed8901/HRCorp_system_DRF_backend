# Generated by Django 4.2.4 on 2024-09-18 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_alter_employee_employee_id'),
        ('payroll', '0008_payroll_net_salary_payroll_npl_salary_deduction'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payroll',
            options={'ordering': ['-month'], 'verbose_name': 'Payroll', 'verbose_name_plural': 'Payrolls'},
        ),
        migrations.AddField(
            model_name='payroll',
            name='late_joining_deduction',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='status',
            field=models.CharField(default='Inactive', max_length=10),
        ),
        migrations.AlterUniqueTogether(
            name='payroll',
            unique_together={('employee', 'month')},
        ),
    ]