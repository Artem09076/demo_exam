from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .forms import LoginForm, ProductForm
from .models import *
from typing import Any
from django.urls import reverse_lazy

class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm

class ProductListView(ListView):
    template_name = "product_list.html"
    model = Product
    context_object_name = "products"

    def get_queryset(self):
        queryset = Product.objects.all().select_related("supplier")
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(manufacturer__icontains=search_query)
                | Q(category__icontains=search_query)
            )
        supplier_id = self.request.GET.get("supplier", "")
        if supplier_id and supplier_id != "all":
            queryset = queryset.filter(supplier_id=supplier_id)
        sort = self.request.GET.get("sort", "")
        if sort == "asc":
            queryset = queryset.order_by("quantity")
        elif sort == "desc":
            queryset = queryset.order_by("-quantity")
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["suppliers"] = Supplier.objects.all()
        context["current_search"] = self.request.GET.get("search", "")
        context["current_supplier"] = self.request.GET.get("supplier", "")
        context["current_sort"] = self.request.GET.get("sort", "")

        return context


class CreateProduct(CreateView):
    model=Product
    template_name='product_form.html'
    form_class=ProductForm
    success_url=reverse_lazy("product_list")

class UpdateProduct(UpdateView):
    model=Product
    template_name='product_form.html'
    form_class=ProductForm
    success_url=reverse_lazy("product_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = True
        return context
    
class DeleteProduct(DeleteView):
    model=Product
    template_name='product_form.html'
    success_url=reverse_lazy("product_list")