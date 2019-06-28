from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('order/<slug:order_id>/', views.carriers, name='carriers'),

]