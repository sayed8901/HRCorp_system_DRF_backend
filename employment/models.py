from django.db import models
from employee.models import Employee
from employee.choices import *
from django.utils.text import slugify

from dateutil.relativedelta import relativedelta


class PersonalInfo(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, to_field='employee_id')
    
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    father_name = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    spouse_name = models.CharField(max_length=255, blank=True, null=True)

    permanent_address = models.TextField()
    present_address = models.TextField()
    date_of_birth = models.DateField()
    smart_id = models.CharField(max_length=20, unique=True)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)

    educational_degree = models.CharField(max_length=20, choices=EDUCATIONAL_DEGREE_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)


    def __str__(self):
        return f'personal info for {self.name}, (id: {self.employee.employee_id})'




class Department(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    # to add automatically slug values after a Department model created or its name updated
    def save(self, *args, **kwargs):
        if not self.slug or self.name != Department.objects.get(pk=self.pk).name:
            self.slug = slugify(self.name)
        super(Department, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'



class Designation(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    # to add automatically slug values after a Designation model created or its name updated
    def save(self, *args, **kwargs):
        if not self.slug or self.name != Designation.objects.get(pk=self.pk).name:
            self.slug = slugify(self.name)
        super(Designation, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'



class JobLocation(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    # to add automatically slug values after a JobLocation model created or its name updated
    def save(self, *args, **kwargs):
        if not self.slug or self.name != JobLocation.objects.get(pk=self.pk).name:
            self.slug = slugify(self.name)
        super(JobLocation, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'



class EmploymentInfo(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, to_field='employee_id')
    status = models.CharField(max_length=10, default='Active', choices=STATUS_CHOICES)

    job_location = models.ForeignKey(JobLocation, on_delete=models.SET_NULL, null=True, blank=False)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=False)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=False)

    joining_date = models.DateField()
    probation_period_months = models.IntegerField(choices=PROBATION_PERIOD_CHOICES, default=6)
    confirmation_effective_date = models.DateField(blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)


    @property
    def tentative_confirmation_date(self):
        # Calculate tentative confirmation date by adding probation period months with joining date
        return self.joining_date + relativedelta(months = self.probation_period_months)
    

    def __str__(self):
        return f'employment info for id: {self.employee.employee_id}, status: {self.status})'


