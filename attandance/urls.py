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
    path('report/', WageCalculationView.as_view(), name='attendancereport'),
    path('ajax/load-contractors/', ContractorOptionsView.as_view(), name='ajax_load_contractors'),
    







]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)