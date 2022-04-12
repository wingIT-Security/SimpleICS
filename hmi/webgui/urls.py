from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('functionchange/', views.ajax_rsp, name='func_change'),
    path('train/', views.train, name='train'),
]