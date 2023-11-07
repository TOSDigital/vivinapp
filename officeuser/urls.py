from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'officeuser'

urlpatterns = [
    path('officeuserlist/', OfficeUserListView.as_view(), name='officeuserlistview'),
    path('officeusercreate/', OfficeUserCreateView.as_view(), name='officeusercreate'),
]

