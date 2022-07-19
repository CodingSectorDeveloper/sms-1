import math
import random
import string
from django.shortcuts import render, HttpResponseRedirect
from main.models import *

# Create your views here.

def home(request):
    dealernum = len(Dealer.objects.all())
    msgnum = len(Message.objects.all())
    enrollnum = len(Enrollment.objects.all())
    invested = 0
    # for i in Enrollment.objects.all():
        # invested += i.total_amount
    # invested = "{:,}".format(invested)
    income = 0
    for i in EMI.objects.all():
        income += i.amount
    income = "{:,}".format(income)
    users = len(User.objects.all())
    return render(request, "Admin/home.html", {"dealernum":dealernum,"msgnum":msgnum, "enrollnum":enrollnum, "invested":invested, "users":users, "income":income})

def dealers(request):
    dealer = Dealer.objects.all()
    response = render(request, "Admin/dealers.html", {"dealers":dealer})
    response.set_cookie("test_cookie", "This is the test", max_age=60*60*24*14)
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
        aadhaar = request.FILES['aadhaar']
        aadhaar_back = request.FILES['aadhaar_back']
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

        user_created = User.objects.create_user(username=username, password=password)
        user_detail = UserDetails.objects.create(user=user_created, is_dealer=True)
        dealer_created = Dealer.objects.create(dealer_id=id_created, password=password,aadhaar_back=aadhaar_back, user=user_created, first_name=first_name, last_name=last_name, middle_name=middle_name, dob=dob, gender=gender, father_name=father_name, marital_status=marital_status, spouse_name=spouse_name, shop_name=shop_name, shop_location=shop_location, qualification=qualification, applicant_photo=applicant_photo, shop_photo=shop_photo, aadhaar=aadhaar, voter_id=voter_id, pan_card=pan_card, gst=gst, bill_book=bill_book, ifsc_code=ifsc_code, account_holder_first_name=account_holder_first_name, account_holder_last_name=account_holder_last_name, account_holder_middle_name=account_holder_middle_name, account_number=account_number, bank_name=bank_name, created_by="Admin")
        return render(request, "Admin/create_dealer.html", {"success":True})
    return render(request, "Admin/create_dealer.html", {"id":id_created})

def create_employee(request):
    id_created = ''.join(random.choice(string.digits) for _ in range(6))
    if request.method == 'POST':
        first_name = request.POST['first_name']
        middle_name = request.POST['middle_name']
        last_name = request.POST['last_name']
        dob = request.POST['dob']
        gender = request.POST['gender']
        father_name = request.POST['father_name']
        marital_status = request.POST['maritial_status']
        spouse_name = request.POST['spouse_name']
        qualification = request.POST['qualification']
        password = request.POST['password']
        applicant_photo = request.FILES['applicant_photo']
        experience = request.POST['experience']
        religion = request.POST['religion']
        mobile = request.POST['mobile']
        username = first_name + ' ' + last_name
        
        if Employee.objects.filter(first_name=first_name, last_name=last_name).exists():
            return render(request, "Admin/create_employee.html", {"error":True, "message":"Employee with the same name already exists, Make sure to delete it first."})
        else:
            user_created = User.objects.create_user(username=username, password=password)
            user_detail = UserDetails.objects.create(user=user_created, is_dealer=True)
            employee = Employee.objects.create(employee_id=id_created, password=password, user=user_created, first_name=first_name, last_name=last_name, middle_name=middle_name, dob=dob, gender=gender, father_name=father_name, marital_status=marital_status, spouse_name=spouse_name, qualification=qualification, applicant_photo=applicant_photo, experience=experience, religion=religion, mobile=mobile)
            return render(request, "Admin/create_employee.html", {"success":True})
    return render(request, "Admin/create_employee.html", {"id":id_created})

def delete_dealer(request, id):
    dealer = Dealer.objects.filter(pk=id).last()
    dealer.delete()
    return HttpResponseRedirect("/admin_dashboard/dealers")

def delete_employee(request, id):
    employee = Employee.objects.filter(pk=id).last()
    employee.delete()
    return HttpResponseRedirect("/admin_dashboard/employee")

def enrollment_details(request, id):
    enrollment = Enrollment.objects.filter(pk=id).last()
    return render(request, "Admin/enrollment_details.html", {"enrollment":enrollment}) 

def employee_details(request, id):
    employee = Employee.objects.filter(pk=id).last()
    return render(request, "Admin/employee_details.html", {"employee":employee})
    
