from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm, ValidationError, CharField
from .models import *

class LoginForm(AuthenticationForm):
    def __init__(self, request = ..., *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields["username"].label = "Логин"
        self.fields["password"].label = "Пароль"

class ProductForm(ModelForm):
    supplier_name = CharField(label="Поставщик", required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            if self.instance.supplier:
                self.fields["supplier_name"].initial = self.instance.supplier
    class Meta:
        model=Product
        fields="__all__"
        labels = {
            "article": "Артикул",
            "name": "Наименование товара",
            "unit": "Единица измерения",
            "price": "Цена",
            'manufacturer': "Производитель",
            "supplier": 'Поставщик',
            "category": 'Категория товара',
            'discount': 'Скидка',
            'quantity': 'Количество товара на складе',
            "description": 'Описание',
            "photo": "Изображение"
        }

    def save(self, commit = True):
        supplier, _ = Supplier.objects.get_or_create(name=self.cleaned_data.get("supplier_name").strip())
        instance = super().save(commit=False)
        instance.supplier = supplier
        if commit:
            instance.save()
        return instance
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError("Цена должна быть больше 0")
        return price
