from base.models import Bill, Vendor
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from decimal import Decimal
# Create your views here.
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
def addBill(request):
    vendors = Vendor.objects.all().values('name','expense_ids__eid')
    ctx = {
        'vendors':vendors
    }
    return render(request,'base/addbill.html',ctx)
def saveBill(request):
    try:
        data = request.POST 
        vendors = data.get("vendors")
        vendor = Vendor.objects.filter(name = vendors).first()
        invoice_num = data.get("v-inv-no")
        invoice_date = data.get("v-inv-dt")
        expense_id = data.get("expid")
        print(expense_id)
        exp_from_date = data.get("v-ex-from-date")
        exp_to_date = data.get("ex-to-date")
        quantity = data.get("qty")
        rate = Decimal(data.get("rate"))
        amount = Decimal(data.get("amount"))
        gst = Decimal(data.get("gst"))
        total_amount = Decimal(data.get("total"))
        due_payment = data.get("due")
        print(amount,type(amount))
        print(gst,type(gst))
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
        return redirect("addBill")
        
    except Exception as e:
        print(e)
    
    
    
    
    
  