from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/new/', views.product_create, name='product_create'),
    path('products/edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('sales/new/', views.sale_create, name='sale_create'),
    path('sales/delete/<int:pk>/', views.sale_delete, name='sale_delete'),
    path('invoice/new/', views.invoice_create, name='invoice_create'),
    path('invoice/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('invoice/', views.invoice_list, name='invoice_list'),
    path('invoice/delete/<int:pk>/', views.invoice_delete, name='invoice_delete'),
]
