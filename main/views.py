import urllib.request
import random
import string
import urllib.parse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, logout as _logout, login as _login
def home(request):
    # id_created = ''.join(random.choice(string.digits) for _ in range(6))
    # resp =  sendSMS('Njk0NjQ5NzgzNzM5MzI0MTc5NjYzMjY3NjYzNjc5Mzg=', '916295426049',
    #     'TXTLCL', f'Please Enter This OTP {id_created} To Verify Your Account')
    # print (resp)
    response = render(request, "Main/home.html", {'user':request.user})
    if request.method == "POST":
        name = request.POST['name']
        subject = request.POST['subject']
        email = request.POST['email']
        message = request.POST['message']
        msg = Message.objects.create(name=name, subject=subject, email=email, message=message)
        return render(request, "Main/home.html", {"success":True, "user":request.user})
    return render(request, "Main/home.html", {'user':request.user})

def customer(request):
    response = render(request, "Main/customer.html")
    if request.method == 'POST':
        enrollment_id = request.POST['id']
        password = request.POST['password']
        customer = Enrollment.objects.filter(enrollment_id=enrollment_id , password=password)
        if customer.exists():
            username = Enrollment.objects.filter(enrollment_id=enrollment_id , password=password).last().user.username
            auth = authenticate(username=username, password=password)
            if auth is not None:
                _login(request, auth)
                return render(request, "Main/customer.html", {'success':True})
        else:
            response = render(request, "Main/customer.html", {'error':True, 'message':"Invalid Credentials"})
            return response
    return response

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        auth = authenticate(username=username, password=password)
        if auth is not None:
            _login(request, auth)
            return render(request, "Main/login.html", {'success':True})
        else:
            return render(request, "Main/login.html", {'error': True, 'message':'User Does Not Exist'})
    return render(request, "Main/login.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, "Main/signup.html", {'error':True, 'message':'User Already Exists'})
        else:
            user_created = User.objects.create_user(username=username, password=password)
            auth = authenticate(username=username, password=password)
            if auth is not None:
                _login(request, auth)
            return render(request, "Main/signup.html", {'success':True})
    return render(request, "Main/signup.html")

def logout(request):
    _logout(request)
    return HttpResponseRedirect("/")

def dashboard(request):
    user_detail = UserDetails.objects.filter(user=request.user).last()
    if request.user.is_superuser:
        return HttpResponseRedirect("/admin_dashboard")
    if user_detail.is_dealer:
        return HttpResponseRedirect("/dealer_dashboard")
    if user_detail.is_customer:
        return HttpResponseRedirect("/customer_dashboard")

def dealer_login(request):
    response = render(request, "Main/dealer_login.html")
    if request.method == 'POST':
        dealer_id = request.POST['id']
        password = request.POST['password']
        dealer = Dealer.objects.filter(dealer_id=dealer_id, password=password)
        if dealer.exists():
            username = Dealer.objects.filter(dealer_id=dealer_id, password=password).last().user.username
            auth = authenticate(username=username, password=password)
            if auth is not None:
                _login(request, auth)
                return render(request, "Main/dealer_login.html", {'success':True})
        else:
            response = render(request, "Main/dealer_login.html", {'error':True, 'message':"Invalid Credentials"})
            return response
    return response

def employee(request):
    response = render(request, "Main/employee.html")
    if request.method == 'POST':
        employee_id = request.POST['id']
        password = request.POST['password']
        employee = Employee.objects.filter(employee_id=employee_id , password=password)
        if employee.exists():
            username = Employee.objects.filter(employee_id=employee_id , password=password).last().user.username
            auth = authenticate(username=username, password=password)
            if auth is not None:
                _login(request, auth)
                return render(request, "Main/employee.html", {'success':True})
        else:
            response = render(request, "Main/employee.html", {'error':True, 'message':"Invalid Credentials"})
            return response
    return response




 
def sendSMS(apikey, numbers, sender, message):
    params = {'apikey': apikey, 'numbers': numbers, 'message' : message, 'sender': sender}
    f = urllib.request.urlopen('https://api.textlocal.in/send/?'
        + urllib.parse.urlencode(params))
    return (f.read(), f.code)
