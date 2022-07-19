from django.shortcuts import render, HttpResponse, HttpResponseRedirect
import random
import math
import string
from main.models import *

def home(request):
    enrollnum = len(Enrollment.objects.filter(dealer=Dealer.objects.filter(user=request.user).last()))
    eminum = len(EMI.objects.filter(dealer=Dealer.objects.filter(user=request.user).last()))
    return render(request, "Dealer/home.html", {"enroll":enrollnum, "emi":eminum})

def enrollments(request):
    enrollments = Enrollment.objects.filter(dealer=Dealer.objects.filter(user=request.user).last())
    return render(request, "Dealer/enrollments.html", {"enrollments":enrollments})

def get_otp(request):
    otp = generateOTP()
    if request.method == "POST":
        mobile_number = request.POST['mobile_number']
        if Enrollment.objects.filter(mobile_number=int(mobile_number)).exists():
            return render(request, "Dealer/get_otp.html", {"error":True, "message":"Mobile Number Already Used", "otp":int(otp)-20})
        # sendOTP()
        return render(request, "Dealer/get_otp.html", {"success":True, "mobile_number":mobile_number, "otp":int(otp)-20})
    
    return render(request, "Dealer/get_otp.html")

def check_otp(request, otp, mobile_number):
    otp = otp + 20
    if request.method == "POST":
        if int(request.POST['otp']) == int(otp):
            print('matched')
            return render(request, "Dealer/check_otp.html", {"success":True, "mobile_number":mobile_number})
        else:
            return render(request, "Dealer/check_otp.html", {"error":True, "mobile_number":mobile_number})
    return render(request, "Dealer/check_otp.html", {"mobile_number":mobile_number})

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
        mobile_number = request.POST['mobile_number']
        maritial_status = request.POST['maritial_status']
        father_name = request.POST['father_name']
        spouse_name = request.POST['spouse_name']
        middle_name = request.POST['middle_name']
        profile_image = request.FILES['profile_image']
        username = first_name + last_name
        user_created = User.objects.create_user(password=password, username=username)
        user_detail = UserDetails.objects.create(user=user_created, is_customer=True)
        enroll_created.password = password
        enroll_created.user = user_created
        enroll_created.mobile_number=mobile_number
        enroll_created.enrollment_id = id_created
        enroll_created.dealer = dealer
        enroll_created.first_name = first_name
        enroll_created.middle_name = middle_name
        enroll_created.last_name = last_name
        enroll_created.dob = dob
        enroll_created.gender = gender
        enroll_created.maritial_status = maritial_status
        enroll_created.father_name = father_name
        enroll_created.spouse_name = spouse_name
        enroll_created.profile_image = profile_image
        enrollment_created_id = enroll_created.id
        enroll_created.save()
        return render(request, "Dealer/create_enrollment.html",{"mobile_number":mobile_number, "success":True, "id":enrollment_created_id, "enroll_created":enroll_created})

    return render(request, "Dealer/create_enrollment.html", {"mobile_number":mobile_number})
    
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
            return render(request, "Dealer/kyc.html", {"error":True, "message":"Please Select A Valid Option"})

        if 'pan_image' in request.FILES:
            pan_image = request.FILES['pan_image']
        if 'driver_license_image' in request.FILES:
            driver_license_image = request.FILES['driver_license_image']
        if 'voter_id_image' in request.FILES:
            voter_id_image = request.FILES['voter_id_image']

        enrollment.id_proof = id_proof
        enrollment.pan_number = pan_number
        enrollment.driver_license = driver_license
        enrollment.voter_id = voter_id
        enrollment.pan_image = pan_image
        enrollment.driver_license_image = driver_license_image
        enrollment.voter_id_image = voter_id_image
        enrollment.consent = consent
        enrollment.save()
        return render(request, 'Dealer/kyc.html', {"success":True, "id":enrollment.id, "enrollment":enrollment})
    return render(request, "Dealer/kyc.html")

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
        return render(request, 'Dealer/address.html', {"success":True, "id":enrollment.id})
    return render(request, "Dealer/address.html")

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
        return render(request, "Dealer/personal_information.html", {"success":True, "id":enrollment.id})
    return render(request, 'Dealer/personal_information.html')

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
        return render(request, 'Dealer/reference_details.html', {'success': True, 'id': enrollment.id})
    return render(request, "Dealer/reference_details.html")

