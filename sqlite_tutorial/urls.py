from django.urls import path
from . import views

app_name = 'sqlite_tutorial'

urlpatterns = [
    path('', views.index, name='index'),
    path('basics/', views.basics, name='basics'),
    path('parameterized/', views.parameterized, name='parameterized'),
    path('optimization/', views.optimization, name='optimization'),
    path('project/', views.project, name='project'),
    path('run_basics/', views.run_basics, name='run_basics'),
    path('run_parameterized/', views.run_parameterized, name='run_parameterized'),
    path('run_optimization/', views.run_optimization, name='run_optimization'),
    path('run_project/', views.run_project, name='run_project'),
]