from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect, get_object_or_404

from .models import Vendor, ExpenseID

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

def getVendors(request):
    vendors = Vendor.objects.all()
    return render(request, 'base/vendorsList.html', {'vendors': vendors})

def addVendor(request):
    return render(request,'base/addVendor.html')

def vendorDetails(request,vendorid):
    vendor = Vendor.objects.get(pk=vendorid)
    expenseIds = vendor.expense_ids.all()
    allExpenseIds = ExpenseID.objects.all()
    return render(request,'base/vendorDetails.html',{'vendor':vendor,'expenseIds':expenseIds})

def createExpenseID(request):
    if request.method == "POST":
        print("DO SMTHNG")
    return render(request,'base/createExpenseId.html')