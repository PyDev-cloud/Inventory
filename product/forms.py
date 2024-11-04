from django import forms
from .models import *  # Make sure to import your Product model

class ProductForm(forms.ModelForm):
    class Meta:
        model = product  # Use 'model' instead of 'models'
        fields = "__all__"  # This will include all fields from the Product model


class CategoryForm(forms.ModelForm):
    class Meta:
        model=category
        fields="__all__"

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model=SubCategory
        fields="__all__"



class SupplierForm(forms.ModelForm):
    class Meta:
        model=Supplier
        fields="__all__"


class CustomarForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields="__all__"