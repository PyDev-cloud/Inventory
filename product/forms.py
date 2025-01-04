from django import forms
from .models import *  # Make sure to import your Product model
from django.forms import inlineformset_factory, modelformset_factory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product  # Use 'model' instead of 'models'
        fields = [
            'name', 'thumbnail_image', 'purchase_price', 
            'sale_price', 'category', 'SubCategory', 
            'unit_mesurement', 'unit_type',  'sku'
        ]
        widgets={
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name','style': 'font-size: 16px;'}),
            'category': forms.Select(attrs={'class': 'form-control form-control-lg','style': 'font-size: 16px;'}),
            'purchase_price': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name','style': 'font-size: 16px;'}),
            'sale_price': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name','style': 'font-size: 16px;'}),
            'SubCategory': forms.Select(attrs={'class': 'form-control form-control-lg', 'style': 'font-size: 16px;'}),
            'unit_mesurement': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name','style': 'font-size: 16px;'}),
            'unit_type': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name','style': 'font-size: 16px;'}),
            'sku': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name','style': 'font-size: 16px;'}),

        }
    # You can customize the widgets here
    
        


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model=SubCategory
        fields=['name','category']
        widgets={
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name','style': 'font-size: 16px;'}),
            'category': forms.Select(attrs={'class': 'form-control form-control-lg'})
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
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name','style': 'font-size: 16px;'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name','style': 'font-size: 16px;'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name','style': 'font-size: 16px;'}),
            'Address': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name','style': 'font-size: 16px;'}),
          

        }



class CustomarForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['name','Email','Mobile','Address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name','style': 'font-size: 16px;'}),
            'Email': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name','style': 'font-size: 16px;'}),
            'Mobile': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name','style': 'font-size: 16px;'}),
            'Address': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name','style': 'font-size: 16px;'}),
          

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
        fields = ['product', 'quantity', 'unit_price']

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


# Define the widgets for the PurchaseItemFormSet
selles_item_widgets = {
    'product': forms.Select(attrs={'class': 'form-control'}),
    'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Quantity', 'style': 'width: 206px;'}),
    'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Unit Price'}),
    'totalAmount': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
}
# Define the PurchaseItemFormSet to handle multiple PurchaseItems
sellesItemForm = modelformset_factory(
    SellesItem, 
    form=sellesItemForm,  # Use the custom form here
    fields=['product', 'quantity', 'unit_price'], 
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
        # Add an empty label (placeholder-like option) to the 'supplier' field
        self.fields['supplier'].empty_label = "Select a supplier"  # This simulates a placeholder
        self.fields['supplier'].widget.attrs.update({
            'class': 'form-control'
        })

class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['product', 'quantity', 'unit_price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add an empty label (placeholder-like option) to the 'product' field
        self.fields['product'].empty_label = "Select a product"  # This simulates a placeholder
        self.fields['product'].widget.attrs.update({
            'class': 'form-control'
        })
        # You can also set custom placeholder for other fields if needed
        self.fields['quantity'].widget.attrs.update({
            'placeholder': 'Enter Quantity',
            'style': 'width: 206px;',
            'class': 'form-control'
        })
        self.fields['unit_price'].widget.attrs.update({
            'placeholder': 'Enter Unit Price',
            'class': 'form-control'
        })

# Define the widgets for the PurchaseItemFormSet
purchase_item_widgets = {
    'product': forms.Select(attrs={'class': 'form-control'}),
    'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Quantity', 'style': 'width: 206px;'}),
    'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Unit Price'}),
    'totalAmount': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
}

# Define the PurchaseItemFormSet to handle multiple PurchaseItems
PurchaseItemFormSet = modelformset_factory(
    PurchaseItem, 
    form=PurchaseItemForm,  # Use the custom form here
    fields=['product', 'quantity', 'unit_price'], 
    extra=10,
    widgets=purchase_item_widgets  # Pass the widgets here
)