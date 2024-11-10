from django.http import HttpResponse
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from pyexpat.errors import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from datetime import datetime
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
    form_class=SubCategoryForm
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
    form_class = SubCategoryForm  # The form used for editing
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





class PurchaseReceiptView(View):
    def get(self, request, purchase_id):
        # Fetch the Purchase object by ID, or return 404 if it doesn't exist
        purchase = get_object_or_404(Purchase, id=purchase_id)

        # Render the receipt template with the purchase data
        return render(request, 'Receipt/PurchaseReceipt.html', {'purchase': purchase})
    
class PurchaseCreate(CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'purchase/Purchasecreate.html'
    success_url = reverse_lazy('purchaseList')  # Redirect to the order list view after successful creation

    def form_valid(self, form):
        # Save the purchase object to the database
        self.object = form.save()

        # Redirect to the purchase receipt page for the created purchase
        return redirect('purchase_receipt', purchase_id=self.object.id)
    

class PurchaseListView(ListView):
     model = Purchase
     template_name = "purchase/purchaseList.html"
     def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["Purchase"] = self.model.objects.all()
            return context


     


class SellesCreateView(CreateView):
    model = Selles
    form_class = SellesForm
    template_name = 'Sells/SellsCreate.html'  # Replace with your template's name
    success_url = reverse_lazy('selles_list')  # Redirect after a successful submission (adjust URL as needed)

    def form_valid(self, form):
        # Extract data from the form
        product = form.cleaned_data['product']
        quantity = form.cleaned_data['quantity']
        discountAmount = form.cleaned_data['discountAmount']
        paidAmount = form.cleaned_data['paidAmount']

        # Calculate totalPrice (product price * quantity)
        totalPrice = product.sale_price * quantity

        # Calculate dueAmount (totalPrice - paidAmount - discountAmount)
        dueAmount = totalPrice - paidAmount - discountAmount

        # Set the calculated values on the form instance
        form.instance.totalPrice = totalPrice
        form.instance.dueAmount = dueAmount

        # Save the form data
        return super().form_valid(form)

    def form_invalid(self, form):
        # Handle any form validation errors (optional)
        return super().form_invalid(form)
    



class DailyReportView(TemplateView):
    template_name = 'report/DailyReport.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get today's date
        today = timezone.now().date()

        # Total purchase for today
        total_purchase = Purchase.objects.filter(create_at=today).aggregate(
            total_quantity=Sum('quantity'),
            total_amount=Sum('totalAmount')
        )

        # Total sales for today
        total_sales = Selles.objects.filter(created_at__date=today).aggregate(
            total_quantity=Sum('quantity'),
            total_amount=Sum('totalPrice')
        )
        
        # Total purchase cost for today
        total_purchase_cost = Purchase.objects.filter(create_at=today).aggregate(
            total_cost=Sum('productname__purchase_price')
        )['total_cost'] or 0

        # Total sales amount for today
        total_sales_amount = total_sales['total_amount'] or 0
        
        # Profit calculation
        profit = total_sales_amount - total_purchase_cost

        context.update({
            'total_purchase': total_purchase,
            'total_sales': total_sales,
            'profit': profit,
            'today': today
        })
        return context


class WeeklyReportView(TemplateView):
    template_name = 'report/weekly_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get today's date and calculate the start of the current week (Monday)
        today = timezone.now().date()
        start_date = today - timedelta(days=today.weekday())

        # Total purchase for the week
        total_purchase = Purchase.objects.filter(create_at__gte=start_date).aggregate(
            total_quantity=Sum('quantity'),
            total_amount=Sum('totalAmount')
        )

        # Total sales for the week
        total_sales = Selles.objects.filter(created_at__gte=start_date).aggregate(
            total_quantity=Sum('quantity'),
            total_amount=Sum('totalPrice')
        )
        
        # Total purchase cost for the week
        total_purchase_cost = Purchase.objects.filter(create_at__gte=start_date).aggregate(
            total_cost=Sum('productname__purchase_price')
        )['total_cost'] or 0

        # Total sales amount for the week
        total_sales_amount = total_sales['total_amount'] or 0
        
        # Profit calculation
        profit = total_sales_amount - total_purchase_cost

        context.update({
            'total_purchase': total_purchase,
            'total_sales': total_sales,
            'profit': profit,
            'start_date': start_date,
            'end_date': today
        })
        return context

class MonthlyReportView(TemplateView):
    template_name = 'report/monthly_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get today's date and calculate the start of the current month
        today = timezone.now().date()
        start_date = today.replace(day=1)

        # Total purchase for the month
        total_purchase = Purchase.objects.filter(create_at__gte=start_date).aggregate(
            total_quantity=Sum('quantity'),
            total_amount=Sum('totalAmount')
        )

        # Total sales for the month
        total_sales = Selles.objects.filter(created_at__gte=start_date).aggregate(
            total_quantity=Sum('quantity'),
            total_amount=Sum('totalPrice')
        )
        
        # Total purchase cost for the month
        total_purchase_cost = Purchase.objects.filter(create_at__gte=start_date).aggregate(
            total_cost=Sum('productname__purchase_price')
        )['total_cost'] or 0

        # Total sales amount for the month
        total_sales_amount = total_sales['total_amount'] or 0
        
        # Profit calculation
        profit = total_sales_amount - total_purchase_cost

        context.update({
            'total_purchase': total_purchase,
            'total_sales': total_sales,
            'profit': profit,
            'start_date': start_date,
            'end_date': today
        })
        return context


class CustomDateReportView(TemplateView):
    template_name = 'report/DailyReport.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the custom start and end dates from the URL (query parameters)
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')

        # If dates are not provided, default to the last 7 days
        if not start_date_str or not end_date_str:
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=7)
        else:
            # Convert the date strings to date objects
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            except ValueError:
                context['error'] = "Invalid date format. Please use YYYY-MM-DD."
                return context

        # Query to get total purchase for the custom date range
        total_purchase = Purchase.objects.filter(create_at__range=[start_date, end_date]).aggregate(
            total_quantity=Sum('quantity'),
            total_amount=Sum('totalAmount')
        )

        # Query to get total sales for the custom date range
        total_sales = Selles.objects.filter(create_at__range=[start_date, end_date]).aggregate(
            total_quantity=Sum('quantity'),
            total_amount=Sum('totalPrice')
        )

        # Total purchase cost for the custom date range
        total_purchase_cost = Purchase.objects.filter(create_at__range=[start_date, end_date]).aggregate(
            total_cost=Sum('productname__purchase_price')
        )['total_cost'] or 0

        # Total sales amount for the custom date range
        total_sales_amount = total_sales['total_amount'] or 0

        # Profit calculation
        profit = total_sales_amount - total_purchase_cost

        # Add the data to context
        context.update({
            'total_purchase': total_purchase,
            'total_sales': total_sales,
            'profit': profit,
            'start_date': start_date,
            'end_date': end_date
        })

        return context