def enrollments(request):
    enrollments = Enrollment.objects.all()
    return render(request, "Admin/enrollments.html", {"enrollments":enrollments})

def approval(request):
    enrollments = Enrollment.objects.filter(status="pending")
    return render(request, "Admin/approval.html", {"enrolls":enrollments})

def approval_details(request, id):
    enroll = Enrollment.objects.filter(pk=id).last()
    return render(request, "Admin/approval_details.html", {"enrollment":enroll})

def reject(request, id):
    enroll = Enrollment.objects.filter(pk=id).last()
    enroll.status = "rejected"
    enroll.save()
    return HttpResponseRedirect("/admin_dashboard/approval")

def approve(request, id):
    enroll = Enrollment.objects.filter(pk=id).last()
    enroll.status = "approved"
    enroll.save()
    return HttpResponseRedirect("/admin_dashboard/approval")

def messages(request):
    messages = Message.objects.all()
    return render(request, "Admin/messages.html", {"messages":messages})

def message_details(request, id):
    message = Message.objects.filter(pk=id).last()
    return render(request, "Admin/message_details.html", {"message":message})

def delete_message(request, id):
    Message.objects.filter(pk=id).last().delete()
    return HttpResponseRedirect("/admin_dashboard/messages")

def emi(request):
    emis = EMI.objects.all()
    return render(request, "Admin/emi.html", {"emis":emis})

def profit_loss(request):
    invested_num = 0
    print(Enrollment.objects.all())
    for i in Enrollment.objects.all():
        print(i.total_amount)
        if i.total_amount:
            invested_num += i.total_amount
    invested = "{:,}".format(invested_num)
    income_num = 0
    for i in EMI.objects.all():
        income_num += i.amount
    income = "{:,}".format(income_num)
    profit = 0
    loss = 0
    if invested_num > income_num:
        loss = invested_num - income_num
    elif income_num > invested_num:
        profit_num = income - invested_num
    profit = "{:,}".format(profit)
    loss = "{:,}".format(loss)
    emi = EMI.objects.all()
    enrollmentaccounts = EnrollmentAccount.objects.all()
    return render(request, "Admin/profit_loss.html", {"enrollmentaccounts":enrollmentaccounts, "emis": emi, "investment":invested, "income":income, "profit":profit, "loss":loss})

def employee(request):
    employee = Employee.objects.all()
    print(employee)
    return render(request, "Admin/employee.html", {"employee":employee})

def get_otp(request):
    otp = generateOTP()
    if request.method == "POST":
        mobile_number = request.POST['mobile_number']
        if Enrollment.objects.filter(mobile_number=int(mobile_number)).exists():
            return render(request, "Admin/get_otp.html", {"error":True, "message":"Mobile Number Already Used", "otp":int(otp)-20})
        # sendOTP()
        return render(request, "Admin/get_otp.html", {"success":True, "mobile_number":mobile_number, "otp":int(otp)-20})
    
    return render(request, "Admin/get_otp.html")

def check_otp(request, otp, mobile_number):
    otp = otp + 20
    if request.method == "POST":
        if int(request.POST['otp']) == int(otp):
            print('matched')
            return render(request, "Admin/check_otp.html", {"success":True, "mobile_number":mobile_number})
        else:
            return render(request, "Admin/check_otp.html", {"error":True, "mobile_number":mobile_number})
    return render(request, "Admin/check_otp.html", {"mobile_number":mobile_number})

def create_enrollment(request, mobile_number):
    id_created = ''.join(random.choice(string.digits) for _ in range(6))
    if request.method == 'POST':
        enroll_created = Enrollment.objects.create()
        password = request.POST['password']
        dealer = Dealer.objects.filter(user=request.user).last()
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dob = request.POST['dob']
        gender = request.POST['gender']
        maritial_status = request.POST['maritial_status']
        father_name = request.POST['father_name']
        spouse_name = request.POST['spouse_name']
        middle_name = request.POST['middle_name']
        mobile_number = request.POST['mobile_number']
        profile_image = request.FILES['profile_image']
        admin = request.user


        username = first_name + last_name
        user_created = User.objects.create_user(password=password, username=username)
        user_detail = UserDetails.objects.create(user=user_created, is_customer=True)
        enroll_created.password = password
        enroll_created.user = user_created
        enroll_created.enrollment_id = id_created
        enroll_created.first_name = first_name
        enroll_created.middle_name = middle_name
        enroll_created.last_name = last_name
        enroll_created.dob = dob
        enroll_created.gender = gender
        enroll_created.mobile_number=mobile_number
        enroll_created.maritial_status = maritial_status
        enroll_created.father_name = father_name
        enroll_created.spouse_name = spouse_name
        enroll_created.profile_image = profile_image
        enrollment_created_id = enroll_created.id
        enroll_created.admin = admin.username
        enroll_created.save()
        return render(request, "Admin/create_enrollment.html", {"success":True, "id":enrollment_created_id, "mobile_number":mobile_number, "enroll_created":enroll_created})

    return render(request, "Admin/create_enrollment.html", {"id":id_created, "mobile_number":mobile_number})

