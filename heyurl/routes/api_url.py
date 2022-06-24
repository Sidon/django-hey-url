from django.urls import path

from heyurl import views

urlpatterns = [
    path('', views.month_metrics, name='api'),
]
