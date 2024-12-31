from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='reports_index'),
    path('monthReport', views.monthlyReport, name='reports_monthReport'),
]
