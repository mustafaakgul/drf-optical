from cassandra.cqlengine import columns
from cassandra.cqlengine import columns as cassandra_columns
from django_cassandra_engine.models import DjangoCassandraModel
from django.db import models
from datetime import datetime
from decimal import *
from operator import itemgetter
import collections


class Sale(DjangoCassandraModel):
    read_repair_chance = 0.05
    date_ = columns.DateTime(primary_key=True)
    ficheno = columns.Text(primary_key=True)
    payplancode  = columns.Text(primary_key=True)
    salesmanname  = columns.Text(primary_key=True)
    payplantype  = columns.Text(primary_key=True)
    code  = columns.Text(required=False)
    city  = columns.Text(required=False)
    definition_  = columns.Text(required=False)
    genexp1 = columns.Text(required=False)
    genexp2  = columns.Text(required=False)
    genexp3  = columns.Text(required=False)
    genexp4  = columns.Text(required=False)
    grosstotal  = columns.Double()
    projectcode  = columns.Text(required=False)
    specode  = columns.Text(required=False)
    totaldiscounts  = columns.Double()
    totaldiscounted = columns.Double()
    totalvat  = columns.Double()
    reportnet = columns.Double()
    nettotal = columns.Double()

    class Meta:
        get_pk_field='date_'


class Saledetail(DjangoCassandraModel):
    read_repair_chance = 0.05 # optional - defaults to 0.1
    date_ = columns.DateTime(primary_key=True)
    logicalref = columns.Integer(primary_key=True)
    productcode  = columns.Text(primary_key=True)
    productname = columns.Text(required=False)
    brandname  = columns.Text(required=False)
    typename  = columns.Text(required=False)
    showasnew = columns.Integer()
    productgender  = columns.Text(required=False)
    productmaterial  = columns.Text(required=False)
    productstyle  = columns.Text(required=False)
    producttype  = columns.Text(required=False)
    productionstatus  = columns.Text(required=False)
    model  = columns.Text(required=False)
    colourcode  = columns.Text(required=False)
    sizecode  = columns.Text(required=False)
    clientcode  = columns.Text(required=False)
    definition_  = columns.Text(required=False)
    specode  = columns.Text(required=False)
    city  = columns.Text(required=False)
    amount = columns.Double()
    shippedamount  = columns.Double()
    price  = columns.Double()
    total  = columns.Double()
    distcost  = columns.Double()
    distdisc  = columns.Double()
    vat  = columns.Double()
    vatamnt  = columns.Double()
    vatmatrah  = columns.Double()
    prcurr = columns.SmallInt()
    prprice = columns.Double()
    totalamount = columns.Double()

    class Meta:
        get_pk_field='date_'


class Stockmovement(DjangoCassandraModel):
    read_repair_chance = 0.05 # optional - defaults to 0.1
    productcode  = columns.Text(primary_key=True)
    date = columns.DateTime(primary_key=True)
    reserved = columns.Double(primary_key=True)
    actporder =columns.Double(primary_key=True)
    onhand = columns.Double(primary_key=True)
    ivenno = columns.Integer(primary_key=True)
    brandname  = columns.Text(required=False)
    colourcode  = columns.Text(required=False)
    model  = columns.Text(required=False)
    productgender  = columns.Text(required=False)
    productionstatus  = columns.Text(required=False)
    productmaterial  = columns.Text(required=False)
    productname = columns.Text(required=False)
    productstyle  = columns.Text(required=False)
    producttype  = columns.Text(required=False)
    salamnt = columns.Double()
    salcash = columns.Double()
    salcurr = columns.Double()
    showasnew = columns.Integer()
    sizecode = columns.Text()
    typename = columns.Text()

    class Meta:
        get_pk_field='productcode'


