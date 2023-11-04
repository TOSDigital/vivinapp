from django.contrib import admin
from .models import Project, User, UserProfile, OfficeLogin, SiteEngineer, AttendanceRecord, LaborTypes, Contractor
# from .forms import ProjectCreationForm
from decimal import Decimal


# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass

@admin.register(LaborTypes)
class LaborTypesAdmin(admin.ModelAdmin):
    list_display = ('Contractor', 'Labor_type', 'wage', 'overtime_wage')
    fields = ('Contractor', 'Labor_type', 'wage', 'overtime_wage')
    readonly_fields = ('overtime_wage',)

    def save_model(self, request, obj, form, change):
        if not obj.overtime_wage:  # Check if overtime_wage is not manually set
            obj.overtime_wage = obj.wage / Decimal('8.0')
        super().save_model(request, obj, form, change)


admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(OfficeLogin)
admin.site.register(SiteEngineer)
admin.site.register(AttendanceRecord)

admin.site.register(Contractor)
