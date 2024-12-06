"""
URL configuration for stocktrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
import stocktrackapi.views.userview as userview
import stocktrackapi.views.inventoryview as inventoryview
import stocktrackapi.views.ordersview as ordersview
import stocktrackapi.views.suppliersview as suppliersview

router = routers.DefaultRouter()
router.register(r'users', userview.StockTrackUserViewSet)
router.register(r'inventory', inventoryview.InventoryViewSet)
router.register(r'orders', ordersview.OrdersViewSet)
router.register(r'suppliers', suppliersview.SupplierViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
]