def product_details(request, id):
    enrollment = Enrollment.objects.filter(pk=id).last()
    if request.method == 'POST':
        product_type = request.POST['product_type']
        product_cost = request.POST['product_cost']

        enrollment.product_type = product_type
        enrollment.product_cost = product_cost
        enrollment.save()
        return render(request, "Dealer/product_details.html", {"success":True, "id":enrollment.id})
    return render(request, "Dealer/product_details.html")

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
        return render(request, "Dealer/bank_details.html", {"success":True, "id":enrollment.id})
    return render(request, "Dealer/bank_details.html")

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
            enrollment.margin_money = 1000
            enrollment.total_cost = enrollment.product_cost + enrollment.processing_fee
        enrollment.save()
        return render(request, "Dealer/emi_scheme.html", {"success":True, "id":enrollment.id})
    return render(request, "Dealer/emi_scheme.html")

def product_information(request, id):
    enrollment = Enrollment.objects.filter(pk=id).last()
    if request.method == 'POST':
        imei_product_image = request.FILES['imei_product_image']
        product_model_sl_no = request.POST['product_model_sl_no']
        loan_amount = request.POST['total_amount']
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
        return render(request, "Dealer/product_information.html", {"success":True, "id":enrollment.id})

    return render(request, "Dealer/product_information.html")

#  Generate Reciept
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os

def invoice(request, id):

    enrollment = Enrollment.objects.filter(pk=id).first()

    template_path = 'Dealer/invoice.html'

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
    return render(request, "Dealer/preview_first.html", {"enrollment":enrollment})

def enrollment_details(request, id):
    enrollment = Enrollment.objects.filter(pk=id).last()
    return render(request, "Dealer/enrollment_details.html", {"enrollment":enrollment})

def submit_emi(request):
    if request.method == 'POST':
        enrollment_id = request.POST['id']
        amount = request.POST['amount']
        dealer = Dealer.objects.filter(user=request.user).last()
        emi = EMI.objects.create(enrollment_id=enrollment_id, amount=amount, dealer=dealer)
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

        return render(request, "Dealer/submit_emi.html", {"success":True})
    return render(request, "Dealer/submit_emi.html")

def emi(request):
    emis = EMI.objects.filter(dealer=Dealer.objects.filter(user=request.user).last())
    return render(request, "Dealer/emi.html", {"emis":emis})


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
        dealer = Dealer.objects.filter(user=request.user).last()
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
        enroll_created.dealer = dealer
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
        return render(request, "Dealer/edit_enrollment.html", {"success":True, "id":enroll_created.id, "enroll_created":enroll_created})

    return render(request, "Dealer/edit_enrollment.html", {"enroll_created": enroll_created, "id":enroll_created.id})

def edit_kyc(request, id):
    enrollment = Enrollment.objects.filter(pk=id).last()
    if request.method == 'POST':
        id_proof = request.POST['id_proof']
        pan_number = request.POST['pan_number']
        driver_license = request.POST['driver_license']
        voter_id = request.POST['voter_id']
        consent = request.POST['consent']

        if id_proof == "Address Source*":
            return render(request, "Dealer/kyc.html", {"error":True, "message":"Please Select A Valid Option"})

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
        return render(request, 'Dealer/edit_kyc.html', {"success":True, "id":enrollment.id, "enrollment":enrollment})
    return render(request, "Dealer/edit_kyc.html", {"enrollment":enrollment})

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
        return render(request, 'Dealer/edit_address.html', {"success":True, "id":enrollment.id, "enrollment":enrollment})
    return render(request, "Dealer/edit_address.html", {"enrollment": enrollment})

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
        return render(request, "Dealer/edit_personal_information.html", {"success":True, "id":enrollment.id, "enrollment":enrollment})
    return render(request, 'Dealer/edit_personal_information.html', {"enrollment":enrollment})

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
        return render(request, 'Dealer/edit_reference_details.html', {'success': True, 'id': enrollment.id, "enrollment":enrollment})
    return render(request, "Dealer/edit_reference_details.html", {"enrollment":enrollment})

def edit_product_details(request, id):
    enrollment = Enrollment.objects.filter(pk=id).last()
    if request.method == 'POST':
        product_type = request.POST['product_type']
        product_cost = request.POST['product_cost']

        enrollment.product_type = product_type
        enrollment.product_cost = product_cost
        enrollment.save()
        return render(request, "Dealer/edit_product_details.html", {"success":True, "id":enrollment.id, "enrollment":enrollment})
    return render(request, "Dealer/edit_product_details.html", {"enrollment":enrollment})

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
        return render(request, "Dealer/edit_bank_details.html", {"success":True, "id":enrollment.id, "enrollment":enrollment})
    return render(request, "Dealer/edit_bank_details.html", {"enrollment":enrollment})

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
        return render(request, "Dealer/edit_emi_scheme.html", {"enrollment":enrollment, "success":True, "id":enrollment.id})
    return render(request, "Dealer/edit_emi_scheme.html", {"enrollment":enrollment})

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
        return render(request, "Dealer/edit_product_information.html", {"success":True, "id":enrollment.id, "enrollment":enrollment})

    return render(request, "Dealer/edit_product_information.html", {"enrollment":enrollment})