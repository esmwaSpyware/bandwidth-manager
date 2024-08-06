# network/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('device/<int:device_id>/', views.device_detail, name='device_detail'),
    path('policies/', views.policy_list, name='policy_list'),
    path('policies/add/', views.add_policy, name='add_policy'),
    path('roles/manage/', views.manage_roles, name='manage_roles'),
    path('roles/add/', views.add_role, name='add_role'),
    path('api/', include(router.urls)),
]