from collections import defaultdict
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
import pandas as pd
from django.core.paginator import Paginator, EmptyPage, Page
import openpyxl
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from datetime import datetime
from datetime import date
from django.db.models.functions import TruncMonth
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound

from django.views.generic import *
from .models import *
from .forms import *

#category Creater View 
class categoryViewlist(LoginRequiredMixin,ListView):
    model = Category
    template_name = "category/categoryList.html"
    paginate_by = 7

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # If you want to use 'category_list' as a custom context variable, that's fine
        context['Category'] = Category.objects.all()  # Rename 'object_list' to 'category_list'
        return context
        
#Category Update View 
class CategoryUpdateView(LoginRequiredMixin,UpdateView):
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
       except Category.DoesNotExist:
            raise Http404("category not found or inactive")
       return obj



class CategoryAndFileUploadView(LoginRequiredMixin,FormView):
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
    

        

#SubCategory View
class SubcategoryViewlist(LoginRequiredMixin,ListView):
        model=SubCategory
        template_name="subcategory/SubcategoryList.html"
        paginate_by=10
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["subcategory"] = SubCategory.objects.all()
            return context

class SubCategoryAndFileUploadView(LoginRequiredMixin,FormView):
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
                return redirect('subcategorylist')  # Redirect after successful file processing
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
            return redirect('subcategorylist')  # Redirect after successful form submission

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
class SubCategoryUpdateView(LoginRequiredMixin,UpdateView):
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
       except SubCategory.DoesNotExist:
            raise Http404("category not found or inactive")
       return obj
    


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/productcreate.html'
    success_url = '/productList/'

    def form_valid(self, form):
        # Custom validation or processing before saving the form
        product = form.save(commit=False)  # Do not save yet
        product.save()  # Now save
        return super().form_valid(form)

    def form_invalid(self, form):
        # Handle invalid form (optional logging or other processing)
        return super().form_invalid(form)
    
#product List View 
class Productlist(LoginRequiredMixin,ListView):
        model=Product
        template_name="product/productList.html"
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["product"] = self.model.objects.all()
            return context


# Update a Product (for editing an existing product)
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/productcreate.html'  # Your template to render the form
    success_url = reverse_lazy('productlist')  # Redirect to the product list after update

    def form_valid(self, form):
        # Add additional logic here if needed before saving the updated form
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin,UpdateView):
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
       except Product.DoesNotExist:
            raise Http404("category not found or inactive")
       return obj





class SupplierCreate(LoginRequiredMixin,CreateView):
    model=Supplier
    form_class=SupplierForm
    template_name="supplier/SupplierCreate.html"
    success_url=reverse_lazy('SupplierList')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Category created successfully!")  # Success message
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")  # Error message
        return super().form_invalid(form)
    
class SupplierList(LoginRequiredMixin,ListView):
        model=Supplier
        template_name="supplier/supplierList.html"
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["supplier"] = self.model.objects.all()
            return context

#Customer List View
class Customerlist(LoginRequiredMixin,ListView):
        model=Customer
        template_name="customer/customerlist.html"
        
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["customer"] = self.model.objects.all()
            return context


class CustomerCreate(LoginRequiredMixin,CreateView):
    model=Customer
    form_class=CustomarForm
    template_name="customer/Customercreate.html"
    success_url=reverse_lazy('customerlist')
    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Customer created successfully!")  # Success message
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")  # Error message
        return super().form_invalid(form)


class CustomerUpdateView(LoginRequiredMixin,UpdateView):
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
       except Customer.DoesNotExist:
            raise Http404("category not found or inactive")
       return obj




