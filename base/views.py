from django.db.models.expressions import F
from django.shortcuts import redirect, render
from django.http import HttpResponse, request
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, EmployeeAdditional, Supervisor, Vendor, ExpenseID, Bill, BillImage
from decimal import Decimal
from django.http import JsonResponse
import datetime
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json



def loginView(request):
    if request.method == "POST":
        try:
            email = request.POST.get("email")
            password = request.POST.get("password")
            print(email,password)
            user = authenticate(request,email = email,password = password)
            print(user)
            if user is not None:
                login(request,user)
                userTypeList = list(user.type)
                # if "supervisor" in userTypeList:
                #     return redirect('home')
                # else:
                #     return redirect('addBill')
                return redirect('home')
                
            else:
                return render(request,'base/login.html',{"data":"wrong"})
        except Exception as e:
            print(e)
    else:
        return render(request,'base/login.html',{})

@login_required(login_url='/login/')
def homeView(request):
    userTypeList = list(request.user.type)
    # if 'supervisor' in userTypeList:
    #     return render(request,"base/home.html",{'userType':userTypeList})
    # else:
    #     return redirect("addBill")
    return render(request,"base/home.html",{'userType':userTypeList})

    
@login_required(login_url='/login/')
def getVendors(request):
    userTypeList = list(request.user.type)
    print(userTypeList)
    if "supervisor" in userTypeList:
        vendors = Vendor.objects.all().order_by("name")
        print(vendors)
        return render(request, 'base/vendorsList.html', {'vendors': vendors,'userType':userTypeList})
    else:
        return redirect('addBill')   

@login_required(login_url='/login/')
def addVendor(request):
    
    if request.method=="POST":
        userTypeList = list(request.user.type)
        print(userTypeList)
        if "supervisor" in userTypeList:
            data=request.POST
            vname=data.get("vname")
            vemail = data.get("vmail")
            gstin = data.get("gstin")
            v = Vendor(name=vname,email=vemail,GSTIN = gstin)
            v.save()
        
            return render(request,'base/vendorsList.html')
        else:
            return redirect('addBill')  
        
@login_required(login_url='/login/')
def removeVendor(request):
    
    if request.method=="POST":
        userTypeList = list(request.user.type)
        print(userTypeList)
        if "supervisor" in userTypeList:
            data=request.POST
            vid=data.get("vid")
            print(vid)
            v = Vendor.objects.filter(id=vid)
            v.delete()
            return JsonResponse({"ok":"ok"})
        else:
            return redirect('addBill') 
     

@login_required(login_url='/login/')
def vendorDetails(request,vendorid):
    userTypeList = list(request.user.type)
    print(userTypeList)
    if "supervisor" in userTypeList:
        vendor = Vendor.objects.get(pk=vendorid)
        expenseIds = vendor.expense_ids.all()
        allExpenseIds = ExpenseID.objects.all()
        print(allExpenseIds)
        return render(request,'base/vendorDetails.html',{'vendor':vendor,'expenseIds':expenseIds,'allExpenseIds':allExpenseIds,'userType':userTypeList})


@login_required(login_url='/login/')
def getExpenseIdsForVendor(request):
    if request.method=='POST':
        userTypeList = list(request.user.type)
        print(userTypeList)
        if "supervisor" in userTypeList:
            data = request.POST
            vname = data.get("vendor")
            v = Vendor.objects.get(name=vname)
            eids = v.expense_ids.all()
            data = {}
            for e in eids:
                data[e.epattern] = e.eid
            return JsonResponse(data)
    
@login_required(login_url='/login/')

def createExpenseID(request):
    userTypeList = list(request.user.type)
    print(userTypeList)
    if "supervisor" in userTypeList:
        if request.method == "POST":
            data = request.POST
            eid = data.get("eid")
            epattern = data.get("epattern")
            if ExpenseID.objects.filter(epattern = epattern).exists():
                return render(request,'base/createExpenseId.html',{'userType':userTypeList,'warn':'Expense Id Exists'})
            else:
                expense = ExpenseID(
                    eid=eid,
                    epattern=epattern
                )
                expense.save()
                return redirect('manageExpenseId')
        return render(request,'base/createExpenseId.html',{'userType':userTypeList})
    else:
        return redirect("addBill")

