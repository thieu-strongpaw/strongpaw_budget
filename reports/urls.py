from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='reports_index'),
    path('incomeVsExpence', views.incomeVsExpence, name='reports_incomeVsExpence'), 
]
