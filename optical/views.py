# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.serializers import serialize
from django.core import serializers
from .models import sale
from .models import saledetail
from .models import saledetailreportsmodel
from .models import stockmovement
from .models import salereportsmodel
from .models import stockmovementreportsmodel
from .serializers import saleSerializer
from .serializers import salereportsmodelSerializer
from .serializers import saledetailSerializer
from .serializers import saledetailreportsmodelSerializer
from .serializers import stockmovementSerializer
from .serializers import stockmovementreportsmodelSerializer
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
import django_filters.rest_framework
from rest_framework import generics
import datetime
from cassandra.query import SimpleStatement
from cassandra.query import tuple_factory
from datetime import datetime
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
from django.http import HttpResponse
from itertools import groupby
from operator import itemgetter
import decimal
import operator
import datetime

# Create your views here.
# datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

@api_view(['GET', 'POST'])
def Sale(request):
    if request.method == 'POST':
        sales = sale.objects.limit(25000)
        city = request.data["city"]
        customercode = request.data["customercode"]
        salesmanname = request.data["salesmanname"]
        payplantype = request.data["payplantype"]
        projectcode = request.data["projectcode"]
        payplancode = request.data["payplancode"]
        maxdate = datetime.datetime.strptime(request.data["maxdate"], "%Y-%m-%dT%H:%M:%S")
        mindate = datetime.datetime.strptime(request.data["mindate"], "%Y-%m-%dT%H:%M:%S")
        maxgrosstotal = request.data["maxgrosstotal"]
        mingrosstotal = request.data["mingrosstotal"]
        maxnettotal = request.data["maxnettotal"]
        minnettotal = request.data["minnettotal"]


        sales = sales.filter(sale.date_ <= maxdate)
        sales = sales.filter(sale.date_ >= mindate)
        sales = sales.filter(sale.grosstotal <= maxgrosstotal)
        sales = sales.filter(sale.grosstotal >= mingrosstotal)
        sales = sales.filter(sale.nettotal <= maxnettotal)
        sales = sales.filter(sale.nettotal >= minnettotal)



        nullablevalues = { 'salesmanname' : salesmanname, 'city': city,
                        'customercode':customercode, 
                        'payplantype' : payplantype, 
                        'projectcode': projectcode, 
                        'payplancode': payplancode,
                        }
        arguments = {}
        for k, v in nullablevalues.items():
            if v:
                arguments[k] = v

        sales = sales.filter(**arguments)
        serializer = saleSerializer(sales, many=True)
        return Response(serializer.data)





@api_view(['GET', 'POST'])
def SaleDetail(request):
    if request.method == 'POST':
        saledetails = saledetail.objects.all()
        maxvatmatrah = request.data["maxvatmatrah"]
        minvatmatrah = request.data["minvatmatrah"]
        maxamount = request.data["maxamount"]
        minamount = request.data["minamount"]
        maxdate = datetime.datetime.strptime(request.data["maxdate"], "%Y-%m-%dT%H:%M:%S")
        mindate = datetime.datetime.strptime(request.data["mindate"], "%Y-%m-%dT%H:%M:%S")
        maxnotshippedamount = request.data["maxnotshippedamount"]
        minnotshippedamount = request.data["minnotshippedamount"]
        productcode = request.data["productcode"]
        productname = request.data["productname"]
        brandname = request.data["brandname"]
        typename = request.data["typename"]  
        productgender = request.data["productgender"]
        productmaterial = request.data["productmaterial"]
        productstyle = request.data["productstyle"]
        producttype = request.data["producttype"]
        productionstatus = request.data["productionstatus"]
        model = request.data["model"]
        sizecode = request.data["sizecode"]
        colourcode = request.data["colourcode"]
        clientcode = request.data["clientcode"]
        specode = request.data["specode"]
        city = request.data["city"]



        saledetails = saledetails.filter(saledetail.totalamount <= maxnotshippedamount)
        saledetails = saledetails.filter(saledetail.totalamount >= minnotshippedamount)
        saledetails = saledetails.filter(saledetail.date_ <= maxdate)
        saledetails = saledetails.filter(saledetail.date_ >= mindate)
        saledetails = saledetails.filter(saledetail.vatmatrah <= maxvatmatrah)
        saledetails = saledetails.filter(saledetail.vatmatrah >= minvatmatrah)
        saledetails = saledetails.filter(saledetail.amount <= maxamount)
        saledetails = saledetails.filter(saledetail.amount >= minamount)

        nullablevalues = { 'productcode' : productcode, 
                        'productname' : productname,
                        'brandname' : brandname, 
                        'typename' : typename,
                        'productgender' : productgender, 
                        'productmaterial' : productmaterial,
                        'productstyle': productstyle, 
                        'producttype' : producttype, 
                        'productionstatus': productionstatus, 
                        'model' : model, 
                        'sizecode' : sizecode, 
                        'clientcode':clientcode, 
                        'colourcode' : colourcode, 
                        'specode':specode, 
                        'city' : city }

        arguments = {}
        for k, v in nullablevalues.items():
            if v:
                arguments[k] = v

        saledetails = saledetails.filter(**arguments)
        serializer = saledetailSerializer(saledetails, many=True)
        return Response(serializer.data)



