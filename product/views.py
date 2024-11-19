import pandas as pd
from django.core.paginator import Paginator, EmptyPage, Page
import openpyxl
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse, JsonResponse
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

#category Creater View 
class CategoryAndFileUploadView(FormView):
    model = Category
    form_class = CategoryForm
    template_name = "category/categorycreate.html"
    success_url = reverse_lazy('categorylist')  # Redirect after successful category creation

    def get(self, request, *args, **kwargs):
        # Handle GET request: Render both the category form and file upload form
        file_form = FileUploadForm()
        category_form = CategoryForm()
        return render(request, self.template_name, {
            "file_form": file_form,
            "category_form": category_form
        })

    def post(self, request, *args, **kwargs):
        """
        Handles POST request:
        - If file is uploaded, process the file (CSV/Excel)
        - If manual form is submitted, create a category
        """
        file_form = FileUploadForm(request.POST, request.FILES)
        category_form = CategoryForm(request.POST)

        if 'file' in request.FILES:  # If a file is uploaded
            if file_form.is_valid():
                uploaded_file = request.FILES['file']
                if uploaded_file.name.endswith('.csv'):
                    self.upload_csv(uploaded_file)
                    messages.success(request, "CSV file processed successfully!")
                elif uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
                    self.upload_excel(uploaded_file)
                   # messages.success(request, "Excel file processed successfully!")
                else:
                    messages.error(request, "Invalid file type. Only CSV and Excel files are allowed.")
                return redirect(self.success_url)  # Redirect after processing the file
            else:
                # If the file form is invalid, render the page with error messages
                messages.error(request, "Invalid file submission.")
                return render(request, self.template_name, {
                    'file_form': file_form,
                    'category_form': category_form,
                })

        elif category_form.is_valid():  # If manual category form is submitted
            category_name = category_form.cleaned_data["name"]
            category, created_category = Category.objects.get_or_create(name=category_name)
            if created_category:
                messages.success(request, f"Category '{category_name}' created successfully!")
            else:
                messages.info(request, f"Category '{category_name}' already exists.")
            return redirect(self.success_url)  # Redirect after category creation

        else:
            # If neither form is valid, render the page with error messages
            messages.error(request, "Please correct the errors below.")
            return render(request, self.template_name, {
                'file_form': file_form,
                'category_form': category_form,
            })

    def upload_csv(self, file):
        """Process uploaded CSV file and create categories"""
        df = pd.read_csv(file)
        for index, row in df.iterrows():
            category_name = row.get('name', None)
            if category_name:
                category, created_category = Category.objects.get_or_create(name=category_name)
                if created_category:
                    print(f"Category '{category_name}' created.")
                else:
                    print(f"Category '{category_name}' already exists.")

    def upload_excel(self, file):
        """Process uploaded Excel file and create categories"""
        df = pd.read_excel(file)
        for index, row in df.iterrows():
            category_name = row.get('name', None)
            if category_name:
                category, created_category = Category.objects.get_or_create(name=category_name)
                if created_category:
                    print(f"Category '{category_name}' created.")
                else:
                    print(f"Category '{category_name}' already exists.")
        print(f"Finished processing {len(df)} rows.")
    



    

                      




class categoryViewlist(ListView):
    model = Category
    template_name = "category/categoryList.html"
    paginate_by = 7

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # If you want to use 'category_list' as a custom context variable, that's fine
        context['Category'] = Category.objects.all()  # Rename 'object_list' to 'category_list'
        return context
        
#Category Update View 
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm  # The form used for editing
    template_name = 'category/categoryUpdate.html'  # The template to render the form
    context_object_name = 'category'  # The context variable used in the template

    # Redirect to the category list view upon successful update
    success_url = reverse_lazy('categorylist')

    def get_object(self, queryset=None):
       queryset = Category.objects.filter(pk=self.kwargs['pk'])
       try:
            obj=queryset.get()
       except Category.DoesNotExixt:
            raise Http404("category not found or inactive")
       return obj
       










              

#SubCategory View
class SubcategoryViewlist(ListView):
        model=SubCategory
        template_name="subcategory/SubcategoryList.html"
        paginate_by=10
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["subcategory"] = SubCategory.objects.all()
            return context

