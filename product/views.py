from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import *
from .models import *
from .forms import *
# Create your views here.

class CategoryView(CreateView):
    model = category
    form_class = CategoryForm
    template_name = "product/categorycreate.html"  # Corrected template path
    success_url = reverse_lazy('success')  # Redirect after successful creation

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Category created successfully!")  # Success message
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")  # Error message
        return super().form_invalid(form)

class SubCategoryView(CreateView):
    model=SubCategory
    form_class=SubcategoryForm
    template_name="product/Subcategorycreate.html"
    #success_url = reverse_lazy('success')  # Redirect after successful creation
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Category created successfully!")  # Success message
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")  # Error message
        return super().form_invalid(form)

    
    
    

class ProductView(View):
    form_class = ProductForm
    template_name = "product/productcreate.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            "form": form,
            "categories": category.objects.all(),  # Call .all() to get the queryset
            "subcategories": SubCategory.objects.all(),  # Call .all() to get the queryset
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():  # Check if the form is valid
            form.save()  # Save the product
            messages.success(request, "Product created successfully!")  # Success message
            return redirect('success')  # Redirect to a success page or another view
        else:
            messages.error(request, "Please correct the errors below.")  # Error message

        context = {
            "form": form,
            "categories": category.objects.all(),
            "subcategories": SubCategory.objects.all(),
        }
        return render(request, self.template_name, context)  # Render the form with errors

 

class SupplierCreate(CreateView):
    model=Supplier
    form_class=SupplierForm
    template_name="product/SupplierCreate.html"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Category created successfully!")  # Success message
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")  # Error message
        return super().form_invalid(form)
    

    
class CustomerCreate(CreateView):
    model=Customer
    form_class=CustomarForm
    template_name="product/Customercreate.html"
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Category created successfully!")  # Success message
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")  # Error message
        return super().form_invalid(form)
    