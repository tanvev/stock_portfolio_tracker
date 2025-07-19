from django.urls import path
from . import views

urlpatterns = [
    path('', views.stock_list, name='stock_list'),
    path('add/', views.add_stock, name='add_stock'),
    path('edit/<str:symbol>/', views.edit_stock, name='edit_stock'),
    path('delete/<str:symbol>/', views.delete_stock, name='delete_stock'),
    path('export_csv/', views.export_csv, name='export_csv'),
    path('stock/<str:symbol>/', views.stock_detail, name='stock_detail'),
    path('api/live-price/<str:symbol>/', views.get_live_price, name='live_price'),
    path('api/price/<str:symbol>/', views.get_live_price, name='get_live_price'),
    path('stock/<str:symbol>/delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
    path('stock/<str:symbol>/add_note/', views.add_note, name='add_note'),

]