class SubCategoryAndFileUploadView(FormView):
    # This view will handle both SubCategory form submission and file uploads
    template_name = 'subcategory/Subcategorycreate.html'
    # We use both forms (manual form and file upload form)
    form_class = SubCategoryForm  # Default form for manual SubCategory creation
    file_form_class = FileUploadForm  # Form for file uploads
    
    # Success URL for file upload or form submission
    success_url = '/subcategoryList/'

    def get(self, request, *args, **kwargs):
        """
        Handles GET request. Renders both the file upload form and the manual SubCategory form.
        """
        file_form = FileUploadForm()
        subcategory_form = SubCategoryForm()
        return render(request, self.template_name, {
            'file_form': file_form,
            'subcategory_form': subcategory_form,
        })

    def post(self, request, *args, **kwargs):
        """
        Handles POST request for either file upload or manual SubCategory creation.
        It checks which form was submitted and processes it accordingly.
        """
        file_form = FileUploadForm(request.POST, request.FILES)
        subcategory_form = SubCategoryForm(request.POST)

        # If the file form was submitted
        if 'file' in request.FILES:
            if file_form.is_valid():
                uploaded_file = request.FILES['file']
                if uploaded_file.name.endswith('.csv'):
                    # Process CSV file
                    self.upload_csv(uploaded_file)
                    messages.success(request, "CSV file processed successfully!")
                elif uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
                    # Process Excel file
                    self.upload_excel(uploaded_file)
                    messages.success(request, "Excel file processed successfully!")
                else:
                    messages.error(request, "Invalid file type. Only CSV and Excel files are allowed.")
                return redirect('subcategory_list')  # Redirect after successful file processing
        elif subcategory_form.is_valid():
            # If the manual SubCategory form was submitted
            category_name = subcategory_form.cleaned_data['category']
            subcategory_name = subcategory_form.cleaned_data['name']
            category, created_category = Category.objects.get_or_create(name=category_name)
            
            if created_category:
                messages.success(request, f"Category '{category_name}' created.")
            else:
                messages.info(request, f"Category '{category_name}' already exists.")
            
            SubCategory.objects.create(name=subcategory_name, category=category)
            messages.success(request, f"SubCategory '{subcategory_name}' created successfully!")
            return redirect('subcategory_list')  # Redirect after successful form submission

        # If neither form is valid, render the page with error messages
        return render(request, self.template_name, {
            'file_form': file_form,
            'subcategory_form': subcategory_form,
        })

    def form_invalid(self, form):
        # Handle invalid form submissions
        #messages.error(self.request, "Please correct the errors below.")  # Error message
        return super().form_invalid(form)

    def upload_csv(self, file):
        # Read the CSV file
        df = pd.read_csv(file)

        print("CSV Columns:", df.columns)  # Debugging step

        # Iterate over the rows and create Category and SubCategory
        for index, row in df.iterrows():
            category_name = row.get('category', None)
            subcategory_name = row.get('subcategory', None)

            if not category_name or not subcategory_name:
                print(f"Row {index} is missing category or subcategory, skipping.")
                continue

            # Ensure category exists or create it
            category, created_category = Category.objects.get_or_create(name=category_name)
            if created_category:
                print(f"Category '{category_name}' created.")
            else:
                print(f"Category '{category_name}' already exists.")

            # Create SubCategory and link it to the Category
            subcategory, created_subcategory = SubCategory.objects.get_or_create(name=subcategory_name, category=category)
            if created_subcategory:
                print(f"SubCategory '{subcategory_name}' created and linked to '{category_name}'.")
            else:
                print(f"SubCategory '{subcategory_name}' already exists for '{category_name}'.")

        print(f"Finished processing {len(df)} rows.")

    def upload_excel(self, file):
        # Read the Excel file
        df = pd.read_excel(file)

        print("Excel Columns:", df.columns)  # Debugging step

        # Iterate over the rows and create Category and SubCategory
        for index, row in df.iterrows():
            category_name = row.get('category', None)
            subcategory_name = row.get('subcategory', None)

            if not category_name or not subcategory_name:
                print(f"Row {index} is missing category or subcategory, skipping.")
                continue

            # Ensure category exists or create it
            category, created_category = Category.objects.get_or_create(name=category_name)
            if created_category:
                print(f"Category '{category_name}' created.")
            else:
                print(f"Category '{category_name}' already exists.")

            # Create SubCategory and link it to the Category
            subcategory, created_subcategory = SubCategory.objects.get_or_create(name=subcategory_name, category=category)
            if created_subcategory:
                print(f"SubCategory '{subcategory_name}' created and linked to '{category_name}'.")
            else:
                print(f"SubCategory '{subcategory_name}' already exists for '{category_name}'.")

        print(f"Finished processing {len(df)} rows.")





    

   
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
        model=Product
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
            "categories": Category.objects.all(),  # Call .all() to get the queryset
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
            "categories": Category.objects.all(),
            "subcategories": SubCategory.objects.all(),
        }
        return render(request, self.template_name, context)  # Render the form with errors



