# coding=utf-8
from rest_framework import serializers
from .models import sale
from .models import saledetailreportsmodel
from .models import salereportsmodel
from .models import stockmovementreportsmodel
from .models import stockmovement
from .models import saledetail
from django.core.serializers.json import DjangoJSONEncoder
import datetime
from rest_framework.serializers import (
    CharField,
    ChoiceField,
    IntegerField,
    DecimalField,
    ModelField,
    FloatField,
    models,
    postgres_fields,
)
# from rest_framework.utils.field_mapping import (
#     ClassLookupDict,
#     needs_label,
#     NUMERIC_FIELD_TYPES,
#     validators,
# )

class saleSerializer (serializers.ModelSerializer):
    date_ = serializers.DateTimeField(required=False, read_only=True)
    ficheno  = serializers.CharField(required=False, read_only=True)
    payplancode = serializers.CharField(required=False, read_only=True)
    salesmanname = serializers.CharField(required=False, read_only=True)
    payplantype = serializers.CharField(required=False, read_only=True)
    code  = serializers.CharField(required=False, read_only=True)
    definition_  = serializers.CharField(required=False, read_only=True)
    specode = serializers.CharField(required=False, read_only=True)
    city  = serializers.CharField(required=False, read_only=True)
    totaldiscounts = serializers.FloatField()
    totaldiscounted = serializers.FloatField()
    totalvat = serializers.FloatField()
    grosstotal = serializers.FloatField()
    nettotal = serializers.FloatField()
    reportnet   = serializers.FloatField()
    genexp1  = serializers.CharField(required=False, read_only=True)
    genexp2  = serializers.CharField(required=False, read_only=True)
    genexp3 = serializers.CharField(required=False, read_only=True)
    genexp4  = serializers.CharField(required=False, read_only=True)
    projectcode  = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = sale
        fields = '__all__'
        #############


class saledetailSerializer(serializers.Serializer):
    date_ = serializers.DateTimeField(required=False, read_only=True)
    logicalref = serializers.IntegerField(required=False, read_only=True)
    productcode  = serializers.CharField(required=False, read_only=True)
    productname = serializers.CharField(required=False, read_only=True)
    brandname  = serializers.CharField(required=False, read_only=True)
    typename  = serializers.CharField(required=False, read_only=True)
    showasnew = serializers.IntegerField()
    productgender  = serializers.CharField(required=False, read_only=True)
    productmaterial  = serializers.CharField(required=False, read_only=True)
    productstyle  = serializers.CharField(required=False, read_only=True)
    producttype  = serializers.CharField(required=False, read_only=True)
    productionstatus  = serializers.CharField(required=False, read_only=True)
    model  = serializers.CharField(required=False, read_only=True)
    colourcode  = serializers.CharField(required=False, read_only=True)
    sizecode  = serializers.CharField(required=False, read_only=True)
    clientcode  = serializers.CharField(required=False, read_only=True)
    definition_  = serializers.CharField(required=False, read_only=True)
    specode  = serializers.CharField(required=False, read_only=True)
    city  = serializers.CharField(required=False, read_only=True)
    amount = serializers.FloatField()
    shippedamount  = serializers.FloatField()
    price  = serializers.FloatField()
    total  = serializers.FloatField()
    distcost  = serializers.FloatField()
    distdisc  = serializers.FloatField()
    vat  = serializers.FloatField()
    vatamnt  = serializers.FloatField()
    vatmatrah  = serializers.FloatField()
    prcurr = serializers.IntegerField()
    prprice = serializers.FloatField()
    totalamount = serializers.FloatField()

    class Meta:
        model = saledetail
        fields = '__all__'




class stockmovementSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(required=False, read_only=True)
    ivenno = serializers.IntegerField(required=False, read_only=True)
    producttype  = serializers.CharField(required=False, read_only=True)
    productname = serializers.CharField(required=False, read_only=True)
    brandname  = serializers.CharField(required=False, read_only=True)
    typename  = serializers.CharField(required=False, read_only=True)
    sizecode  = serializers.CharField(required=False, read_only=True)
    showasnew = serializers.IntegerField()
    productgender  = serializers.CharField(required=False, read_only=True)
    productmaterial  = serializers.CharField(required=False, read_only=True)
    productstyle  = serializers.CharField(required=False, read_only=True)
    productionstatus  = serializers.CharField(required=False, read_only=True)
    model  = serializers.CharField(required=False, read_only=True)
    colourcode  = serializers.CharField(required=False, read_only=True)
    productcode  = serializers.CharField(required=False, read_only=True)
    reserved = serializers.FloatField()
    actporder  = serializers.FloatField()
    onhand  = serializers.FloatField()
    salamnt  = serializers.FloatField()
    salcash  = serializers.FloatField()
    salcurr  = serializers.FloatField()
 
    class Meta:
        model = stockmovement
        fields = '__all__'


class saledetailreportsmodelSerializer(serializers.Serializer):
    amountbycustomers = serializers.DictField()
    amountbybrandnames = serializers.DictField()
    amountsbyproductcode = serializers.DictField()
    amountbygenders = serializers.DictField()

    salesbycity = serializers.DictField()
    totalamountbycustomers = serializers.DictField()
    totalamountbycity = serializers.DictField()

    typeamountbybrandnames = serializers.DictField()

    vatmatrahbybrands = serializers.DictField()
    vatmatrahbyproducts = serializers.DictField()
    vatmatrahbytypes = serializers.DictField()



    class Meta:
        model = saledetailreportsmodel

class salereportsmodelSerializer(serializers.Serializer):
    payplansummaries = serializers.DictField()
    citynettotalsummaries = serializers.DictField()
    salesmansummaries = serializers.DictField()
    regiontotalsummaries = serializers.DictField()
    salesmanbyregions = serializers.DictField()
    salesbyregions = serializers.DictField()
    salesmanbycities = serializers.DictField()
    customerpayplans = serializers.DictField()

    class Meta:
        model = salereportsmodel


class stockmovementreportsmodelSerializer(serializers.Serializer):
    productonhands = serializers.DictField()
    productreserves = serializers.DictField()
    productacporders = serializers.DictField()
    brandonhands = serializers.DictField()
    brandreserves = serializers.DictField()
    brandactporders = serializers.DictField()



    class Meta:
        model = stockmovementreportsmodel

