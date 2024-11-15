from django.urls import path
from . import views

urlpatterns = [
    path('', views.alarm_list, name='alarm-list'),
    path('alarm/new/', views.alarm_create, name='alarm-create'),
    path('alarm/<int:pk>/update/', views.alarm_update, name='alarm-update'),
    path('alarm/<int:pk>/delete/', views.alarm_delete, name='alarm-delete'),
    path('alarm/<int:pk>/toggle/', views.alarm_toggle, name='alarm-toggle'),
    path('test-sound/<str:sound_file>/', views.test_sound, name='test-sound'),
]