def manageExpenseId(request):
    userTypeList = list(request.user.type)
    print(userTypeList)
    if "supervisor" in userTypeList:
        allExpenseIds = ExpenseID.objects.all()
        print('hi',allExpenseIds)
        return render(request,'base/manageexpense.html',{'userType':userTypeList,'allExpenseIds':allExpenseIds})
    else:
        return redirect("addBill")
    

def removeExpId(request):
    if request.method=="POST":
        userTypeList = list(request.user.type)
        print(userTypeList)
        if "supervisor" in userTypeList:
            data=request.POST
            eid=data.get("eid")
            expense = ExpenseID.objects.filter(eid = eid)
            expense.delete()
            return JsonResponse({"ok":"ok"})
        else:
            return redirect('addBill') 
    

@login_required(login_url='/login/')    
def addExpenseID(request):
    userTypeList = list(request.user.type)
    print(userTypeList)
    if "supervisor" in userTypeList:
        if request.method=="POST":
            data=request.POST
            selectedeid=data.get("selectedeid")
            vendorid = data.get("vendorid")
            print(vendorid,selectedeid)
            vendor = Vendor.objects.get(pk=vendorid)
            print(vendor)
            vendor.expense_ids.add(ExpenseID.objects.get(epattern=selectedeid))
            
        return render(request,'base/vendorDetails.html')
    else:
        return redirect("addBill")


@login_required(login_url='/login/')
def addBill(request):
    userTypeList = list(request.user.type)
    
    if request.method == "POST":
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
        sgst = Decimal(data.get("sgst"))
        cgst = Decimal(data.get("cgst"))
        igst = Decimal(data.get("igst"))
        total_amount = Decimal(data.get("total"))
        narration = (data.get("narration"))
        due_payment = data.get("due")
        files = data.get("myFileInput")
        inv_date = datetime.datetime.strptime(invoice_date, "%d-%m-%Y").strftime("%Y-%m-%d")
        exp_from = datetime.datetime.strptime(exp_from_date, "%d-%m-%Y").strftime("%Y-%m-%d")
        exp_to = datetime.datetime.strptime(exp_to_date, "%d-%m-%Y").strftime("%Y-%m-%d")
        due = datetime.datetime.strptime(due_payment, "%d-%m-%Y").strftime("%Y-%m-%d")
        if Bill.objects.filter(invoice_num =invoice_num ).exists():
            vendors = Vendor.objects.all().values('name','expense_ids__eid')
            vendorNames = Vendor.objects.all().values('name').distinct()
            return render(request,'base/addbill.html',{'vendors':vendors,'vendorNames':vendorNames,"userType":userTypeList,"msg":"Invoice Number Already Exists"})
        else:
            bill = Bill(
                vendor = vendor,
                invoice_num = invoice_num,
                invoice_date = inv_date,
                expense_id = expense_id,
                exp_from_date = exp_from,
                exp_to_date = exp_to,
                narration = narration,
                quantity = quantity,
                rate = (rate),
                amount = (amount),
                sgst = (sgst),
                cgst = (cgst),
                igst = (igst),
                total_amount = (total_amount),
                due_payment = due
            )
            
            bill.save()
            for f in request.FILES.getlist('myFileInput'):
                bi = BillImage(
                    image = f,
                    bill = bill
                )
                bi.save()
            return redirect("addBill")
    else:
        if "supervisor" in userTypeList:
            userTypeList = list(request.user.type)
            vendors = Vendor.objects.all().values('name','expense_ids__eid')
            vendorNames = Vendor.objects.all().values('name').distinct()
            return render(request,'base/addbill.html',{'vendors':vendors,'vendorNames':vendorNames,"userType":userTypeList})
        else:
            vendorNames = EmployeeAdditional.objects.filter(user = request.user).values('vendor__name').distinct()
            vendors = EmployeeAdditional.objects.filter(user = request.user).values('vendor__name','vendor__expense_ids__eid')
            print(vendors)
            return render(request,'base/addbill.html',{'vendors':vendors,'vendorNames':vendorNames,"userType":userTypeList})

        
    

