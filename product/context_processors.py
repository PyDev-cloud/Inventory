from .models import Stock

def low_stock_notification(request):
    # Get products with quantity less than or equal to 5
    low_stock_items = Stock.objects.filter(quantity__lte=5)
    return {'low_stock_items': low_stock_items}