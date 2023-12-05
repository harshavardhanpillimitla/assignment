from rest_framework import serializers
from .models import InvoiceItem, InvoiceBillSundry, InvoiceHeader

class InvoiceItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvoiceItem
        fields = '__all__'
    
    def validate_price(self, value):
        if (value<=0):
            raise serializers.ValidationError(
            'price must be grater than zero'
            )
        return value
    
    def validate_quantity(self, value):
        if (value<=0):
            raise serializers.ValidationError(
            'quantity must be grater than zero'
            )
        return value
    
    def validate(self, data):
        data['amount'] = data.get('price') * data.get('quantity')
        return data
         


class InvoiceBillSundrySerializer(serializers.ModelSerializer):

    class Meta:
        model = InvoiceBillSundry
        fields = '__all__'


class InvoiceHeaderSerializer(serializers.ModelSerializer):
    invoice_items = InvoiceItemSerializer(many=True)
    invoice_billsundry = InvoiceBillSundrySerializer(many=True)
    class Meta:
        model = InvoiceHeader
        fields = ['date', 'invoice_number','customer_name', 'billing_address' , 'shipping_address', 'gstin', 'total_amount', 'invoice_items', 'invoice_billsundry']

    def create(self, validated_data):
        invoice_items = validated_data.pop('invoice_items', [])
        invoice_billsundry = validated_data.pop('invoice_billsundry', [])
        invoice_header = InvoiceHeader.objects.create(**validated_data)
        
        sum_invoice_amount = 0
        sum_sundry_amount = 0
        
        bulk_create_invoice_items = []
        for item in invoice_items:
            serializer =  InvoiceItemSerializer(data=item)
            if(serializer.is_valid()):
                sum_invoice_amount += serializer.validated_data.get('amount')
                bulk_create_invoice_items.append(InvoiceItem(invoice_header=invoice_header,**serializer.validated_data))

        bulk_create_invoice_billsundry = []
        for sundry in invoice_billsundry:
            serializer =  InvoiceBillSundrySerializer(data=sundry)
            if(serializer.is_valid()):
                if(serializer.validated_data.get('type_of_operation')=='a'):
                    sum_sundry_amount += serializer.validated_data.get('amount')
                else:
                    sum_sundry_amount -=  serializer.validated_data.get('amount')
                bulk_create_invoice_billsundry.append(InvoiceBillSundry(invoice_header=invoice_header,**serializer.validated_data))

        invoice_header.amount = sum_invoice_amount + sum_sundry_amount
        invoice_header.save()

        InvoiceItem.objects.bulk_create(bulk_create_invoice_items)
        InvoiceBillSundry.objects.bulk_create(bulk_create_invoice_billsundry)

        return invoice_header

    
    def update(self,instance, validated_data):
        invoice_items = validated_data.pop('invoice_items', [])
        invoice_billsundry = validated_data.pop('invoice_billsundry', [])
        invoice_header = InvoiceHeader.objects.filter(id=instance.id).update(**validated_data)

        sum_invoice_amount = 0
        sum_sundry_amount = 0
        
        bulk_create_invoice_items = []
        for item in invoice_items:
            serializer =  InvoiceItemSerializer(data=item)
            if(serializer.is_valid()):
                sum_invoice_amount += serializer.validated_data.get('amount')
                bulk_create_invoice_items.append(InvoiceItem(invoice_header=invoice_header,**serializer.validated_data))

        bulk_create_invoice_billsundry = []
        for sundry in invoice_billsundry:
            serializer =  InvoiceBillSundrySerializer(data=sundry)
            if(serializer.is_valid()):
                if(serializer.validated_data.get('type_of_operation')=='a'):
                    sum_sundry_amount += serializer.validated_data.get('amount')
                else:
                    sum_sundry_amount -=  serializer.validated_data.get('amount')
                bulk_create_invoice_billsundry.append(InvoiceBillSundry(invoice_header=invoice_header,**serializer.validated_data))
                
        invoice_header.amount = sum_invoice_amount + sum_sundry_amount
        invoice_header.save()

        InvoiceItem.objects.bulk_create(bulk_create_invoice_items, ignore_conflicts=True)
        InvoiceBillSundry.objects.bulk_create(bulk_create_invoice_billsundry, ignore_conflicts=True)


        return invoice_header

        


    