class PurchaseCreateView(LoginRequiredMixin,CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'purchase/Purchasecreate.html'
    success_url = reverse_lazy('purchaseList')

    def form_valid(self, form):
        # Start a transaction to ensure atomicity
        with transaction.atomic():
            # Save the Purchase object first
            self.object = form.save()

            # Create or get the PurchaseItem formset based on the current Purchase instance
            purchase_item_formset = PurchaseItemFormSet(self.request.POST, queryset=PurchaseItem.objects.filter(purchase=self.object))

            if purchase_item_formset.is_valid():
                for idx, purchase_item_form in enumerate(purchase_item_formset):
                    # Skip empty forms
                    if not purchase_item_form.cleaned_data.get('product'):
                        print(f"Form {idx} is missing product.")  # Debugging line
                        continue  # Skip saving this item if no product is selected

                    # Save the valid form data
                    purchase_item = purchase_item_form.save(commit=False)
                    purchase_item.purchase = self.object  # Link each item to the purchase
                    purchase_item.save()
                   # After saving the item, update stock quantity for the product
                    product = purchase_item.product
                    purchased_quantity = purchase_item.quantity

                    # Update or create the stock entry
                    stock, created = Stock.objects.get_or_create(product=product)

                    # Update the stock quantity by adding the purchased quantity
                    stock.quantity += purchased_quantity
                    stock.save()
                # After saving the items, recalculate the totalAmount and dueAmount for the purchase
                self.object.product_totalAmount = sum(item.product_totalAmount for item in self.object.purchase_items.all())
                self.object.dueAmount = (self.object.product_totalAmount - self.object.discount)- self.object.paidAmount
                self.object.alltotalAmount=sum(item.product_totalAmount for item in self.object.purchase_items.all())
                self.object.save()  # Save the updated Purchase instance

                # Ensure the invoice is created if it does not exist
                if not self.object.invoice:
                    invoice = PurchaseInvoice.objects.create(
                        invoice_number=str(uuid.uuid4()),  # Unique invoice number
                        total_amount=self.object.alltotalAmount,
                        discount=self.object.discount,
                        paid_amount=self.object.paidAmount,
                    )
                    self.object.invoice = invoice
                    self.object.save()

                # Now the invoice is set, redirect to the purchase invoice detail page
                return redirect('purchase_invoice_detail', invoice_id=self.object.invoice.id)

            # If formset is invalid, re-render the page with errors
            return self.render_to_response(self.get_context_data(form=form, purchase_item_formset=purchase_item_formset))

        # If the form is not valid, re-render the page with errors
        return self.render_to_response(self.get_context_data(form=form, purchase_item_formset=purchase_item_formset))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['purchase_item_formset'] = PurchaseItemFormSet(queryset=self.object.purchase_items.all())
        else:
            context['purchase_item_formset'] = PurchaseItemFormSet(queryset=PurchaseItem.objects.none())  # Empty formset for new purchases
        return context
    



def get_product_purchase_price(request):
    product_id = request.GET.get('product_id')
    try:
        product = Product.objects.get(id=product_id)
        return JsonResponse({'purchase_price': float(product.purchase_price)})
    except Product.DoesNotExist:
        return JsonResponse({'purchase_price': 0})



class PurchaseUpdateView(UpdateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'purchase/update_purchase.html'
    success_url = reverse_lazy('purchase_list')  # Update this to your actual success URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['purchase_item_formset'] = PurchaseItemFormSet(self.request.POST, queryset=PurchaseItem.objects.filter(purchase=self.object))
        else:
            context['purchase_item_formset'] = PurchaseItemFormSet(queryset=PurchaseItem.objects.filter(purchase=self.object))
        context['is_update'] = True
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['purchase_item_formset']

        if formset.is_valid():
            purchase = form.save(commit=False)
            total = 0

            # Recalculate totals
            for item_form in formset:
                product = item_form.cleaned_data.get('product')
                quantity = item_form.cleaned_data.get('quantity')
                unit_price = item_form.cleaned_data.get('unit_price')
                if product and quantity and unit_price:
                    total += quantity * unit_price

            discount = form.cleaned_data.get('discount') or 0
            paid = form.cleaned_data.get('paidAmount') or 0
            grand_total = total - discount
            due = grand_total - paid

            purchase.alltotalAmount = total
            purchase.dueAmount = due
            purchase.save()

            # Save the formset
            items = formset.save(commit=False)
            for item in items:
                item.purchase = purchase
                item.product_totalAmount = item.unit_price * item.quantity
                item.save()

            # Optionally delete removed forms
            for item in formset.deleted_objects:
                item.delete()

            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))
    




# Create a view to show the Purchase Invoice
class PurchaseInvoiceDetailView(LoginRequiredMixin, CreateView):
    model = Purchase
    template_name = 'Receipt/PurchaseInvoice.html'  # The template where the invoice is shown
    form_class=PurchaseInvoiceForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice_id = self.kwargs['invoice_id']
        invoice = PurchaseInvoice.objects.get(id=invoice_id)
        context['invoice'] = invoice

        purchases = Purchase.objects.filter(invoice=invoice)
        context['purchases'] = purchases
        return context
    






class SellesInvoiceDetailView(LoginRequiredMixin, CreateView):
    model = Selles
    template_name = 'Receipt/SellesInvoice.html'  # The template where the invoice is shown
    form_class=SellesInvoiceForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice_id = self.kwargs['invoice_id']
        invoice = SellesInvoice.objects.get(id=invoice_id)
        context['invoice'] = invoice
        selles = Selles.objects.filter(invoice=invoice)
        context['selles'] = selles
        return context




