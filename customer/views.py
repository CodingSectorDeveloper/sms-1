from django.shortcuts import render
from main.models import *

def home(request):
    enrollment_account = EnrollmentAccount.objects.filter(enrollment=Enrollment.objects.filter(user=request.user).last()).last()
    return render(request, "Customer/home.html", {"enrollment_account":enrollment_account})

def emi(request):
    enroll_id = Enrollment.objects.filter(user=request.user).last().enrollment_id
    emis = EMI.objects.filter(enrollment_id=enroll_id)
    return render(request, "Customer/emi.html", {"emis":emis, "enrollment_account":enrollment_account})