import random
import math
import string
from django.shortcuts import render,HttpResponseRedirect, HttpResponse
from main.models import *

def home(request):
    return render(request, "Employee/home.html")

def approval(request):
    enrollments = Enrollment.objects.filter(status="pending")
    return render(request, "Employee/approval.html", {"enrolls":enrollments})

def approval_details(request, id):
    enroll = Enrollment.objects.filter(pk=id).last()
    return render(request, "Employee/approval_details.html", {"enrollment":enroll})

def reject(request, id):
    enroll = Enrollment.objects.filter(pk=id).last()
    enroll.status = "rejected"
    enroll.save()
    return HttpResponseRedirect("/employee_dashboard/approval")

def approve(request, id):
    enroll = Enrollment.objects.filter(pk=id).last()
    enroll.status = "approved"
    enroll.save()
    return HttpResponseRedirect("/employee_dashboard/approval")


def dealers(request):
    dealer = Dealer.objects.filter(employee=Employee.objects.filter(user=request.user).last())
    response = render(request, "Employee/dealers.html", {"dealers":dealer})
    return response

def create_dealer(request):
    id_created = ''.join(random.choice(string.digits) for _ in range(6))
    if request.method == 'POST':
        first_name = request.POST['first_name']
        middle_name = request.POST['middle_name']
        last_name = request.POST['last_name']
        dob = request.POST['dob']
        gender = request.POST['gender']
        father_name = request.POST['father_name']
        marital_status = request.POST['marital_status']
        spouse_name = request.POST['spouse_name']
        shop_name = request.POST['shop_name']
        shop_location = request.POST['shop_location']
        qualification = request.POST['qualification']
        password = request.POST['password']
        applicant_photo = request.FILES['applicant_photo']
        shop_photo = request.FILES['shop_photo']
        aadhaar_back = request.FILES['aadhaar_back']
        aadhaar = request.FILES['aadhaar']
        voter_id = request.FILES['voter_id']
        pan_card = request.FILES['pan_card']
        gst = request.FILES['gst']
        bill_book = request.FILES['bill_book']
        ifsc_code = request.POST['ifsc_code']
        account_holder_first_name = request.POST['account_holder_first_name']
        account_holder_last_name = request.POST['account_holder_last_name']
        account_holder_middle_name = request.POST['account_holder_middle_name']
        bank_name = request.POST['bank_name']
        account_number = request.POST['account_number']
        username = first_name + ' ' + last_name
        employee = Employee.objects.filter(user=request.user).last()

        user_created = User.objects.create_user(username=username, password=password)
        user_detail = UserDetails.objects.create(user=user_created, is_dealer=True)
        dealer_created = Dealer.objects.create(dealer_id=id_created, password=password,employee=employee, aadhaar_back=aadhaar_back, user=user_created, first_name=first_name, last_name=last_name, middle_name=middle_name, dob=dob, gender=gender, father_name=father_name, marital_status=marital_status, spouse_name=spouse_name, shop_name=shop_name, shop_location=shop_location, qualification=qualification, applicant_photo=applicant_photo, shop_photo=shop_photo, aadhaar=aadhaar, voter_id=voter_id, pan_card=pan_card, gst=gst, bill_book=bill_book, ifsc_code=ifsc_code, account_holder_first_name=account_holder_first_name, account_holder_last_name=account_holder_last_name, account_holder_middle_name=account_holder_middle_name, account_number=account_number, bank_name=bank_name, created_by="Employee")
        return render(request, "Employee/create_dealer.html", {"success":True})
    return render(request, "Employee/create_dealer.html", {"id":id_created})
    
def dealer_details(request, id):
    dealer = Dealer.objects.filter(pk=id).last()
    return render(request, "Employee/dealer_details.html", {"dealer":dealer})