class SellesCreateView(LoginRequiredMixin, CreateView):
    model = Selles
    form_class = SellesForm
    template_name = 'sells/sellsCreate.html'
    success_url = reverse_lazy('')  # You should define the actual success URL
    
    def form_valid(self, form):
        # Initialize formset with submitted POST data
        selles_item_formset = sellesItemForm(self.request.POST, queryset=SellesItem.objects.none())

        if not selles_item_formset.is_valid():
            return self.render_to_response(self.get_context_data(form=form, selles_item_formset=selles_item_formset))

        form_items = []
        product_quantities = defaultdict(int)
        stock_errors = False

        # Step 1: Collect valid items and aggregate quantity per product
        for item_form in selles_item_formset:
            if not item_form.cleaned_data:
                continue  # Skip empty or deleted forms

            product = item_form.cleaned_data.get('product')
            quantity = item_form.cleaned_data.get('quantity')

            if not product or quantity in [None, 0]:
                continue  # Skip invalid entries

            form_items.append(item_form)
            product_quantities[product] += quantity

        if not product_quantities:
            form.add_error(None, "At least one valid item with sufficient stock is required.")
            return self.render_to_response(self.get_context_data(form=form, selles_item_formset=selles_item_formset))

        # Step 2: Validate stock for each unique product
        stock_map = {}

        for product, total_quantity in product_quantities.items():
            try:
                stock = Stock.objects.get(product=product)
                stock_map[product] = stock
            except Stock.DoesNotExist:
                for f in form_items:
                    if f.cleaned_data.get('product') == product:
                        f.add_error('product', f"No stock record found for {product}")
                stock_errors = True
                continue

            if stock.quantity < total_quantity:
                for f in form_items:
                    if f.cleaned_data.get('product') == product:
                        f.add_error('quantity', f"Insufficient stock for {product.name}. Available: {stock.quantity}")
                stock_errors = True

        if stock_errors:
            return self.render_to_response(self.get_context_data(form=form, selles_item_formset=selles_item_formset))

        # Step 3: Save everything in a transaction
        with transaction.atomic():
            self.object = form.save()

            for item_form in form_items:
                product = item_form.cleaned_data['product']
                quantity = item_form.cleaned_data['quantity']

                # Save item and link to the Selles instance
                item = item_form.save(commit=False)
                item.selles = self.object
                item.save()

                # Reduce stock
                stock = stock_map[product]
                stock.quantity -= quantity
                stock.save()

            # Step 4: Update totals
            total_amount = sum(item.totalAmount for item in self.object.selles_items.all())
            paid_amount = self.object.paidAmount or Decimal('0.00')
            discount_amount = self.object.discountAmount or Decimal('0.00')

            self.object.totalPrice = total_amount
            self.object.grand_total = total_amount - discount_amount
            self.object.dueAmount = self.object.grand_total - paid_amount
            self.object.save()

            # Step 5: Create invoice if not exists
            if not self.object.invoice:
                invoice = SellesInvoice.objects.create(
                    invoice_number=str(uuid.uuid4()),
                    total_amount=self.object.totalPrice,
                    discount=self.object.discountAmount,
                    paid_amount=self.object.paidAmount,
                    dueAmount=self.object.dueAmount,
                )
                self.object.invoice = invoice
                self.object.save()

        return redirect('selles_invoice_detail', invoice_id=self.object.invoice.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'object') and self.object:
            context['selles_item_formset'] = sellesItemForm(queryset=self.object.selles_items.all())
        else:
            context['selles_item_formset'] = sellesItemForm(queryset=SellesItem.objects.none())
        return context


class SellesListView(LoginRequiredMixin, ListView):
    model = Selles
    template_name = 'sells/sellesList.html'  # Template to render the list
    context_object_name = 'sales'  # Context variable name for the list

    # You can add pagination if needed
    paginate_by = 10  # Adjust the number of items per page if required
    

        
    



class DailyReportView(LoginRequiredMixin,TemplateView):
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


class WeeklyReportView(LoginRequiredMixin, TemplateView):
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

class MonthlyReportView(LoginRequiredMixin, TemplateView):
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


class CustomDateReportView(LoginRequiredMixin, TemplateView):
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
    