@login_required(login_url='/login/')
def addBillVendor(request,vendorid):
    userTypeList = list(request.user.type)
    if request.method == "POST":
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
        sgst = Decimal(data.get("sgst"))
        cgst = Decimal(data.get("cgst"))
        igst = Decimal(data.get("igst"))
        total_amount = Decimal(data.get("total"))
        narration = (data.get("narration"))
        due_payment = data.get("due")
        files = data.get("myFileInput")
        inv_date = datetime.datetime.strptime(invoice_date, "%d-%m-%Y").strftime("%Y-%m-%d")
        exp_from = datetime.datetime.strptime(exp_from_date, "%d-%m-%Y").strftime("%Y-%m-%d")
        exp_to = datetime.datetime.strptime(exp_to_date, "%d-%m-%Y").strftime("%Y-%m-%d")
        due = datetime.datetime.strptime(due_payment, "%d-%m-%Y").strftime("%Y-%m-%d")
        if Bill.objects.filter(invoice_num =invoice_num ).exists():
            vendor = Vendor.objects.get(pk=vendorid)
            vendors = Vendor.objects.all().values('name','expense_ids__eid')
            vendorNames = Vendor.objects.all().values('name').distinct()
            return render(request,'base/addbill.html',{'selectedvendor':vendor,'vendors':vendors,'vendorNames':vendorNames,"userType":userTypeList,"msg":"Invoice Number Already Exists"})
        else:
            bill = Bill(
                vendor = vendor,
                invoice_num = invoice_num,
                invoice_date = inv_date,
                expense_id = expense_id,
                exp_from_date = exp_from,
                exp_to_date = exp_to,
                narration = narration,
                quantity = quantity,
                rate = (rate),
                amount = (amount),
                sgst = (sgst),
                cgst = (cgst),
                igst = (igst),
                total_amount = (total_amount),
                due_payment = due
            )
            
            bill.save()
            for f in request.FILES.getlist('myFileInput'):
                bi = BillImage(
                    image = f,
                    bill = bill
                )
                bi.save()
            return redirect("addBill")
    else:
        if 'supervisor' in userTypeList:
            vendor = Vendor.objects.get(pk=vendorid)
            vendors = Vendor.objects.all().values('name','expense_ids__eid')
            vendorNames = Vendor.objects.all().values('name').distinct()
            return render(request,'base/addbill.html',{'selectedvendor':vendor,'vendors':vendors,'vendorNames':vendorNames,"userType":userTypeList})
        else:
            return redirect("addBill")

@login_required(login_url='/login/')
def selectEmployee(request):
    userTypeList = list(request.user.type)
    print(userTypeList)
    if "supervisor" in userTypeList:
        supervisor = request.user
        emps = EmployeeAdditional.objects.filter(supervisor__email = supervisor)
        userTypeList = list(request.user.type)
        return render(request,'base/selectemps.html',{'emps':emps,"userType":userTypeList})
    else:
        return redirect('addBill')
    
@login_required(login_url='/login/')
def employeeVendor(request,empid):
    userTypeList = list(request.user.type)
    if "supervisor" in userTypeList:
        x = []
        y = []
        allocated = EmployeeAdditional.objects.filter(id = empid).values('vendor__name','vendor__id').distinct()
        vendorNames = Vendor.objects.all().values('name').distinct()
        for i in range(len(allocated)):
            x.append(allocated[i]['vendor__name'])
        for m in range(len(vendorNames)):
            y.append(vendorNames[m]['name'])
        not_allocated = list(set(x).symmetric_difference(set(y)))
        vendorName = Vendor.objects.filter(name__in = not_allocated).values('id','name')
        return render(request,'base/employeevendor.html',{'allocated':allocated,'vendornames':vendorName,"empid":empid,"userType":userTypeList})
    else:
        return redirect("addBill")

