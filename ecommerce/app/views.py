import form as form
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views import View
from .models import Product, Customer, Cart
from .forms import CustomerRegistrationForm, PasswordChangeForm, CustomerProfileView
from django.contrib import messages
from django.db.models import Count

def home(request):
    template=loader.get_template('index.html')
    return HttpResponse(template.render())
def about(request):
    template=loader.get_template('about.html')
    return HttpResponse(template.render())
def contact(request):
    template=loader.get_template('contact.html')
    return HttpResponse(template.render())
class CategoryView(View):
    def get(self,request,val):
        product=Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title')
        return render(request,'category.html',locals())
class CategoryTitle(View):
    def get(self,request,val):
     product=Product.objects.filter(title=val)
     title=Product.objects.filter(category=product[0].category).values('title')
     return render(request,'category.html',locals())

class ProductDetail(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        return render(request, 'productdetail.html', locals())

# Create your views here.
class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm
        return render(request,'customerregistration.html',locals())
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Congratulations! user register successfully')
        else:
            messages.warning(request,'Invalid Input Data')
        return render(request, 'customerregistration.html', locals())


class ProfileView(View):
    def get(self,request):
        form=CustomerProfileView()
        return render(request,'profile.html',locals())
    def post(self,request):
        form = CustomerProfileView(request.POST)
        if form.is_valid():
             user=request.user
             name=form.cleaned_data['name']
             locality = form.cleaned_data['locality']
             city = form.cleaned_data['city']
             mobile = form.cleaned_data['mobile']
             state = form.cleaned_data['state']
             zipcode = form.cleaned_data['zipcode']
             reg=Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
             reg.save()
             messages.success(request,"Successfully! you have save the data")
        else:
            messages.warning(request,'Invalid Data')
        return render(request,'profile.html',locals())
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request,'address.html',locals())
class UpdateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileView(instance=add)
        return render(request,'updateaddress.html',locals())
    def post(self,request,pk):
        form=CustomerProfileView(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Successfully! Data Updated!")
        else:
            messages.warning(request,'Invalid Data')
        return  redirect('address')
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/show-cart')
def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.quantity * p.product.discounted_price
        amount=amount+value
    totalamount=amount+40
    return render(request,'addtocart.html',locals())