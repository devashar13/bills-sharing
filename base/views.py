from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import Vendor, ExpenseID, Bill, BillImage
from decimal import Decimal
from django.http import JsonResponse
import json

def loginView(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email,password)
        user = authenticate(request,email = email,password = password)
        if user is not None:
            login(request,user)
            return render(request,'base/login.html',{"data":"hello"})
        else:
            print('nope')
    else:
        return render(request,'base/login.html',{})

def getVendors(request):
    vendors = Vendor.objects.all()
    return render(request, 'base/vendorsList.html', {'vendors': vendors})

def addVendor(request):
    if request.method=="POST":
        data=request.POST
        vname=data.get("vname")
        vemail = data.get("vmail")
        v = Vendor(name=vname,email=vemail)
        v.save()
    
    return render(request,'base/vendorsList.html')

def vendorDetails(request,vendorid):
    vendor = Vendor.objects.get(pk=vendorid)
    expenseIds = vendor.expense_ids.all()
    allExpenseIds = ExpenseID.objects.all()
    return render(request,'base/vendorDetails.html',{'vendor':vendor,'expenseIds':expenseIds,'allExpenseIds':allExpenseIds})

def getExpenseIdsForVendor(request):
    if request.method=='POST':
        data = request.POST
        vname = data.get("vendor")
        v = Vendor.objects.get(name=vname)
        eids = v.expense_ids.all()
        data = {}
        for e in eids:
            data[e.epattern] = e.eid
        return JsonResponse(data)

def createExpenseID(request):
    if request.method == "POST":
        data = request.POST
        eid = data.get("eid")
        epattern = data.get("epattern")
        expense = ExpenseID(
            eid=eid,
            epattern=epattern
        )
        expense.save()
        return render(request,'base/ExpenseIdAdded.html')
    return render(request,'base/createExpenseId.html')
    
def addExpenseID(request):
    if request.method=="POST":
        data=request.POST
        selectedeid=data.get("selectedeid")
        vendorid = data.get("vendorid")
        vendor = Vendor.objects.get(pk=vendorid)
        vendor.expense_ids.add(ExpenseID.objects.get(epattern=selectedeid))
    
    return render(request,'base/vendorDetails.html')


def addBill(request):
    vendors = Vendor.objects.all().values('name','expense_ids__eid')
    vendorNames = Vendor.objects.all().values('name').distinct()
    return render(request,'base/addbill.html',{'vendors':vendors,'vendorNames':vendorNames})

def addBillVendor(request,vendorid):
    vendor = Vendor.objects.get(pk=vendorid)
    vendors = Vendor.objects.all().values('name','expense_ids__eid')
    vendorNames = Vendor.objects.all().values('name').distinct()
    return render(request,'base/addbill.html',{'selectedvendor':vendor,'vendors':vendors,'vendorNames':vendorNames})


def saveBill(request):
    try:
        data = request.POST 
        vendors_name = data.get("vendors-name")
        print(vendors_name)
        vendor = Vendor.objects.filter(name = vendors_name).first()
        invoice_num = data.get("v-inv-no")
        invoice_date = data.get("v-inv-dt")
        expense_id = data.get("vendors-expense")
        exp_from_date = data.get("ex-from-date")
        exp_to_date = data.get("ex-to-date")
        quantity = data.get("qty")
        rate = Decimal(data.get("rate"))
        amount = Decimal(data.get("amount"))
        gst = Decimal(data.get("gst"))
        total_amount = Decimal(data.get("total"))
        due_payment = data.get("due")
        files = data.get("myFileInput")

        bill = Bill(
            vendor = vendor,
            invoice_num = invoice_num,
            invoice_date = invoice_date,
            expense_id = expense_id,
            exp_from_date = exp_from_date,
            exp_to_date = exp_to_date,
            quantity = quantity,
            rate = (rate),
            amount = (amount),
            gst = (gst),
            total_amount = (total_amount),
            due_payment = due_payment
        )
        bill.save()
        for f in request.FILES.getlist('myFileInput'):
            bi = BillImage(
                image = f,
                bill = bill
            )
            bi.save()
        return redirect("addBill")
        
    except Exception as e:
        print("HELLO")
        print(e)
        return redirect("addBill")

    
