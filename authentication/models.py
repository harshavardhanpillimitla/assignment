from django.db import models

# Create your models here.
# Invoice Header
# Id: UUID
# Date: string (UTC)
# InvoiceNumber: number
# CustomerName: string
# BillingAddress: string
# ShippingAddress: string
# GSTIN: string
# TotalAmount: Decimal
class InvoiceHeader(models.Model):
    date =  models.CharField(max_length=30)
    invoice_number = models.IntegerField(unique=True)
    customer_name = models.CharField(max_length=30)
    billing_address = models.CharField(max_length=30)
    shipping_address = models.CharField(max_length=30)
    gstin = models.CharField(max_length=30)
    total_amount = models.FloatField()


class InvoiceItem(models.Model):
    invoice_header = models.ForeignKey(InvoiceHeader, on_delete = models.DO_NOTHING)
    item_name = models.CharField(max_length=30)
    quantity = models.FloatField()
    amount = models.FloatField()

class InvoiceBillSundry(models.Model):
    invoice_header = models.ForeignKey(InvoiceHeader, on_delete = models.DO_NOTHING)
    billing_sundry_name = models.CharField(max_length=30)
    amount = models.FloatField()
    # for addition to bill 'a' , subration from bill 's'
    type_of_operation =  models.CharField(max_length=1, default='s')





# Invoice Items
# Id: UUID
# itemName: string
# Quantity: decimal
# Price: decimal
# Amount: decimal

# Invoice BillSundry
# Id: UUID
# billSundryName: string
# Amount: decimal