@api_view(['GET', 'POST'])
def StockMovement(request):
    if request.method == 'POST':
        stockmovements = stockmovement.objects.limit(25000)
        productcode = request.data["productcode"]
        productname = request.data["productname"]
        brandname = request.data["brandname"]
        typename = request.data["typename"]
        showasnew = request.data["showasnew"]
        productgender = request.data["productgender"]
        productmaterial = request.data["productmaterial"]
        productstyle = request.data["productstyle"]
        producttype = request.data["producttype"]
        productionstatus = request.data["productionstatus"]
        model = request.data["model"]
        colourcode = request.data["colourcode"]
        sizecode = request.data["sizecode"]
        ivenno = request.data["invenno"]
        maxdate = datetime.datetime.strptime(request.data["maxdate"], "%Y-%m-%dT%H:%M:%S")
        mindate = datetime.datetime.strptime(request.data["mindate"], "%Y-%m-%dT%H:%M:%S")
        maxreserved = request.data["maxreserved"]
        minreserved = request.data["minreserved"]
        maxactporder = request.data["maxactporder"]
        minactporder = request.data["minactporder"]
        maxonhand = request.data["maxonhand"]
        minonhand = request.data["minonhand"]
        stockmovements = stockmovements.filter(stockmovement.reserved <= maxreserved)
        stockmovements = stockmovements.filter(stockmovement.reserved >= minreserved)
        stockmovements = stockmovements.filter(stockmovement.date <= maxdate)
        stockmovements = stockmovements.filter(stockmovement.date >= mindate)
        stockmovements = stockmovements.filter(stockmovement.actporder <= maxactporder)
        stockmovements = stockmovements.filter(stockmovement.actporder >= minactporder)
        stockmovements = stockmovements.filter(stockmovement.onhand <= maxonhand)
        stockmovements = stockmovements.filter(stockmovement.onhand >= minonhand)


        nullablevalues = { 'productcode' : productcode,
                        'productname' : productname,
                        'brandname' : brandname,
                        'typename' : typename,
                        'productgender' : productgender,
                        'productmaterial' : productmaterial,
                        'productstyle': productstyle,
                        'producttype' : producttype,
                        'productionstatus': productionstatus,
                        'model' : model,
                        'sizecode' : sizecode,
                        'colourcode' : colourcode,
                        'showasnew' : showasnew,
                        'invenno' : ivenno }


        arguments = {}
        for k, v in nullablevalues.items():
            if v:
                arguments[k] = v

        stockmovements = stockmovements.filter(**arguments)
        serializer = stockmovementSerializer(stockmovements, many=True)
        return Response (serializer.data)


@api_view(['GET', 'POST'])
def saledetailreports(request):
    if request.method == 'POST':
        saledetails = saledetail.objects.limit(25000)
        maxdate = datetime.datetime.strptime(request.data["maxdate"], "%Y-%m-%dT%H:%M:%S")
        mindate = datetime.datetime.strptime(request.data["mindate"], "%Y-%m-%dT%H:%M:%S")
        maxvatmatrah = request.data["maxvatmatrah"]
        minvatmatrah = request.data["minvatmatrah"]
        maxamount = request.data["maxamount"]
        minamount = request.data["minamount"]        
        productcode = request.data["productcode"]
        productname = request.data["productname"]
        brandname = request.data["brandname"]
        typename = request.data["typename"]  
        productgender = request.data["productgender"]
        productmaterial = request.data["productmaterial"]
        productstyle = request.data["productstyle"]
        producttype = request.data["producttype"]
        productionstatus = request.data["productionstatus"]
        model = request.data["model"]
        sizecode = request.data["sizecode"]
        colourcode = request.data["colourcode"]
        clientcode = request.data["clientcode"]
        specode = request.data["specode"]
        city = request.data["city"]
        definition_ = request.data["definition_"]



        saledetails = saledetails.filter(saledetail.date_ <= maxdate)
        saledetails = saledetails.filter(saledetail.date_ >= mindate)
        saledetails = saledetails.filter(saledetail.vatmatrah <= maxvatmatrah)
        saledetails = saledetails.filter(saledetail.vatmatrah >= minvatmatrah)
        saledetails = saledetails.filter(saledetail.amount <= maxamount)
        saledetails = saledetails.filter(saledetail.amount >= minamount)

        nullablevalues = { 'productcode' : productcode, 
                        'productname' : productname,
                        'brandname' : brandname, 
                        'typename' : typename,
                        'productgender' : productgender, 
                        'productmaterial' : productmaterial,
                        'productstyle': productstyle, 
                        'producttype' : producttype, 
                        'productionstatus': productionstatus, 
                        'model' : model, 
                        'sizecode' : sizecode, 
                        'clientcode':clientcode, 
                        'colourcode' : colourcode, 
                        'specode':specode, 
                        'city' : city,
                        'definition_' : definition_}
        arguments = {}
        for k, v in nullablevalues.items():
            if v:
                arguments[k] = v

    saledetails = saledetails.filter(**arguments)
    serializer = saledetailSerializer(saledetails, many=True)
    asd = saledetailreportsmodel(serializer.data)
    serializer2 = saledetailreportsmodelSerializer(asd)
    return Response(serializer2.data)



