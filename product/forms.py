from django import forms
from .models import *  # Make sure to import your Product model
from django.forms import inlineformset_factory, modelformset_factory
from .models import Selles 
from django import forms
from .models import Product
import random
import string

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'thumbnail_image', 'purchase_price',
            'sale_price', 'category', 'SubCategory',
            'unit_mesurement', 'unit_type', 'sku','status'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter product name',
                'style': 'font-size: 16px;',
            }),
            'category': forms.Select(attrs={'class': 'form-control form-control-lg', 'style': 'font-size: 16px;'}),
            'purchase_price': forms.NumberInput(attrs={
                    'class': 'form-control form-control-lg',
                    'placeholder': 'Enter purchase price',
                    'style': 'font-size: 16px;',
                    'id': 'purchase_price'  # Important!
                }),
                'sale_price': forms.NumberInput(attrs={
                    'class': 'form-control form-control-lg',
                    'placeholder': 'Enter sale price',
                    'style': 'font-size: 16px;',
                    'id': 'sale_price'  # Important!
                }),
            'SubCategory': forms.Select(attrs={'class': 'form-control form-control-lg', 'style': 'font-size: 16px;'}),
            'unit_mesurement': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter unit measurement',
                'style': 'font-size: 16px;',
            }),
             'unit_type': forms.Select(attrs={
                'class': 'form-control form-control-lg',
                'style': 'font-size: 16px;',
            }),
            'sku': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter SKU',
                'style': 'font-size: 16px;',
                
            }),
            'status': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'role': 'switch',  # Bootstrap 5 switch styling
                'style': 'margin-left: 3.5rem; transform: scale(1.3);',
})
        }
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Product.objects.filter(name__iexact=name).exists():
            raise ValidationError("A product with this name already exists.")
        return name    

    def clean(self):
        cleaned_data = super().clean()
        purchase_price = cleaned_data.get('purchase_price')
        sale_price = cleaned_data.get('sale_price')

        if purchase_price and sale_price and sale_price< purchase_price :
            raise forms.ValidationError("sale price cannot be greater than Purchase price.")
       
    


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter subcategory name',
                'style': 'font-size: 16px;',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control form-control-lg',
            }),
        }
        
        

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name', 'style': 'font-size: 16px;' })
        }
        labels = {
            'name': 'Category Name', 'style': 'font-size: 46px;height: 40px;'  # Custom label for the 'name' field
        }
      



class SupplierForm(forms.ModelForm):
    class Meta:
        model=Supplier
        fields=['name','email','mobile','Address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter supplier name','style': 'font-size: 16px;'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter supplier email','style': 'font-size: 16px;'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter supplier mobile','style': 'font-size: 16px;'}),
            'Address': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter supplier Address','style': 'font-size: 16px;'}),
          

        }



class CustomarForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['name','Email','Mobile','Address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter customer name','style': 'font-size: 16px;'}),
            'Email': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter customer email','style': 'font-size: 16px;'}),
            'Mobile': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter customer mobile','style': 'font-size: 16px;'}),
            'Address': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter customer address','style': 'font-size: 16px;'}),
          

        }


    



class SellesForm(forms.ModelForm):
    class Meta:
        model = Selles
        fields = ['customer', 'discountAmount', 'paidAmount','totalPrice','dueAmount']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
          
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add an empty label (placeholder-like option) to the 'supplier' field
        self.fields['customer'].empty_label = "Select a customer"  # This simulates a placeholder
        self.fields['customer'].widget.attrs.update({
            'class': 'form-control'
        })
        


class sellesItemForm(forms.ModelForm):
    class Meta:
        model = SellesItem
        fields = ['product', 'quantity', 'unit_price','quantity_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the product field has a queryset populated
        self.fields['product'].empty_label = "Select a product"  # This simulates a placeholder
        self.fields['product'].widget.attrs.update({
            'class': 'form-control'
        })


        self.fields['quantity'].widget.attrs.update({
            'placeholder': 'Enter Quantity',
            'style': 'width: 206px;',
            'class': 'form-control'
        })
        self.fields['unit_price'].widget.attrs.update({
            'placeholder': 'Enter Unit Price',
            'class': 'form-control'
        })
        self.fields['quantity_type'].widget.attrs.update({  # <-- new styling for quantity_type
            'class': 'form-control',
            'style': 'width: 120px;',
        })


# Define the widgets for the PurchaseItemFormSet
selles_item_widgets = {
    'product': forms.Select(attrs={'class': 'form-control'}),
    'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Quantity', 'style': 'width: 206px;'}),
    'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Unit Price'}),
    'quantity_type': forms.Select(attrs={'class': 'form-control', 'style': 'width: 120px;'}),  # <-- new widget
    'totalAmount': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
}
# Define the PurchaseItemFormSet to handle multiple PurchaseItems
sellesItemForm = modelformset_factory(
    SellesItem, 
    form=sellesItemForm,  # Use the custom form here
    fields=['product', 'quantity', 'unit_price','quantity_type'], 
    extra=10,
    widgets=selles_item_widgets  # Pass the widgets here
)



class FileUploadForm(forms.Form):
    file = forms.FileField()



class PurchaseInvoiceForm(forms.ModelForm):
    class Meta:
        model = SellesInvoice
        fields ="__all__"


class SellesInvoiceForm(forms.ModelForm):
    class Meta:
        model = SellesInvoice
        fields ="__all__"
        





# PurchaseForm 
class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['supplier', 'discount', 'paidAmount']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
          
        }
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['supplier'].empty_label = "Select a supplier"
        self.fields['supplier'].widget.attrs.update({'class': 'form-control'})

        # These IDs are needed so JavaScript can interact with the fields
        self.fields['discount'].widget.attrs.update({
            'class': 'form-control',
            'id': 'discountAmount'
        })
        self.fields['paidAmount'].widget.attrs.update({
            'class': 'form-control',
            'id': 'paidAmount'
        })

class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['product', 'quantity', 'quantity_type', 'unit_price']  # <-- add 'quantity_type'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].empty_label = "Select a product"
        self.fields['product'].widget.attrs.update({'class': 'form-control'})
        
        self.fields['quantity'].widget.attrs.update({
            'placeholder': 'Enter Quantity',
            'style': 'width: 206px;',
            'class': 'form-control'
        })
        
        self.fields['quantity_type'].widget.attrs.update({  # <-- new styling for quantity_type
            'class': 'form-control',
            'style': 'width: 120px;',
        })
        
        self.fields['unit_price'].widget.attrs.update({
            'placeholder': 'Enter Unit Price',
            'class': 'form-control'
        })

# Define the widgets for the PurchaseItemFormSet
purchase_item_widgets = {
    'product': forms.Select(attrs={'class': 'form-control'}),
    'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Quantity', 'style': 'width: 206px;'}),
    'quantity_type': forms.Select(attrs={'class': 'form-control', 'style': 'width: 120px;'}),  # <-- new widget
    'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Unit Price'}),
    'totalAmount': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
}

# Define the PurchaseItemFormSet to handle multiple PurchaseItems
PurchaseItemFormSet = modelformset_factory(
    PurchaseItem, 
    form=PurchaseItemForm,  # Use the custom form here
    fields=['product', 'quantity', 'unit_price','quantity_type'], 
    extra=10,
    widgets=purchase_item_widgets  # Pass the widgets here
)