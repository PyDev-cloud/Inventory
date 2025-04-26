from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from .views import *
from product import views

urlpatterns = [
    path('Dashboard/', DashboardView.as_view(), name='dashboard'),
    path('category/',CategoryAndFileUploadView.as_view(),name='category'),
    path('categoryList/',categoryViewlist.as_view(),name="categorylist"),
    path('category/<int:pk>/edit/',CategoryUpdateView.as_view(),name="categoryupdate"),
 


    path('subcategory/',SubCategoryAndFileUploadView.as_view(),name='subcategory'),
    path('subcategoryList/',SubcategoryViewlist.as_view(),name="subcategorylist"),
    path('subcategory/<int:pk>/edit/',SubCategoryUpdateView.as_view(),name="subcategoryupdate"),
  
    
    path('product/', ProductCreateView.as_view(), name='product'),
    path('productList/',Productlist.as_view(),name="productlist"),
    path('productUpdate/<int:pk>/edit/',ProductUpdateView.as_view(),name="productupdate"),

    path('supplier/',SupplierCreate.as_view(),name='supplier'),
    path('supplierlist/',SupplierList.as_view(),name="SupplierList"),


     path("purchaseList/",PurchaseItemListView.as_view(),name="purchaseList"),
     path('create_purchase/', PurchaseCreateView.as_view(), name='create_purchase'),
     path('purchase/invoice/<int:invoice_id>/', PurchaseInvoiceDetailView.as_view(), name='purchase_invoice_detail'),
     path('purchase/receipt/<int:purchase_id>/', InvoiceView.as_view(), name="purchase_receipt"),  # Show a specific receipt
     path('get-purchase-price/', views.get_product_purchase_price, name='get_purchase_price'),







    path('customer/',CustomerCreate.as_view(),name='customer'),
    path('customerlist/',Customerlist.as_view(),name='customerlist'),
    path('customerUpdate/<int:pk>/edit/',CustomerUpdateView.as_view(),name="customerupdate"),
    

   
    
    
   

    
    path('create_selles/', SellesCreateView.as_view(), name='create_selles'),
    path('selles/invoice/<int:invoice_id>/', SellesInvoiceDetailView.as_view(), name='selles_invoice_detail'),







    path('selles/', SellesListView.as_view(), name='selles_list'),



    path('StockList/', StockView.as_view(), name='stocklist'),
    path('export/pdf/', export_stock_pdf, name='export_stock_pdf'),
    path('export/excel/', export_stock_excel, name='export_stock_excel'),
    #path("excel/",export_stock_excel,name="export_stock_excl"),


    path('daily/', DailyReportView.as_view(), name='daily_report'),
    path('weekly/', WeeklyReportView.as_view(), name='weekly_report'),
    path('monthly/', MonthlyReportView.as_view(), name='monthly_report'),
    #path('custom/<str:start_date>/<str:end_date>/', CustomDateReportView.as_view(), name='custom_date_report'),
    path('custom-date-report/', CustomDateReportView.as_view(), name='custom_date_report'),

    #path('upload/', FileUploadView.as_view(), name='file_upload'),

    #path('purchases/', PurchaseListView.as_view(), name='purchase_list'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
