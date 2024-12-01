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

# class PurchaseForm(forms.ModelForm):
#     class Meta:
#         model = Purchase
#         fields = ['productname', 'suppliername', 'quantity', 'discount', 'paidAmount']
#         widgets = {
#             'productname': forms.Select(attrs={'class': 'form-control form-control-lg', 'style': 'font-size: 16px;'}),
#             'suppliername': forms.Select(attrs={'class': 'form-control form-control-lg', 'style': 'font-size: 16px;'}),
#             'quantity': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name','style': 'font-size: 16px;'}),
#             'discount': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name','style': 'font-size: 16px;'}),
#             'paidAmount': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name','style': 'font-size: 16px;'}),

#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         quantity = cleaned_data.get('quantity')
#         product = cleaned_data.get('productname')
#         discount = cleaned_data.get('discount')
#         paid_amount = cleaned_data.get('paidAmount')

#         # Calculate totalAmount based on product price and quantity
#         if product and quantity:
#             total_amount = product.purchase_price * quantity
#             cleaned_data['totalAmount'] = total_amount

#         if discount is None:
#             cleaned_data['discount'] = 0  # Default discount if not provided
        
#         if paid_amount is None:
#             cleaned_data['paidAmount'] = 0  # Default paid amount if not provided

#         # Calculate dueAmount
#         total_amount = cleaned_data.get('totalAmount')
#         due_amount = total_amount - paid_amount - discount
#         cleaned_data['dueAmount'] = due_amount

#         return cleaned_data
    

# class SellesForm(forms.ModelForm):
#     class Meta:
#         model = Selles
#         fields = [ 'customer', 'discountAmount', 'paidAmount','dueAmount']
#         widgets = {
#             'customer': forms.Select(attrs={'class': 'form-control form-control-lg', 'style': 'font-size: 16px;'}),
#             'discountAmount': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name','style': 'font-size: 16px;'}),
#             'paidAmount': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name','style': 'font-size: 16px;'}),
#             'dueAmount':forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name','style': 'font-size: 16px;'}),
#         }
#     def __init__(self, *args, **kwargs):
#         super(SellesForm, self).__init__(*args, **kwargs)

class SeelsForm(forms.ModelForm):
    class Meta:
        model = Selles
        fields = ['customer', 'discountAmount', 'paidAmount']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),  # Example widget for product (a dropdown)
            'discountAmount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Unit Price'}),  # For unit price field
            'paidAmount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Unit Price'}),  # For unit price field
            
        }

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





# PurchaseForm মডেল ফর্ম
class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['supplier', 'discount', 'paidAmount']  

# PurchaseItemFormSet 
PurchaseItemFormSet = modelformset_factory(
    PurchaseItem, 
    fields=['product', 'quantity', 'unit_price'], 
    extra=1,  
)