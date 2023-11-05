from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    
    path('office/', DashboardView.as_view(), name='dashboard'),
    path('projects/', ProjectListView.as_view(), name='projects'),
    path('createproject/', ProjectCreateView.as_view(), name='createproject'),
    path('updateproject/<int:pk>/', ProjectUpdateView.as_view(), name='updateproject'),
    path('projectdetail/<int:pk>/', ProjectDeatilView.as_view(), name='projectdetail'),
    path('attendance/new/', AttendanceRecordCreateView.as_view(), name='attendance_record'),
    path('ajax/load-contractors/', load_contractors, name='ajax_load_contractors'),
    path('ajax/load-labor-types/', load_labor_types, name='ajax_load_labor_types'),
    path('attendancelist/', AttendanceRecordListView.as_view(), name='attendance_recordlist'),
    path('attendanceupdate/<int:pk>/', AttendanceRecordUpdateView.as_view(), name='attendance_recordupdate'),
    path('attendancedelete/<int:pk>/', AttendanceRecordDeleteView.as_view(), name='attendance_recorddelete'),
    path('all-reports/', AllReports.as_view(), name='allreports'),
    path('report/', WageCalculationView.as_view(), name='attendancereport'),
    path('ajax/load-contractors/', ContractorOptionsView.as_view(), name='ajax_load_contractors'),
    path('contractorcreate/', ContractorCreateView.as_view(), name='createcontractor'),
    path('contractorslist/', ContractorListView.as_view(), name='contractorslist'),
    path('contractorsupdate/<int:pk>', ContractorUpdateView.as_view(), name='contractorsupdate'),
    path('contractorsdelete/<int:pk>', ContractorDeleteView.as_view(), name='contractorsdelete'),
    path('Labortypelist/', LaborTypeListView.as_view(), name='labortypelist'),
    path('Labortypecreate/', LaborTypeCreateView.as_view(), name='labortypecreate'),
    path('Labortypeupdate/<int:pk>', LaborTypeUpdateView.as_view(), name='labortypeupdate'),
    path('Labortypedelete/<int:pk>', LaborTypeDeleteView.as_view(), name='labortypedelete'),
    path('Labortypedetail/<int:pk>', LaborTypeDeatilView.as_view(), name='labortypedetail'),
    path('overtimewagelist/', OvertimeListView.as_view(), name='overtimelist'),
    path('overtimewagecreate/', OvertimeCreateView.as_view(), name='overtimecreate'),
    path('overtimewageupdate/<int:pk>', OvertimeUpdateView.as_view(), name='overtimeupdate'),
    path('overtimewagedelete/<int:pk>', OvertimeDeleteView.as_view(), name='overtimedelete'),
    path('overtime-wage-calculation/', OvertimeWageCalculationView.as_view(), name='overtime_wage_calculation'),
    path('ajax/load-contractors/', LoadContractorsView.as_view(), name='ajax_load_contractors'),
    path('materialcategories/', MaterialCategoryList.as_view(), name='materialcategorylist'),
    path('materialcategoriescreate/', MaterialCreateView.as_view(), name='materialcategorycreate'),
    path('materialcategorydelete/<int:pk>/', MaterialDeleteView.as_view(), name='materialcategorydelete'),


    







]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)