class Saledetailreportsmodel(models.Model):

    def __init__(self, liste):
        self.vatmatrahbyproducts = {}
        self.vatmatrahbybrands = {}
        self.vatmatrahbytypes={}
        self.amountsbyproductcode = {}
        self.amountbycustomers = {}
        self.amountbybrandnames = {}
        self.amountbygenders = {}
        self.salesbycity = {}
        self.totalamountbycustomers = {}
        self.totalamountbycity ={}
        self.typeamountbybrandnames={}

        self.totalamountbycustomer(liste)
        self.typeamountbybrandname(liste)
        
        self.methods(liste,'productname', 'vatmatrah', self.vatmatrahbyproducts)
        self.methods(liste,'brandname', 'vatmatrah', self.vatmatrahbybrands)
        self.methods(liste,'typename', 'vatmatrah', self.vatmatrahbytypes)
        self.methods(liste,'productcode', 'amount', self.amountsbyproductcode)
        self.methods(liste,'definition_', 'amount', self.amountbycustomers)
        self.methods(liste,'brandname', 'amount', self.amountbybrandnames)
        self.methods(liste,'productgender', 'amount', self.amountbygenders)
        self.methods(liste,'city', 'total', self.salesbycity)
        self.methods(liste,'city', 'amount', self.totalamountbycity)

    def methods(self, liste,mainvalue,complementaryvalue,dictionary):
        for x in range(0, len(liste)):
            if liste[x][mainvalue] in dictionary:
                dictionary[liste[x][mainvalue]] = dictionary[liste[x][mainvalue]] + liste[x][complementaryvalue]
            else:
                dictionary[liste[x][mainvalue]] = liste[x][complementaryvalue]

    def typeamountbybrandname(self, liste):
        for x in range(0, len(liste)):
            if liste[x]['brandname'] in self.typeamountbybrandnames:
                if liste[x]['typename'] in self.typeamountbybrandnames[liste[x]['brandname']]:
                    self.typeamountbybrandnames[liste[x]['brandname']][liste[x]['typename']] = self.typeamountbybrandnames[liste[x]['brandname']][liste[x]['typename']] + liste[x]['amount']
                else:
                    self.typedictionary = {}
                    self.typeamountbybrandnames[liste[x]['brandname']][liste[x]['typename']] = liste[x]['amount']
            else:
                self.typedictionary = {}
                self.typeamountbybrandnames[liste[x]['brandname']] = self.typedictionary
                self.typeamountbybrandnames[liste[x]['brandname']][liste[x]['typename']] = liste[x]['amount']

    def totalamountbycustomer(self, liste):
        for x in range(0, len(liste)):
            if liste[x]['definition_'] in self.totalamountbycustomers:
                if liste[x]['productcode'] in self.totalamountbycustomers[liste[x]['definition_']]:
                    self.totalamountbycustomers[liste[x]['definition_']][liste[x]['productcode']] = self.totalamountbycustomers[liste[x]['definition_']][liste[x]['productcode']] + liste[x]['amount']
                else:
                    self.typedictionaries = {}
                    self.totalamountbycustomers[liste[x]['definition_']][liste[x]['productcode']] = liste[x]['amount']
            else:
                self.typedictionaries = {}
                self.totalamountbycustomers[liste[x]['definition_']] = self.typedictionaries
                self.totalamountbycustomers[liste[x]['definition_']][liste[x]['productcode']] = liste[x]['amount']


