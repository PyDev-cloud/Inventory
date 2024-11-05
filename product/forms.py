from django import forms
from .models import *  # Make sure to import your Product model

class ProductForm(forms.ModelForm):
    class Meta:
        model = product  # Use 'model' instead of 'models'
        fields = [
            'name', 'thumbnail_image', 'quantity', 'purchase_price', 
            'sale_price', 'category', 'sub_category', 
            'unit_mesurement', 'unit_type', 'reorder_quantity', 'sku'
        ]
        
    # You can customize the widgets here
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    thumbnail_image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    purchase_price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    sale_price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    category = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    sub_category = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    unit_mesurement = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    unit_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    reorder_quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    sku = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
        


class CategoryForm(forms.ModelForm):
    class Meta:
        model=category
        fields=['name']

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