def kyc(request, id):
    enrollment = Enrollment.objects.filter(pk=id).last()
    if request.method == 'POST':
        id_proof = request.POST['id_proof']
        pan_number = request.POST['pan_number']
        driver_license = request.POST['driver_license']
        voter_id = request.POST['voter_id']
        consent = request.POST['consent']

        voter_id_image = None
        driver_license_image = None
        pan_image = None

        if id_proof == "Address Source*":
            return render(request, "Admin/kyc.html", {"error":True, "message":"Please Select A Valid Option"})

        if 'pan_image' in request.FILES:
            pan_image = request.FILES['pan_image']
        if 'driver_license_image' in request.FILES:
            driver_license_image = request.FILES['driver_license_image']
        if 'voter_id_image' in request.FILES:
            voter_id_image = request.FILES['voter_id_image']

        enrollment.id_proof = id_proof
        enrollment.pan = pan_number
        enrollment.driver_license = driver_license
        enrollment.voter_id = voter_id
        enrollment.pan_image = pan_image
        enrollment.driver_license_image = driver_license_image
        enrollment.voter_id_image = voter_id_image
        enrollment.consent = consent
        enrollment.save()
        return render(request, 'Admin/kyc.html', {"success":True, "id":enrollment.id, "enrollment":enrollment})
    return render(request, "Admin/kyc.html")

def address(request, id):
    enrollment = Enrollment.objects.filter(pk=id).last()
    if request.method == 'POST':
        address_1 = request.POST['address_1']
        address_2 = request.POST['address_2']
        address_3 = request.POST['address_3']
        pincode = request.POST['pincode']
        city = request.POST['city']
        state = request.POST['state']
        post_office = request.POST['post_office']
        landmark = request.POST['landmark']
        aadhaar_image = request.FILES['aadhaar_image']
        aadhar_image_back = request.FILES['aadhaar_image_back']
        location = request.POST['location']

        enrollment.address_1 = address_1
        enrollment.address_2 = address_2
        enrollment.address_3 = address_3
        enrollment.pincode = pincode
        enrollment.city = city
        enrollment.state = state
        enrollment.post_office = post_office
        enrollment.landmark = landmark
        enrollment.aadhar_image = aadhaar_image
        enrollment.aadhar_image_back = aadhar_image_back
        enrollment.location = location
        enrollment.save()
        return render(request, 'Admin/address.html', {"success":True, "id":enrollment.id, "enrollment":enrollment})
    return render(request, "Admin/address.html")

def personal_information(request, id):
    enrollment = Enrollment.objects.filter(pk=id).last()
    if request.method == 'POST':
        educational_qualification = request.POST['educational_qualification']
        designation = request.POST['designation']
        family_members = request.POST['family_members']
        monthly_income = request.POST['monthly_income']

        enrollment.educational_qualification = educational_qualification
        enrollment.designation = designation
        enrollment.family_members = family_members
        enrollment.monthly_income = monthly_income
        enrollment.save()
        return render(request, "Admin/personal_information.html", {"success":True, "id":enrollment.id, "enrollment":enrollment})
    return render(request, 'Admin/personal_information.html')

def reference_details(request, id):
    enrollment = Enrollment.objects.filter(pk=id).last()
    if request.method == 'POST':
        reference_first_name = request.POST['reference_first_name']
        reference_middle_name = request.POST['reference_middle_name']
        reference_last_name = request.POST['reference_last_name']
        reference_mobile_number = request.POST['reference_mobile_number']
        reference_relation = request.POST['reference_relation']

        enrollment.reference_first_name = reference_first_name
        enrollment.reference_middle_name = reference_middle_name
        enrollment.reference_last_name = reference_last_name
        enrollment.reference_mobile_number = reference_mobile_number
        enrollment.reference_relation = reference_relation
        enrollment.save()
        return render(request, 'Admin/reference_details.html', {'success': True, 'id': enrollment.id, "enrollment":enrollment})
    return render(request, "Admin/reference_details.html")

