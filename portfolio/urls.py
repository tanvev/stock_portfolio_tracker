from django.urls import path
from . import views

urlpatterns = [
    path('', views.stock_list, name='stock_list'),
    path('add/', views.add_stock, name='add_stock'),
    path('edit/<str:symbol>/', views.edit_stock, name='edit_stock'),
    path('delete/<str:symbol>/', views.delete_stock, name='delete_stock'),
    path('export_csv/', views.export_csv, name='export_csv'),
]