class Salereportsmodel(models.Model):

    def __init__(self, liste):
        self.customerpayplans = {}
        self.salesbyregions = {}
        self.salesmanbycities = {}
        self.salesmanbyregions = {}
        self.payplansummaries = {}
        self.citynettotalsummaries = {}
        self.regiontotalsummaries = {}
        self.salesmansummaries = {}
        
        self.customerpayplan(liste)
        self.salesmanbyregion(liste)
        self.salesbyregion(liste)
        self.salesmanbycity(liste)

        self.methods(liste,'payplantype', 'nettotal', self.payplansummaries)
        self.methods(liste,'city', 'nettotal', self.citynettotalsummaries)
        self.methods(liste,'specode', 'nettotal', self.regiontotalsummaries)
        self.methods(liste,'salesmanname', 'nettotal', self.salesmansummaries)

    def methods(self, liste,mainvalue,complementaryvalue,dictionary):
        for x in range(0, len(liste)):
            if liste[x][mainvalue] in dictionary:
                dictionary[liste[x][mainvalue]] = dictionary[liste[x][mainvalue]] + liste[x][complementaryvalue]
            else:
                dictionary[liste[x][mainvalue]] = liste[x][complementaryvalue]

    def customerpayplan(self,liste):
        for x in range(0, len(liste)):
            if liste[x]['definition_'] in self.customerpayplans:
                if liste[x]['payplantype'] in self.customerpayplans[liste[x]['definition_']]:
                    self.customerpayplans[liste[x]['definition_']][liste[x]['payplantype']] = self.customerpayplans[liste[x]['definition_']][liste[x]['payplantype']] + liste[x]['nettotal']
                else:
                    self.payplandict = {}
                    self.customerpayplans[liste[x]['definition_']][liste[x]['payplantype']] = liste[x]['nettotal']
            else:
                self.payplandict = {}
                self.customerpayplans[liste[x]['definition_']] = self.payplandict
                self.customerpayplans[liste[x]['definition_']][liste[x]['payplantype']] = liste[x]['nettotal']

    def salesbyregion(self,liste):
        for x in range(0, len(liste)):
            if liste[x]['specode'] in self.salesbyregions:
                if liste[x]['projectcode'] in self.salesbyregions[liste[x]['specode']]:
                    self.salesbyregions[liste[x]['specode']][liste[x]['projectcode']] = self.salesbyregions[liste[x]['specode']][liste[x]['projectcode']] + liste[x]['nettotal']
                else:
                    self.payplandict = {}
                    self.salesbyregions[liste[x]['specode']][liste[x]['projectcode']] = liste[x]['nettotal']
            else:
                self.payplandict = {}
                self.salesbyregions[liste[x]['specode']] = self.payplandict
                self.salesbyregions[liste[x]['specode']][liste[x]['projectcode']] = liste[x]['nettotal']

    def salesmanbyregion(self,liste):
        for x in range(0, len(liste)):
            if liste[x]['specode'] in self.salesmanbyregions:
                if liste[x]['salesmanname'] in self.salesmanbyregions[liste[x]['specode']]:
                    self.salesmanbyregions[liste[x]['specode']][liste[x]['salesmanname']] = self.salesmanbyregions[liste[x]['specode']][liste[x]['salesmanname']] + liste[x]['nettotal']
                else:
                    self.payplandict = {}
                    self.salesmanbyregions[liste[x]['specode']][liste[x]['salesmanname']] = liste[x]['nettotal']
            else:
                self.payplandict = {}
                self.salesmanbyregions[liste[x]['specode']] = self.payplandict
                self.salesmanbyregions[liste[x]['specode']][liste[x]['salesmanname']] = liste[x]['nettotal']

    def salesmanbycity(self,liste):
        for x in range(0, len(liste)):
            if liste[x]['city'] in self.salesmanbycities:
                if liste[x]['salesmanname'] in self.salesmanbycities[liste[x]['city']]:
                    self.salesmanbycities[liste[x]['city']][liste[x]['salesmanname']] = self.salesmanbycities[liste[x]['city']][liste[x]['salesmanname']] + liste[x]['nettotal']
                else:
                    self.payplandict = {}
                    self.salesmanbycities[liste[x]['city']][liste[x]['salesmanname']] = liste[x]['nettotal']
            else:
                self.payplandict = {}
                self.salesmanbycities[liste[x]['city']] = self.payplandict
                self.salesmanbycities[liste[x]['city']][liste[x]['salesmanname']] = liste[x]['nettotal']


