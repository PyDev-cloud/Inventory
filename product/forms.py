from django import forms
from .models import *  # Make sure to import your Product model

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product  # Use 'model' instead of 'models'
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
        


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model=SubCategory
        fields=['name','category']
        widgets={
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name'}),
            'category': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name'})
        }
        

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name'})
            

        }
      



class SupplierForm(forms.ModelForm):
    class Meta:
        model=Supplier
        fields=['name','email','mobile','Address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name'}),
            'Address': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name'}),
          

        }



class CustomarForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['name','Email','Mobile','Address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name'}),
            'Email': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name'}),
            'Mobile': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name'}),
            'Address': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter category name'}),
          

        }

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['productname', 'suppliername', 'quantity', 'discount', 'paidAmount']

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('productname')
        discount = cleaned_data.get('discount')
        paid_amount = cleaned_data.get('paidAmount')

        # Calculate totalAmount based on product price and quantity
        if product and quantity:
            total_amount = product.purchase_price * quantity
            cleaned_data['totalAmount'] = total_amount

        if discount is None:
            cleaned_data['discount'] = 0  # Default discount if not provided
        
        if paid_amount is None:
            cleaned_data['paidAmount'] = 0  # Default paid amount if not provided

        # Calculate dueAmount
        total_amount = cleaned_data.get('totalAmount')
        due_amount = total_amount - paid_amount - discount
        cleaned_data['dueAmount'] = due_amount

        return cleaned_data
    

class SellesForm(forms.ModelForm):
    class Meta:
        model = Selles
        fields = ['product', 'customer', 'quantity', 'discountAmount', 'paidAmount']

    def __init__(self, *args, **kwargs):
        super(SellesForm, self).__init__(*args, **kwargs)


class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(label='Select an Excel file to upload')