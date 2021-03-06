"""bills URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from base.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("",homeView,name="home"),

    path('admin/', admin.site.urls),
    path("login/",loginView,name = "login"),
    path("logout/",logoutView,name = "logout"),
    path("vendors/",getVendors,name = "getVendors"),
    path("addvendor/",addVendor,name = "addVendor"),
    path("removevendor/",removeVendor,name = "removeVendor"),
    path("manageexp/",manageExpenseId,name = "manageExpenseId"),
    path("removeexpid/",removeExpId,name = "removeExpId"),
    
    
    path("vendordetail/<int:vendorid>/",vendorDetails,name="vendorDetails"),
    path("getexpenseidsforvendor/",getExpenseIdsForVendor,name="getExpenseIdsForVendor"),
    path("addexpenseidtovendor/",addExpenseID,name="addExpenseID"),
    path("createexpenseid/",createExpenseID,name="createExpenseID"),
    path("addBill/",addBill,name = "addBill"),
    path("addBill/<int:vendorid>",addBillVendor,name = "addBillVendor"),
    path("savebill/",saveBill,name = "saveBill"),
    path("viewBills/",viewBills,name = "viewBills"),
    path("selectEmployee/",selectEmployee,name = "selectEmployee"),
    path("selectEmployee/<int:empid>",employeeVendor,name = "employeeVendor"),
    path("viewBills/<int:vendorid>",vendorBills,name = "vendorBills"),
    path("sendImages/",sendImages,name = "sendImages"),
    path("saveEmployeeVendors/",saveEmployeeVendors,name = "saveEmployeeVendors"),
    path("deleteEmployeeVendors/",deleteEmployeeVendors,name = "deleteEmployeeVendors"),
    
    
    
    
]
urlpatterns+=static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
