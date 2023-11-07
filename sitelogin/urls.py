from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'sitelogin'

urlpatterns = [
    path('siteuserlist/', SiteUserListView.as_view(), name='siteuserlistview'),
    path('siteusercreate/', SiteUserCreateView.as_view(), name='siteusercreate'),
]

