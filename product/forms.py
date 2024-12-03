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


    



class SeelsForm(forms.ModelForm):
    class Meta:
        model = Selles
        fields = ['customer', 'discountAmount', 'paidAmount','totalPrice','dueAmount']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),  # Example widget for product (a dropdown)
            'discountAmount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Unit Price'}),  # For unit price field
            'paidAmount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Unit Price'}),  # For unit price field
            'totalPrice': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'dueAmount' :forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }
        totalPrice = forms.DecimalField(required=False, widget=forms.HiddenInput())
        dueAmount = forms.DecimalField(required=False, widget=forms.HiddenInput())
        def clean(self):
            cleaned_data = super().clean()
            total_price = cleaned_data.get('totalPrice')
            due_amount = cleaned_data.get('dueAmount')

            # Ensure these values are correctly calculated on the server side, if needed
            if total_price and due_amount:
                # Validate or adjust values if necessary
                pass
            
            return cleaned_data

SellesItemFormSet = modelformset_factory(
    SellesItem,  
    fields=['product', 'quantity', 'unit_price','totalAmount',],  
    extra=1, 
    widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),  # Example widget for product (a dropdown)
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Quantity','style': 'width: 206px;'}),  # For quantity field
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Unit Price'}),  # For unit price field
            'totalAmount': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),  # Readonly for totalAmount
            

        }
)

class FileUploadForm(forms.Form):
    file = forms.FileField()


class PurchaseInvoiceForm(forms.ModelForm):
    class Meta:
        model = PurchaseInvoice
        fields ="__all__"





# PurchaseForm 
class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['supplier', 'discount', 'paidAmount']

# Define PurchaseItemFormSet to handle multiple PurchaseItems in the same form
PurchaseItemFormSet = modelformset_factory(PurchaseItem, fields=['product', 'quantity', 'unit_price'],extra=6)