def product_details(request, id):
    enrollment = Enrollment.objects.filter(pk=id).last()
    if request.method == 'POST':
        product_type = request.POST['product_type']
        product_cost = request.POST['product_cost']

        enrollment.product_type = product_type
        enrollment.product_cost = product_cost
        enrollment.save()
        return render(request, "Admin/product_details.html", {"success":True, "id":enrollment.id, "enrollment":enrollment})
    return render(request, "Admin/product_details.html")

def bank_details(request, id):
    enrollment = Enrollment.objects.filter(pk=id).last()
    if request.method == 'POST':
        ifsc_code = request.POST['ifsc_code']
        account_holder_first_name = request.POST['account_holder_first_name']
        account_holder_last_name = request.POST['account_holder_last_name']
        account_holder_middle_name = request.POST['account_holder_middle_name']
        account_number = request.POST['account_number']
        prospect_no = request.POST['prospect_no']
        period_from = request.POST['period_from']
        period_to = request.POST['period_to']
        umrn = request.POST['umrn']
        bank_name = request.POST['bank_name']

        enrollment.ifsc_code = ifsc_code
        enrollment.prospect_no = prospect_no
        enrollment.period_to = period_to
        enrollment.period_from = period_from
        enrollment.urmn = umrn
        enrollment.account_holder_first_name = account_holder_first_name
        enrollment.account_holder_middle_name = account_holder_middle_name
        enrollment.account_holder_last_name = account_holder_last_name
        enrollment.account_number = account_number
        enrollment.bank_name = bank_name
        enrollment.save()
        return render(request, "Admin/bank_details.html", {"success":True, "id":enrollment.id, "enrollment":enrollment})
    return render(request, "Admin/bank_details.html")

def emi_scheme(request, id):
    enrollment = Enrollment.objects.filter(pk=id).last()
    if request.method == 'POST':
        emi_scheme_plan  = request.POST['emi_scheme_plan']

        enrollment.emi_plan = emi_scheme_plan
        if enrollment.emi_plan == "S Plan":
            enrollment.card = 390
            enrollment.processing_fee = 1790
            enrollment.insurance = 800
            enrollment.total_terms = 8
            enrollment.down_payment_terms = 2
            enrollment.due_amount_terms = 6
            enrollment.margin_money = 0
            enrollment.total_cost = enrollment.product_cost + 800 + 1790
        if enrollment.emi_plan == "M Plan":
            enrollment.card = 390
            enrollment.processing_fee = 1790
            enrollment.insurance = 0
            enrollment.total_terms = 11
            enrollment.down_payment_terms = 3
            enrollment.due_amount_terms = 8
            enrollment.margin_money = 1000
            enrollment.total_cost = enrollment.product_cost + enrollment.processing_fee
        if enrollment.emi_plan == "L Plan":
            enrollment.card = 390
            enrollment.processing_fee = 1790
            enrollment.insurance = 0
            enrollment.total_terms = 15
            enrollment.down_payment_terms = 4
            enrollment.due_amount_terms = 11
            enrollment.total_cost = enrollment.product_cost + enrollment.processing_fee
            enrollment.margin_money = 1000
        enrollment.save()
        return render(request, "Admin/emi_scheme.html", {"success":True, "id":enrollment.id, "enrollment":enrollment})
    return render(request, "Admin/emi_scheme.html")

def product_information(request, id):
    enrollment = Enrollment.objects.filter(pk=id).last()
    if request.method == 'POST':
        imei_product_image = request.FILES['imei_product_image']
        product_model_sl_no = request.POST['product_model_sl_no']
        loan_amount = request.POST['total_amount']

        enrollment.imei_product_image = imei_product_image
        enrollment.total_amount = loan_amount
        enrollment.product_model_sl_no = product_model_sl_no
        if enrollment.emi_plan == "S Plan":
            enrollment.emi = enrollment.total_cost / enrollment.total_terms
            enrollment.down_payment = enrollment.emi * enrollment.down_payment_terms
            enrollment.due_payment = enrollment.emi * enrollment.due_amount_terms
            enrollment.save()
        else:
            enrollment.down_payment = enrollment.total_cost / enrollment.total_terms * enrollment.down_payment_terms + enrollment.margin_money
            enrollment.due_payment = enrollment.total_cost - enrollment.down_payment
            enrollment.emi = enrollment.due_payment / enrollment.due_amount_terms
            enrollment.save()
        return render(request, "Admin/product_information.html", {"success":True, "id":enrollment.id, "enrollment":enrollment})

    return render(request, "Admin/product_information.html")

