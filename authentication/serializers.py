from rest_framework import serializers
from .models import InvoiceItem, InvoiceBillSundry, InvoiceHeader

class InvoiceItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvoiceItem
        fields = [ "item_name",
              "quantity",
              "price", "amount"]
    
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
        data['amount'] = data.get('price',0) * data.get('quantity',0)
        return data
         


class InvoiceBillSundrySerializer(serializers.ModelSerializer):

    class Meta:
        model = InvoiceBillSundry
        fields = [ "billing_sundry_name",
          "amount",
          "type_of_operation"]
    
class InvoiceHeaderGetSerializer(serializers.ModelSerializer):
    invoice_items = InvoiceItemSerializer(many=True)
    invoice_billsundry = InvoiceBillSundrySerializer(many=True)
    class Meta:
        model = InvoiceHeader
        fields = ["date", "invoice_number","customer_name", "billing_address" , "shipping_address", "gstin", "total_amount", "invoice_items", "invoice_billsundry"]


class InvoiceHeaderSerializer(serializers.ModelSerializer):
    invoice_items = InvoiceItemSerializer(many=True, write_only=True)
    invoice_billsundry = InvoiceBillSundrySerializer(many=True, write_only=True)
    invoiceitems = serializers.SerializerMethodField()
    invoicebillsundry = serializers.SerializerMethodField()

    def get_invoiceitems(self, obj):
        return InvoiceItemSerializer(obj.invoiceitem_set.all(), many=True).data

    def get_invoicebillsundry(self,obj):
        return InvoiceBillSundrySerializer(obj.invoicebillsundry_set.all(), many=True).data



    
    class Meta:
        model = InvoiceHeader
        fields = ["id","date", "invoice_number","customer_name", "billing_address" , "shipping_address", "gstin", "total_amount", "invoice_items", "invoice_billsundry", 'invoiceitems',"invoicebillsundry"]

    def create(self, validated_data):
        invoice_items = validated_data.pop('invoice_items', [])
        invoice_billsundry = validated_data.pop('invoice_billsundry', [])
        invoice_header = InvoiceHeader.objects.create(**validated_data)
        
        sum_invoice_amount = 0
        sum_sundry_amount = 0
        
        bulk_create_invoice_items = []
        for item in invoice_items:
            item.update({'invoice_header':invoice_header})
            serializer =  InvoiceItemSerializer(data=item)
            if(serializer.is_valid()):
                sum_invoice_amount += serializer.validated_data.get('amount')
                bulk_create_invoice_items.append(InvoiceItem(invoice_header=invoice_header,**serializer.validated_data))

        bulk_create_invoice_billsundry = []
        print(invoice_billsundry)
        for sundry in invoice_billsundry:
            temp=sundry
            sundry.update({'invoice_header':invoice_header})
            serializer =  InvoiceBillSundrySerializer(data=sundry)
            if(serializer.is_valid()):
                if(serializer.validated_data.get('type_of_operation')=='a'):
                    sum_sundry_amount += serializer.validated_data.get('amount')
                else:
                    sum_sundry_amount -=  serializer.validated_data.get('amount')
                bulk_create_invoice_billsundry.append(InvoiceBillSundry(invoice_header=invoice_header,**serializer.validated_data))

        invoice_header.total_amount = sum_invoice_amount + sum_sundry_amount
        invoice_header.save()

        InvoiceItem.objects.bulk_create(bulk_create_invoice_items)
        InvoiceBillSundry.objects.bulk_create(bulk_create_invoice_billsundry)
        
        return invoice_header

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(representation)
        return representation

    
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
                bulk_create_invoice_items.append(InvoiceItem(invoice_header=instance,**serializer.validated_data))

        bulk_create_invoice_billsundry = []
        for sundry in invoice_billsundry:
            serializer =  InvoiceBillSundrySerializer(data=sundry)
            if(serializer.is_valid()):
                if(serializer.validated_data.get('type_of_operation')=='a'):
                    sum_sundry_amount += serializer.validated_data.get('amount')
                else:
                    sum_sundry_amount -=  serializer.validated_data.get('amount')
                bulk_create_invoice_billsundry.append(InvoiceBillSundry(invoice_header=instance,**serializer.validated_data))
                
        instance.amount = sum_invoice_amount + sum_sundry_amount
        instance.save()

        InvoiceItem.objects.bulk_create(bulk_create_invoice_items, ignore_conflicts=True)
        InvoiceBillSundry.objects.bulk_create(bulk_create_invoice_billsundry, ignore_conflicts=True)


        return instance

        


    


