from django.contrib import admin
from .models import PromotionInfo


# Register your models here.
class PromotionInfoAdmin(admin.ModelAdmin):
    def employee_id(self, obj):
        return obj.employee.employee_id

    list_display = ['employee_id', 'promoted_to_designation', 'promoted_salary_grade', 'promoted_salary_step', 'promotion_effective_date', 'entry_date']

admin.site.register(PromotionInfo, PromotionInfoAdmin)