#  Generate Reciept
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os

def invoice(request, id):

    enrollment = Enrollment.objects.filter(pk=id).first()

    template_path = 'Admin/invoice.html'

    context = {'myvar': 'this is your template context', 'enrollment':enrollment}
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = f'filename="SMS_Financial_Services_{enrollment.first_name} {enrollment.last_name}-receipt.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    result = BytesIO() 
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def preview_first(request, id):
    enrollment = Enrollment.objects.filter(pk=id).last()
    return render(request, "Admin/preview_first.html", {"enrollment":enrollment})

def submit_emi(request):
    if request.method == 'POST':
        enrollment_id = request.POST['id']
        amount = request.POST['amount']
        admin = request.user
        emi = EMI.objects.create(enrollment_id=enrollment_id, amount=amount, admin=admin)
        enrollment = Enrollment.objects.filter(enrollment_id=enrollment_id).last()
        amount_paid = 0
        for i in EMI.objects.filter(enrollment_id=enrollment_id):
            amount_paid += int(i.amount)
        amount_left = int(enrollment.total_amount) - int(amount_paid)
        if EnrollmentAccount.objects.filter(enrollment=enrollment).exists():
            enrollmentaccount = EnrollmentAccount.objects.filter(enrollment=enrollment).last()
            enrollmentaccount.amount_paid = amount_paid
            enrollmentaccount.amount_left = amount_left
            enrollmentaccount.save()
        else:
            enrollmentaccount = EnrollmentAccount.objects.create(enrollment=enrollment, amount_left=amount_left, amount_paid=amount_paid)

        return render(request, "Admin/submit_emi.html", {"success":True})
    return render(request, "Admin/submit_emi.html")

def generateOTP() :
 
    # Declare a digits variable 
    # which stores all digits
    digits = "0123456789"
    OTP = ""
 
   # length of password can be changed
   # by changing value in range
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
 
    return OTP

def edit_enrollment(request, id):
    id_created = ''.join(random.choice(string.digits) for _ in range(6))
    enroll_created = Enrollment.objects.filter(pk=id).last()
    if request.method == 'POST':
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dob = request.POST['dob']
        gender = request.POST['gender']
        mobile_number = request.POST['mobile_number']
        maritial_status = request.POST['maritial_status']
        father_name = request.POST['father_name']
        spouse_name = request.POST['spouse_name']
        middle_name = request.POST['middle_name']
        if 'profile_image' in request.FILES:
            profile_image = request.FILES['profile_image']
        username = first_name + last_name
        enroll_created.password = password
        enroll_created.mobile_number=mobile_number
        enroll_created.enrollment_id = id_created
        enroll_created.first_name = first_name
        enroll_created.middle_name = middle_name
        enroll_created.last_name = last_name
        enroll_created.dob = dob
        enroll_created.gender = gender
        enroll_created.maritial_status = maritial_status
        enroll_created.father_name = father_name
        enroll_created.spouse_name = spouse_name
        if 'profile_image' in request.FILES:
            enroll_created.profile_image = profile_image
        enrollment_created_id = enroll_created.id
        if maritial_status == "Single":
            enroll_created.spouse_name = ""
        enroll_created.save()
        return render(request, "Admin/edit_enrollment.html", {"success":True, "id":enroll_created.id, "enroll_created":enroll_created})

    return render(request, "Admin/edit_enrollment.html", {"enroll_created": enroll_created, "id":enroll_created.id})

