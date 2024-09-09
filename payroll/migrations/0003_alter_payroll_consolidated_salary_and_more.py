# Generated by Django 4.2.4 on 2024-09-09 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0002_remove_payroll_basic_salary_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payroll',
            name='consolidated_salary',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='conveyance',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='effective_basic',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='festival_bonus',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='hardship',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='house_rent',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='is_confirmed',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='medical_allowance',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='other_allowance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='pf_contribution',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='pf_deduction',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='salary_grade',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='salary_step',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='starting_basic',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='swf_deduction',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='tax_deduction',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
