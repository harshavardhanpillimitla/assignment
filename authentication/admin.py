from django.contrib import admin
from .models import InvoiceItem, InvoiceBillSundry, InvoiceHeader

# Register your models here.
admin.site.register(InvoiceItem)
admin.site.register(InvoiceBillSundry)
admin.site.register(InvoiceHeader)