def saveEmployeeVendors(request):
    data=request.POST
    new_vendids = data.getlist("vends[]")
    empid = data.get("empid")
    print(new_vendids)
    # allocated = list(allocated)
    more = Vendor.objects.filter(id__in = new_vendids)
    addnew = EmployeeAdditional.objects.get(id = empid)
    print(addnew)
    addnew.vendor.add(*more)
        # for i in range(len(allocated)):
    #     new_vendids.append(allocated[i]['vendor__id'])
    # print(new_vendids)
    # new_vendors = data.get("vends")
    # emp = data.get('empid')
    # print(new_vendors,emp)
    return JsonResponse({"hi":"OK"})

def deleteEmployeeVendors(request):
    data=request.POST
    vendor = data.get("vendor")
    print(vendor)
    empid = data.get("empid")
    more = Vendor.objects.filter(id = vendor)
    addnew = EmployeeAdditional.objects.get(id = empid)
    addnew.vendor.remove(vendor)
    return JsonResponse({"hi":"OK"})
    
    
    

@login_required(login_url='/login/')
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
        sgst = Decimal(data.get("sgst"))
        cgst = Decimal(data.get("cgst"))
        igst = Decimal(data.get("igst"))
        total_amount = Decimal(data.get("total"))
        narration = (data.get("narration"))
        due_payment = data.get("due")
        files = data.get("myFileInput")
        inv_date = datetime.datetime.strptime(invoice_date, "%d-%m-%Y").strftime("%Y-%m-%d")
        exp_from = datetime.datetime.strptime(exp_from_date, "%d-%m-%Y").strftime("%Y-%m-%d")
        exp_to = datetime.datetime.strptime(exp_to_date, "%d-%m-%Y").strftime("%Y-%m-%d")
        due = datetime.datetime.strptime(due_payment, "%d-%m-%Y").strftime("%Y-%m-%d")
        print
        
      
        bill = Bill(
            vendor = vendor,
            invoice_num = invoice_num,
            invoice_date = inv_date,
            expense_id = expense_id,
            exp_from_date = exp_from,
            exp_to_date = exp_to,
            narration = narration,
            quantity = quantity,
            rate = (rate),
            amount = (amount),
            sgst = (sgst),
            cgst = (cgst),
            igst = (igst),
            total_amount = (total_amount),
            due_payment = due
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

@login_required(login_url='/login/')
def viewBills(request):
    userTypeList = list(request.user.type)
    bills = Bill.objects.values(
        "vendor__name",'invoice_num','invoice_date',
        'expense_id','exp_from_date','exp_to_date',
        'quantity','rate','amount','sgst','cgst','igst','other',
        'total_amount','due_payment','paid'
        )
    print(bills)
    return render(request,'base/viewbills.html',{"bills":bills,"userType":userTypeList})

@login_required(login_url='/login/')
def vendorBills(request,vendorid):
    userTypeList = list(request.user.type)
    print(userTypeList)
    if "supervisor" in userTypeList:
        vendor = Vendor.objects.get(pk=vendorid)
        print(vendor)
        bills  = Bill.objects.filter(vendor__id = vendorid)
        print(bills)
        return render(request,'base/viewbills.html',{'selectedvendor':vendor,'selectbills':bills,"userType":userTypeList})
    else: 
        return redirect("addBill")

@login_required(login_url='/login/')    
def sendImages(request):
    data = request.POST
    x = {}
    bill = request.POST.get('bill')
    print(bill)
    images = BillImage.objects.filter(bill__invoice_num = bill)
    print(images)
    for e in images:
        print(e.image.url)
        x[bill] = str(e.image.url)

    return JsonResponse(x)

@login_required(login_url='/login/')
def logoutView(request):
    logout(request)
    return redirect('login')