class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm  # The form used for editing
    template_name = 'product/productupdate.html'  # The template to render the form
    context_object_name = 'product'  # The context variable used in the template

    # Redirect to the category list view upon successful update
    success_url = reverse_lazy('productlist')

    def get_object(self, queryset=None):
       queryset = Product.objects.filter(pk=self.kwargs['pk'])
       try:
            obj=queryset.get()
       except Product.DoesNotExixt:
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

    def get_context_data(self, **kwargs):
        """
        Pass the product data to the context if the product_id is passed in the URL.
        """
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('product_id')  # Get the product_id from the URL
        if product_id:
            # Make sure the product exists and pass it to the context
            product_instance = get_object_or_404(Product, id=product_id)
            context['product'] = product_instance
        return context

    def form_valid(self, form):
        """
        Override the form_valid method to include the Product when saving the Purchase.
        """
        product_id = self.kwargs.get('product_id')
        
        if product_id:
            try:
                # Get the product by its ID and ensure we don't have name collision
                product_instance = Product.objects.get(id=product_id)
                form.instance.product = product_instance  # Associate the product with the purchase
            except Product.DoesNotExist:
                # If the product doesn't exist, add an error and return the invalid form
                form.add_error(None, "Product does not exist.")
                return self.form_invalid(form)
        
        # Save the purchase object to the database
        self.object = form.save()

        # Redirect to the purchase receipt page for the created purchase
        return redirect('purchase_receipt', purchase_id=self.object.id)

    def form_invalid(self, form):
        # If the form is invalid, return to the form page with the errors
        return super().form_invalid(form)
    

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
    




class StockView(View):
    template_name = "Stock/Stock.html"
    
    def get(self, request, *args, **kwargs):
        # Get the filter parameters from the request (if any)
        product_name = request.GET.get('product_name', '')
        category = request.GET.get('category', '')
        min_quantity = request.GET.get('min_quantity', '')
        max_quantity = request.GET.get('max_quantity', '')

        # Build the filter conditions dynamically
        stock_queryset = Stock.objects.all()

        if product_name:
            stock_queryset = stock_queryset.filter(product__name__icontains=product_name)
        
        if category:
            stock_queryset = stock_queryset.filter(product__category__name__icontains=category)

        if min_quantity:
            stock_queryset = stock_queryset.filter(quantity__gte=min_quantity)

        if max_quantity:
            stock_queryset = stock_queryset.filter(quantity__lte=max_quantity)

        # Pagination
        paginator = Paginator(stock_queryset, 10)  # Show 10 items per page
        page = request.GET.get('page')
        stock_page = paginator.get_page(page)

        context = {
            'stock': stock_page,
            'paginator': paginator,
        }

        return render(request, self.template_name, context)



    
def export_stock_pdf(request):
        # Create the HTTP response with content type set to PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="stock_report.pdf"'

        # Create a PDF canvas
        c = canvas.Canvas(response, pagesize=letter)
        c.drawString(100, 750, "Stock Report")

        # Get the filtered queryset based on the filters passed in GET parameters
        product_name = request.GET.get('product_name', '')
        category = request.GET.get('category', '')
        min_quantity =request.GET.get('min_quantity', '')
        max_quantity = request.GET.get('max_quantity', '')

        stock_queryset = Stock.objects.all()

        if product_name:
            stock_queryset = stock_queryset.filter(product__name__icontains=product_name)

        if category:
            stock_queryset = stock_queryset.filter(product__category__name__icontains=category)

        if min_quantity:
            stock_queryset = stock_queryset.filter(quantity__gte=min_quantity)

        if max_quantity:
            stock_queryset = stock_queryset.filter(quantity__lte=max_quantity)

        # Write the stock data to the PDF
        y_position = 730
        for stock in stock_queryset:
            c.drawString(100, y_position, f"{stock.product.name} - {stock.quantity} in stock")
            y_position -= 20  # Move down the page for the next line

        # Save the PDF
        c.showPage()
        c.save()

        return response

def export_stock_excel(request):
        # Create a new workbook and sheet
        
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Stock Report"

        # Write headers
        ws.append(['Product Name', 'Category', 'Quantity', 'Created Date'])

        # Get the filtered queryset from the request parameters
        product_name =request.GET.get('product_name', '')
        category = request.GET.get('category', '')
        min_quantity =request.GET.get('min_quantity', '')
        max_quantity =request.GET.get('max_quantity', '')

        
        # Build the queryset based on filters
        stock_queryset = Stock.objects.all()

        if product_name:
            stock_queryset = stock_queryset.filter(product__name__icontains=product_name)

        if category:
            stock_queryset = stock_queryset.filter(product__category__name__icontains=category)

        if min_quantity:
            stock_queryset = stock_queryset.filter(quantity__gte=int(min_quantity))  # Ensure it's an integer

        if max_quantity:
            stock_queryset = stock_queryset.filter(quantity__lte=int(max_quantity))  # Ensure it's an integer

        # Write data to the Excel sheet
        for stock in stock_queryset:
            
            # Format the created_at to string in case it's a datetime object
          
            created_at = stock.created_at.strftime('%Y-%m-%d %H:%M:%S') if stock.created_at else ''
            ws.append([stock.product.name, stock.product.category.name, stock.quantity, created_at])

        # Create the HTTP response with content type set to Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="stock_report.xlsx"'

        # Save the workbook to the response
        wb.save(response)

        return response
