from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('',views.Index,name='index'),
    path('api/products/',views.ProductHandler.as_view(),name='products'),
    path('api/products/<int:prod_id>/',views.UpdateProduct.as_view(),name='update_product'),
    path('api/dashboard/',views.Dashboard,name='dashboard'),
    path('api/login/',views.LoginView.as_view(),name='login'),
    path("api/product/dashboard",views.DasbboardView.as_view,name='api_dashboard')
]