def edit_kyc(request, id):
    enrollment = Enrollment.objects.filter(pk=id).last()
    if request.method == 'POST':
        id_proof = request.POST['id_proof']
        pan_number = request.POST['pan_number']
        driver_license = request.POST['driver_license']
        voter_id = request.POST['voter_id']
        consent = request.POST['consent']

        if id_proof == "Address Source*":
            return render(request, "Admin/kyc.html", {"error":True, "message":"Please Select A Valid Option"})

        if 'pan_image' in request.FILES:
            pan_image = request.FILES['pan_image']
        if 'driver_license_image' in request.FILES:
            driver_license_image = request.FILES['driver_license_image']
        if 'voter_id_image' in request.FILES:
            voter_id_image = request.FILES['voter_id_image']

        enrollment.id_proof = id_proof
        enrollment.pan = pan_number
        enrollment.driver_license = driver_license
        enrollment.voter_id = voter_id
        if 'pan_image' in request.FILES:
            enrollment.pan_image = pan_image
        if 'driver_license_image' in request.FILES:
            enrollment.driver_license_image = driver_license_image
        if 'voter_id_image' in request.FILES:
            enrollment.voter_id_image = voter_id_image
        enrollment.consent = consent
        enrollment.save()
        return render(request, 'Admin/edit_kyc.html', {"success":True, "id":enrollment.id, "enrollment":enrollment})
    return render(request, "Admin/edit_kyc.html", {"enrollment":enrollment})

def edit_address(request, id):
    enrollment = Enrollment.objects.filter(pk=id).last()
    if request.method == 'POST':
        address_1 = request.POST['address_1']
        address_2 = request.POST['address_2']
        address_3 = request.POST['address_3']
        pincode = request.POST['pincode']
        city = request.POST['city']
        state = request.POST['state']
        post_office = request.POST['post_office']
        landmark = request.POST['landmark']
        if 'aadhaar_image' in request.FILES:
            aadhaar_image = request.FILES['aadhaar_image']
        if 'aadhaar_image_back' in request.FILES:
            aadhar_image_back = request.FILES['aadhaar_image_back']
        location = request.POST['location']

        enrollment.address_1 = address_1
        enrollment.address_2 = address_2
        enrollment.address_3 = address_3
        enrollment.pincode = pincode
        enrollment.city = city
        enrollment.state = state
        enrollment.post_office = post_office
        enrollment.landmark = landmark
        if 'aadhaar_image' in request.FILES:
            enrollment.aadhar_image = aadhaar_image
        if 'aadhaar_image_back' in request.FILES:
            enrollment.aadhar_image_back = aadhar_image_back
        enrollment.location = location
        enrollment.save()
        return render(request, 'Admin/edit_address.html', {"success":True, "id":enrollment.id, "enrollment":enrollment})
    return render(request, "Admin/edit_address.html", {"enrollment": enrollment})

def edit_personal_information(request, id):
    enrollment = Enrollment.objects.filter(pk=id).last()
    if request.method == 'POST':
        educational_qualification = request.POST['educational_qualification']
        designation = request.POST['designation']
        family_members = request.POST['family_members']
        monthly_income = request.POST['monthly_income']

        enrollment.educational_qualification = educational_qualification
        enrollment.designation = designation
        enrollment.family_members = family_members
        enrollment.monthly_income = monthly_income
        enrollment.save()
        return render(request, "Admin/edit_personal_information.html", {"success":True, "id":enrollment.id, "enrollment":enrollment})
    return render(request, 'Admin/edit_personal_information.html', {"enrollment":enrollment})

def edit_reference_details(request, id):
    enrollment = Enrollment.objects.filter(pk=id).last()
    if request.method == 'POST':
        reference_first_name = request.POST['reference_first_name']
        reference_middle_name = request.POST['reference_middle_name']
        reference_last_name = request.POST['reference_last_name']
        reference_mobile_number = request.POST['reference_mobile_number']
        reference_relation = request.POST['reference_relation']

        enrollment.reference_first_name = reference_first_name
        enrollment.reference_middle_name = reference_middle_name
        enrollment.reference_last_name = reference_last_name
        enrollment.reference_mobile_number = reference_mobile_number
        enrollment.reference_relation = reference_relation
        enrollment.save()
        return render(request, 'Admin/edit_reference_details.html', {'success': True, 'id': enrollment.id, "enrollment":enrollment})
    return render(request, "Admin/edit_reference_details.html", {"enrollment":enrollment})

def edit_product_details(request, id):
    enrollment = Enrollment.objects.filter(pk=id).last()
    if request.method == 'POST':
        product_type = request.POST['product_type']
        product_cost = request.POST['product_cost']

        enrollment.product_type = product_type
        enrollment.product_cost = product_cost
        enrollment.save()
        return render(request, "Admin/edit_product_details.html", {"success":True, "id":enrollment.id, "enrollment":enrollment})
    return render(request, "Admin/edit_product_details.html", {"enrollment":enrollment})

