from pyexpat.errors import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import *
from .models import *
from .forms import *
# Create your views here.
#category Creater View 
class CategoryView(CreateView):
    model = category
    form_class = CategoryForm
    template_name = "category/categorycreate.html"  # Corrected template path
    success_url = reverse_lazy('categorylist')  # Redirect after successful creation

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Category created successfully!")  # Success message
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")  # Error message
        return super().form_invalid(form)
#category View 

class categoryViewlist(ListView):
        model=category
        template_name="category/categoryList.html"
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["Category"] = self.model.objects.all()
            return context
        
        
#Category Update View 
class CategoryUpdateView(UpdateView):
    model = category
    form_class = CategoryForm  # The form used for editing
    template_name = 'category/categoryUpdate.html'  # The template to render the form
    context_object_name = 'category'  # The context variable used in the template

    # Redirect to the category list view upon successful update
    success_url = reverse_lazy('categorylist')

    def get_object(self, queryset=None):
       queryset = category.objects.filter(pk=self.kwargs['pk'])
       try:
            obj=queryset.get()
       except category.DoesNotExixt:
            raise Http404("category not found or inactive")
       return obj
       

     
              

#SubCategory View
class SubcategoryViewlist(ListView):
        model=SubCategory
        template_name="subcategory/SubcategoryList.html"
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["subcategory"] = self.model.objects.all()
            return context
      
class SubCategoryView(CreateView):
    model=SubCategory
    form_class=SubcategoryForm
    template_name="subcategory/Subcategorycreate.html"
    #success_url = reverse_lazy('success')  # Redirect after successful creation
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Category created successfully!")  # Success message
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")  # Error message
        return super().form_invalid(form)

#SubCategory Update View
class SubCategoryUpdateView(UpdateView):
    model = SubCategory
    form_class = SubcategoryForm  # The form used for editing
    template_name = 'subcategory/subcategoryUpdate.html'  # The template to render the form
    context_object_name = 'SubCategory'  # The context variable used in the template

    # Redirect to the category list view upon successful update
    success_url = reverse_lazy('subcategorylist')

    def get_object(self, queryset=None):
       queryset = SubCategory.objects.filter(pk=self.kwargs['pk'])
       try:
            obj=queryset.get()
       except SubCategory.DoesNotExixt:
            raise Http404("category not found or inactive")
       return obj
    

#product List View 
class Productlist(ListView):
        model=product
        template_name="product/productList.html"
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["product"] = self.model.objects.all()
            return context

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



class ProductUpdateView(UpdateView):
    model = product
    form_class = ProductForm  # The form used for editing
    template_name = 'product/productupdate.html'  # The template to render the form
    context_object_name = 'product'  # The context variable used in the template

    # Redirect to the category list view upon successful update
    success_url = reverse_lazy('productlist')

    def get_object(self, queryset=None):
       queryset = product.objects.filter(pk=self.kwargs['pk'])
       try:
            obj=queryset.get()
       except product.DoesNotExixt:
            raise Http404("category not found or inactive")
       return obj


class SupplierList(ListView):
        model=Supplier
        template_name="supplier/supplierList.html"
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["supplier"] = self.model.objects.all()
            return context


class SupplierCreate(CreateView):
    model=Supplier
    form_class=SupplierForm
    template_name="supplier/SupplierCreate.html"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Category created successfully!")  # Success message
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")  # Error message
        return super().form_invalid(form)
    

#Customer List View
class Customerlist(ListView):
        model=Customer
        template_name="customer/customerlist.html"
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["customer"] = self.model.objects.all()
            return context


class CustomerCreate(CreateView):
    model=Customer
    form_class=CustomarForm
    template_name="customer/Customercreate.html"
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Category created successfully!")  # Success message
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")  # Error message
        return super().form_invalid(form)


class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomarForm  # The form used for editing
    template_name = 'customer/customerUpdate.html'  # The template to render the form
    context_object_name = 'customer'  # The context variable used in the template

    # Redirect to the category list view upon successful update
    success_url = reverse_lazy('customerlist')

    def get_object(self, queryset=None):
       queryset = Customer.objects.filter(pk=self.kwargs['pk'])
       try:
            obj=queryset.get()
       except Customer.DoesNotExixt:
            raise Http404("category not found or inactive")
       return obj
    