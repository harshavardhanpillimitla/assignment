from rest_framework import viewsets
from rest_framework.response import Response
from .models import InvoiceItem, InvoiceBillSundry, InvoiceHeader
from .serializers import InvoiceHeaderSerializer
from django.shortcuts import get_object_or_404

class InvoiceCrud(viewsets.ViewSet):
    serializer_class = InvoiceHeaderSerializer
    def list(self, request):
        query_set = InvoiceHeader.objects.prefetch_related('invoiceitem_set', 'invoicebillsundry_set').all() 
        serializer = InvoiceHeaderSerializer(query_set, many=True)
        return Response(serializer.data)
        
    
    def create(self, request):
        serializer = InvoiceHeaderSerializer(data=request.data)
        if serializer.is_valid():
            invoice_header = serializer.save()
            return Response(serializer.data)
        else:
            return Response({"error":serializer.errors})
    
    def update(self, request, pk):
        invoice_header =   InvoiceHeader.objects.prefetch_related('invoiceitem_set', 'invoicebillsundry_set').get(id=pk)
        serializer = InvoiceHeaderSerializer(invoice_header, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"error":serializer.errors})
    
    def destroy(self, request, pk):
        invoice_header =   InvoiceHeader.objects.prefetch_related('invoiceitem_set', 'invoicebillsundry_set').filter(id=pk)
        invoice_header.delete()
        
        return Response({'sucess':True})
    
    def retrieve(self, request, pk):
        invoice_header =   InvoiceHeader.objects.prefetch_related('invoiceitem_set', 'invoicebillsundry_set').get(id=pk)
        serializer = InvoiceHeaderSerializer(invoice_header)
        
        return Response(serializer.data)