class StockView(LoginRequiredMixin, View):
    template_name = "Stock/Stock.html"
    
    def get(self, request, *args, **kwargs):
        # Get the filter parameters from the request (if any)
        product_name = request.GET.get('product_name', '')
        category = request.GET.get('category', '')
        min_quantity = request.GET.get('min_quantity', '')
        max_quantity = request.GET.get('max_quantity', '')

        # Build the filter conditions dynamically
        stock_queryset = Stock.objects.all()
        print("Initial queryset (no filters):", stock_queryset.query)

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


class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'Dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_year = timezone.now().year
        current_month = timezone.now().month
        
        # Total Purchases
        total_purchases = Purchase.objects.filter(created_at__month=current_month, created_at__year=current_year)

        total_purchase_amount = total_purchases.aggregate(Sum('alltotalAmount'))['alltotalAmount__sum'] or 0
        total_purchase_paid = total_purchases.aggregate(Sum('paidAmount'))['paidAmount__sum'] or 0
        total_purchase_due = total_purchase_amount - total_purchase_paid

        # Total Sales
        total_sales = Selles.objects.filter(created_at__month=current_month, created_at__year=current_year)
        total_sales_amount = total_sales.aggregate(Sum('totalPrice'))['totalPrice__sum'] or 0
        total_sales_paid = total_sales.aggregate(Sum('paidAmount'))['paidAmount__sum'] or 0
        #total_profit=total_sales.aggregate(Sum('profit'))['profit__sum'] or 0
        total_sales_due = total_sales_amount - total_sales_paid
        
        

        # Total Invoices
        total_invoices = PurchaseInvoice.objects.filter(created_at__month=current_month, created_at__year=current_year)

        total_invoice_amount = total_invoices.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        total_invoice_paid = total_invoices.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
        total_invoice_due = total_invoice_amount - total_invoice_paid

        # Total Profit
        total_profit = total_sales_amount - total_purchase_amount  # Profit = Sales - Purchases

        # Daily Sales
        today_sales = Selles.objects.filter(created_at=date.today())
        daily_sales_amount = today_sales.aggregate(Sum('totalPrice'))['totalPrice__sum'] or 0
        #daily_profit=today_sales.aggregate(Sum('profit'))['profit__sum'] or 0

        # Daily Purchases
        today_purchases = Purchase.objects.filter(created_at=date.today())
        daily_purchase_amount = today_purchases.aggregate(Sum('alltotalAmount'))['alltotalAmount__sum'] or 0

      


        # Daily Invoices
        today_invoices = PurchaseInvoice.objects.filter(created_at=date.today())
        daily_invoice_amount = today_invoices.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

        context.update({
            'total_purchase_amount': total_purchase_amount,
            'total_purchase_paid': total_purchase_paid,
            'total_purchase_due': total_purchase_due,
            'total_sales_amount': total_sales_amount,
            'total_sales_paid': total_sales_paid,
            'total_sales_due': total_sales_due,
            'total_invoice_amount': total_invoice_amount,
            'total_invoice_paid': total_invoice_paid,
            'total_invoice_due': total_invoice_due,
            'total_profit': total_profit,
            'daily_sales_amount': daily_sales_amount,
            'daily_purchase_amount': daily_purchase_amount,
            'daily_invoice_amount': daily_invoice_amount,
            'today_sales': today_sales,
            'today_purchases': today_purchases,
            'today_invoices': today_invoices,
            'total_profit':total_profit,
            
        })

        return context
    




class PurchaseItemListView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = 'purchase/purchaseList.html'
    context_object_name = 'purchases'

    def get_queryset(self):
        return Purchase.objects.prefetch_related('purchase_items__product').select_related('supplier')




# views.py
class SellesItemListView(LoginRequiredMixin, ListView):
    model = Selles
    template_name = 'sells/sellesList.html'  # Use correct path
    context_object_name = 'sales'

    def get_queryset(self):
        return Selles.objects.prefetch_related('selles_items__product').select_related('customer')








class Custom404View(TemplateView):
    template_name = 'errors/404.html'

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['status'] = 404
        return super().render_to_response(context, **response_kwargs)







class InvoiceView(LoginRequiredMixin,TemplateView):
    template_name = 'Receipt/purchaseRecipt.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        purchase_id = self.kwargs.get('purchase_id')
        if purchase_id:
            # Attempt to get the invoice for the purchase
            purchase_invoice = PurchaseInvoice.objects.filter(purchase__id=purchase_id).first()
            
            if purchase_invoice:
                context['purchase_invoice'] = purchase_invoice
            else:
                context['purchase_invoice'] = None  # Handle the case when no invoice exists for this purchase

        return context
    
