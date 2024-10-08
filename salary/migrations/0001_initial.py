# Generated by Django 4.2.4 on 2024-08-25 05:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0004_alter_employee_employee_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalaryInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary_grade', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)])),
                ('step', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])),
                ('starting_basic', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('effective_basic', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('other_allowance', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('festival_bonus', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('salary_deduction_npl', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employee.employee')),
            ],
        ),
    ]