@api_view(['GET', 'POST'])
def salereports(request):
    if request.method == 'POST':
    
        sales = sale.objects.limit(25000)
       
        maxgrosstotal = request.data["maxgrosstotal"]
        mingrosstotal = request.data["mingrosstotal"]
        maxnettotal = request.data["maxnettotal"]
        minnettotal = request.data["minnettotal"]
        maxdate = datetime.datetime.strptime(request.data["maxdate"], "%Y-%m-%dT%H:%M:%S")
        mindate = datetime.datetime.strptime(request.data["mindate"], "%Y-%m-%dT%H:%M:%S")
        customercode = request.data["customercode"]
        city = request.data["city"]
        salesmanname = request.data["salesmanname"]
        payplantype = request.data["payplantype"]  
        projectcode = request.data["projectcode"]
        payplancode = request.data["payplancode"]
        definition_ = request.data['clientname']
        specode = request.data['specode']
        

        sales = sales.filter(sale.date_ <= maxdate)
        sales = sales.filter(sale.date_ >= mindate)
        sales = sales.filter(sale.grosstotal <= maxgrosstotal)
        sales = sales.filter(sale.grosstotal >= mingrosstotal)
        sales = sales.filter(sale.nettotal <= maxnettotal)
        sales = sales.filter(sale.nettotal >= minnettotal)

        nullablevalues = { 'code' : customercode , 'city': city, 
                        'salesmanname' : salesmanname, 
                        'payplantype' : payplantype, 
                        'projectcode': projectcode, 
                        'payplancode': payplancode, 
                        'definition_': definition_,
                        'specode': specode
                        }
        arguments = {}
        for k, v in nullablevalues.items():
            if v:
                arguments[k] = v


        sales = sales.filter(**arguments)
        serializer = saleSerializer(sales, many=True)
        asd = salereportsmodel(serializer.data)
        serializer2 = salereportsmodelSerializer(asd)
        return Response(serializer2.data)






@api_view(['GET', 'POST'])
def stockmovementreports(request):
    if request.method == 'POST':
        stockmovements = stockmovement.objects.limit(20000)
        productcode = request.data["productcode"]
        productname = request.data["productname"]
        brandname = request.data["brandname"]
        typename = request.data["typename"]
        showasnew = request.data["showasnew"]
        productgender = request.data["productgender"]
        productmaterial = request.data["productmaterial"]
        productstyle = request.data["productstyle"]
        producttype = request.data["producttype"]
        productionstatus = request.data["productionstatus"]
        model = request.data["model"]
        colourcode = request.data["colourcode"]
        sizecode = request.data["sizecode"]
        ivenno = request.data["invenno"]
        maxdate = datetime.datetime.strptime(request.data["maxdate"], "%Y-%m-%dT%H:%M:%S")
        mindate = datetime.datetime.strptime(request.data["mindate"], "%Y-%m-%dT%H:%M:%S")
        maxreserved = request.data["maxreserved"]
        minreserved = request.data["minreserved"]
        maxactporder = request.data["maxactporder"]
        minactporder = request.data["minactporder"]
        maxonhand = request.data["maxonhand"]
        minonhand = request.data["minonhand"]
        stockmovements = stockmovements.filter(stockmovement.reserved <= maxreserved)
        stockmovements = stockmovements.filter(stockmovement.reserved >= minreserved)
        stockmovements = stockmovements.filter(stockmovement.date <= maxdate)
        stockmovements = stockmovements.filter(stockmovement.date >= mindate)
        stockmovements = stockmovements.filter(stockmovement.actporder <= maxactporder)
        stockmovements = stockmovements.filter(stockmovement.actporder >= minactporder)
        stockmovements = stockmovements.filter(stockmovement.onhand <= maxonhand)
        stockmovements = stockmovements.filter(stockmovement.onhand >= minonhand)

        nullablevalues = { 'productcode' : productcode,
                        'productname' : productname,
                        'brandname' : brandname,
                        'typename' : typename,
                        'productgender' : productgender,
                        'productmaterial' : productmaterial,
                        'productstyle': productstyle,
                        'producttype' : producttype,
                        'productionstatus': productionstatus,
                        'model' : model,
                        'sizecode' : sizecode,
                        'colourcode' : colourcode,
                        'showasnew' : showasnew,
                        'ivenno' : ivenno }


        arguments = {}
        for k, v in nullablevalues.items():
            if v:
                arguments[k] = v

        stockmovements = stockmovements.filter(**arguments)
        serializer = stockmovementSerializer(stockmovements, many=True)
        asd = stockmovementreportsmodel(serializer.data)
        serializer2 = stockmovementreportsmodelSerializer(asd)
        
        return Response(serializer2.data)








      

     
