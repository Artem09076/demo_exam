"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from core.views import UserLoginView, ProductListView, CreateProduct, UpdateProduct, DeleteProduct
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path("admin/", admin.site.urls),
    path("", UserLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("product/add/", CreateProduct.as_view(), name="create_product"),
    path('product/<int:pk>/', UpdateProduct.as_view(), name='upadte_product'),
    path("product/<int:pk>/delete", DeleteProduct.as_view(), name='delete_product')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
