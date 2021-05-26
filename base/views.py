from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout

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