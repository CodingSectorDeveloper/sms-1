from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('approval', views.approval, name="approval"),
    path('create_dealer/', views.create_dealer, name="create_dealer"),
    path('dealers/', views.dealers, name="dealers"),
    path('dealer_details/<int:id>', views.dealer_details, name="dealer_details"),
    path('approval_details/<int:id>', views.approval_details, name="approval_details"),
    path('approve/<int:id>', views.approve, name="approve"),
    path('reject/<int:id>', views.reject, name="reject"),
]