def edit_bank_details(request, id):
    enrollment = Enrollment.objects.filter(pk=id).last()
    if request.method == 'POST':
        ifsc_code = request.POST['ifsc_code']
        account_holder_first_name = request.POST['account_holder_first_name']
        account_holder_last_name = request.POST['account_holder_last_name']
        account_holder_middle_name = request.POST['account_holder_middle_name']
        account_number = request.POST['account_number']
        prospect_no = request.POST['prospect_no']
        period_from = request.POST['period_from']
        period_to = request.POST['period_to']
        umrn = request.POST['umrn']
        bank_name = request.POST['bank_name']

        enrollment.ifsc_code = ifsc_code
        enrollment.prospect_no = prospect_no
        enrollment.period_to = period_to
        enrollment.period_from = period_from
        enrollment.urmn = umrn
        enrollment.account_holder_first_name = account_holder_first_name
        enrollment.account_holder_middle_name = account_holder_middle_name
        enrollment.account_holder_last_name = account_holder_last_name
        enrollment.account_number = account_number
        enrollment.bank_name = bank_name
        enrollment.save()
        return render(request, "Admin/edit_bank_details.html", {"success":True, "id":enrollment.id, "enrollment":enrollment})
    return render(request, "Admin/edit_bank_details.html", {"enrollment":enrollment})

def edit_emi_scheme(request, id):
    enrollment = Enrollment.objects.filter(pk=id).last()
    if request.method == 'POST':
        emi_scheme_plan  = request.POST['emi_scheme_plan']

        enrollment.emi_plan = emi_scheme_plan
        if enrollment.emi_plan == "S Plan":
            enrollment.card = 390
            enrollment.processing_fee = 1790
            enrollment.insurance = 800
            enrollment.total_terms = 8
            enrollment.down_payment_terms = 2
            enrollment.due_amount_terms = 6
            enrollment.margin_money = 0
            enrollment.total_cost = enrollment.product_cost + 800 + 1790
        if enrollment.emi_plan == "M Plan":
            enrollment.card = 390
            enrollment.processing_fee = 1790
            enrollment.insurance = 0
            enrollment.total_terms = 11
            enrollment.down_payment_terms = 3
            enrollment.due_amount_terms = 8
            enrollment.margin_money = 1000
            enrollment.total_cost = enrollment.product_cost + enrollment.processing_fee
        if enrollment.emi_plan == "L Plan":
            enrollment.card = 390
            enrollment.processing_fee = 1790
            enrollment.insurance = 0
            enrollment.total_terms = 15
            enrollment.down_payment_terms = 4
            enrollment.due_amount_terms = 11
            enrollment.margin_money = 1000
            enrollment.total_cost = enrollment.product_cost + enrollment.processing_fee
        enrollment.save()
        return render(request, "Admin/edit_emi_scheme.html", {"enrollment":enrollment, "success":True, "id":enrollment.id})
    return render(request, "Admin/edit_emi_scheme.html", {"enrollment":enrollment})

def edit_product_information(request, id):
    enrollment = Enrollment.objects.filter(pk=id).last()
    if request.method == 'POST':
        if 'imei_product_image' in request.FILES:
            imei_product_image = request.FILES['imei_product_image']
        product_model_sl_no = request.POST['product_model_sl_no']
        loan_amount = request.POST['total_amount']
        if 'imei_product_image' in request.FILES:
            enrollment.imei_product_image = imei_product_image
        enrollment.product_model_sl_no = product_model_sl_no
        enrollment.total_amount = loan_amount
        if enrollment.emi_plan == "S Plan":
            enrollment.emi = enrollment.total_cost / enrollment.total_terms
            enrollment.down_payment = enrollment.emi * enrollment.down_payment_terms
            enrollment.due_payment = enrollment.emi * enrollment.due_amount_terms
            enrollment.save()
        else:
            enrollment.down_payment = enrollment.total_cost / enrollment.total_terms * enrollment.down_payment_terms + enrollment.margin_money
            enrollment.due_payment = enrollment.total_cost - enrollment.down_payment
            enrollment.emi = enrollment.due_payment / enrollment.due_amount_terms
            enrollment.save()
        return render(request, "Admin/edit_product_information.html", {"success":True, "id":enrollment.id, "enrollment":enrollment})

    return render(request, "Admin/edit_product_information.html", {"enrollment":enrollment})