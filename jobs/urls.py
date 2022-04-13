from django.urls import path
from . import views
from django.views.generic.base import View


urlpatterns = [

    path('', views.encontrar_jobs, name="encontrar_jobs"),
    path('aceitar_job/<int:id>/', views.aceitar_job, name="aceitar_job"),
    path('perfil/', views.perfil, name="perfil"),
    path('enviar_projeto/', views.enviar_projeto, name="enviar_projeto"),
    path('job_create/', views.CreateJob.as_view(), name='job_create'),
]