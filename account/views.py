from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm,CreateUserForm,CustomerForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group
from .filters import *
# Create your views here.

@login_required(login_url='/login')
@allowed_users(allowed_roles=['customers'])
def Profile(request):
    order = request.user.customer.order_set.all()
    pending = order.filter(status='Pending').count()
    total = order.all().count()
    delivered = order.filter(status='delivered').count()
    context = {'pending':pending,'total':total,'delivered':delivered,'orders':order}
    return render(request,'account/User.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])
def profile_settings(request):
    customer = Customer.objects.get(user=request.user)
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST,request.FILES,instance=customer)
        #in form image is present so request.files needed
        #here instance is to make sure we are updating the same form and not creating new one
        if form.is_valid():
            form.save()
            return redirect('/user')
    context ={'form':form}
    return render(request,'account/account_settings.html',context)

@unauthenticated_user
def Login(request):
    
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.info(request,'username or password incorrect!')
            #return render(request,'account/Login.html')
    return render(request,'account/Login.html')

def logoutUser(request):
    logout(request)
    return redirect('/login')

@unauthenticated_user
def Register(request):
    form = CreateUserForm()
    if request.method=='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username=form.cleaned_data.get('username')
            #group = Group.objects.get(name='customers')
            #user.groups.add(group)
            #Customer.objects.create(
             #   user=user,
              #  name=user.username,)
            messages.success(request,'Account created for' + username)
            return redirect('/login')
    context={'form':form}
    return render(request,'account/Register.html',context)

@login_required(login_url='/login')
#@allowed_users(allowed_roles=['admins'])
@admin_only
def Home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    
    pending = orders.filter(status='Pending').count()
    total = orders.all().count()
    delivered = orders.filter(status='delivered').count()
    context = {'pending':pending,'total':total,'delivered':delivered,'customers':customers,'orders':orders}
    return render(request,'account/Dashboard.html',context)

@login_required(login_url='/login')
@allowed_users(allowed_roles=['admins'])
def Con(request,pk):
    customer = Customer.objects.get(id=pk)
    order = customer.order_set.all()
    filterset = OrderFilter(request.GET, queryset=order)
    order = filterset.qs

    context = {'customer':customer,'order':order.count(),'orders':order,'filterset':filterset}
    return render(request,'account/Customers.html',context)

@login_required(login_url='/login')
@allowed_users(allowed_roles=['admins'])
def Products(request):
    products = Product.objects.all()
    return render(request,'account/Products.html',{'products':products})

@login_required(login_url='/login')
@allowed_users(allowed_roles=['admins'])
def create_order(request,pk):
    customer = Customer.objects.get(id=pk)
    form = OrderForm(initial={'customer':customer})
    
    if request.method=='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'account/order_form.html',context)

@login_required(login_url='/login')
@allowed_users(allowed_roles=['admins'])
def update_order(request,pk):
    orders = Order.objects.get(id=pk)
    form = OrderForm(instance=orders)
    #instance = orders means we are filling orderform with existng data
    if request.method=='POST':
        form = OrderForm(request.POST,instance=orders)
        # here instance is to make sure we are not creating a new order and we are instead updating an existing instance
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context={'form':form}
    return render(request,'account/order_form.html',context)

@login_required(login_url='/login')
@allowed_users(allowed_roles=['admins'])
def delete_order(request,pk):
    order = Order.objects.get(id=pk)
    if request.method=='POST':
        order.delete()
        return redirect('/')
    context={'item':order}
    return render(request,'account/delete.html',context)