class Stockmovementreportsmodel(models.Model):
    def __init__(self, liste):
        self.liste = liste
        self.productreserves = {}
        self.productonhands = {}
        self.productacporders = {}
        self.brandonhands = {}
        self.brandreserves = {}
        self.brandactporders = {}

        self.brandreserve(self.liste)
        self.brandonhand(self.liste)
        self.brandactporder(self.liste)
        self.methods(liste,'productname', 'reserved', self.productreserves)
        self.methods(liste,'productname', 'actporder', self.productacporders)
        self.methods(liste,'productname', 'onhand', self.productonhands)

    def methods(self, liste,mainvalue,complementaryvalue,dictionary):
        for x in range(0, len(liste)):
            if liste[x][mainvalue] in dictionary:
                dictionary[liste[x][mainvalue]] = dictionary[liste[x][mainvalue]] + liste[x][complementaryvalue]
            else:
                dictionary[liste[x][mainvalue]] = liste[x][complementaryvalue]
                
    def brandonhand(self,liste):
        for x in range(0, len(liste)):
            if liste[x]['brandname'] in self.brandonhands:
                if liste[x]['typename'] in self.brandonhands[liste[x]['brandname']]:
                    self.brandonhands[liste[x]['brandname']][liste[x]['typename']] = self.brandonhands[liste[x]['brandname']][liste[x]['typename']] + liste[x]['onhand']
                else:
                    self.brandonhands[liste[x]['brandname']][liste[x]['typename']] = liste[x]['onhand']
            else:
                self.typedictionary = {}
                self.brandonhands[liste[x]['brandname']] = self.typedictionary
                self.brandonhands[liste[x]['brandname']][liste[x]['typename']] = liste[x]['onhand']   

    def brandactporder(self,liste):
        for x in range(0, len(liste)):
            if liste[x]['brandname'] in self.brandactporders:
                if liste[x]['typename'] in self.brandactporders[liste[x]['brandname']]:
                    self.brandactporders[liste[x]['brandname']][liste[x]['typename']] = self.brandactporders[liste[x]['brandname']][liste[x]['typename']] + liste[x]['actporder']
                else:
                    self.brandactporders[liste[x]['brandname']][liste[x]['typename']] = liste[x]['actporder']
            else:
                self.acporder = {}
                self.brandactporders[liste[x]['brandname']] = self.acporder
                self.brandactporders[liste[x]['brandname']][liste[x]['typename']] = liste[x]['actporder']

    def brandreserve(self,liste):
        for x in range(0, len(liste)):
            if liste[x]['brandname'] in self.brandreserves:
                if liste[x]['typename'] in self.brandreserves[liste[x]['brandname']]:
                    self.brandreserves[liste[x]['brandname']][liste[x]['typename']] = self.brandreserves[liste[x]['brandname']][liste[x]['typename']] + liste[x]['reserved']
                else:
                    self.brandreserves[liste[x]['brandname']][liste[x]['typename']] = liste[x]['reserved']
            else:
                self.acporder = {}
                self.brandreserves[liste[x]['brandname']] = self.acporder
                self.brandreserves[liste[x]['brandname']][liste[x]['typename']] = liste[x]['reserved']


    # def productnametoclientcode(self,liste):
    #     for x in range(0, len(liste)):
    #         if liste[x]['productcode'] in self.brandbytype:
    #             if liste[x]['definition_'] in self.brandbytype[liste[x]['productcode']]:
    #                 self.brandbytype[liste[x]['productcode']][liste[x]['definition_']] = self.brandbytype[liste[x]['productcode']][liste[x]['definition_']] + liste[x]['amount']
    #             else:
    #                 self.typedict = {}
    #                 self.brandbytype[liste[x]['productcode']][liste[x]['definition_']] = liste[x]['amount']
    #         else:
    #             self.typedict = {}
    #             self.brandbytype[liste[x]['productcode']] = self.typedict




# class salereport (models.Model):

#         def brandnametotype(self,liste):
#         for x in range(0, len(liste)):
#             if liste[x]['brandname'] in self.productbycode:
#                 # return self.brandbytype[liste[x]['brandname']][liste[x]['typename']]
#                 # self.brandbytype[liste[x]['brandname']] = [[liste[x]['typename']]+[liste[x]['amount']]]
#                 if liste[x]['typename'] in self.productbycode[liste[x]['brandname']]:
#                     self.productbycode[liste[x]['brandname']][liste[x]['typename']] = self.productbycode[liste[x]['brandname']][liste[x]['typename']] + liste[x]['amount']
#                 else:
#                     self.typedictionary = {}
#                     self.productbycode[liste[x]['brandname']][liste[x]['typename']] = liste[x]['amount']
#                     # self.brandbytype[liste[x]['brandname']][liste[x]['typename']] = self.typedict
#             else:
#                 # self.brandbytype[liste[x]['brandname']] = liste[x]['typename']
#                 self.typedictionary = {}
#                 # self.typedict[liste[x]['typename']] = liste[x]['amount']
#                 self.productbycode[liste[x]['brandname']] = self.typedictionary