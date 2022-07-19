from django.db import models
from django.contrib.auth.models import User


class Franchisee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    enrollment_id = models.TextField()
    password = models.TextField()
    total_amount = models.IntegerField(blank=True, null=True)
    admin = models.TextField(null=True, blank=True)
    status = models.TextField(default="pending", blank=True)
    # First Page
    first_name = models.TextField(blank=True, null=True)
    middle_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    mobile_number = models.IntegerField(max_length=10, blank=True, null=True)
    maritial_status = models.TextField(blank=True, null=True)
    father_name = models.TextField(blank=True, null=True)
    spouse_name = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile_images", blank=True, null=True)
    # Second Page (KYC)
    id_proof = models.TextField(blank=True, null=True)
    pan = models.TextField(null=True, blank=True)
    pan_image = models.TextField(null=True, blank=True)
    voter_id = models.TextField(null=True, blank=True)
    voter_id_image = models.TextField(null=True, blank=True)
    driver_license = models.TextField(null=True, blank=True)
    driver_license_image = models.TextField(null=True, blank=True)
    consent = models.BooleanField(default=True)
    # Second (Address)
    address_1 = models.TextField(blank=True, null=True)
    address_2 = models.TextField(blank=True, null=True)
    address_3 = models.TextField(blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    post_office = models.TextField(blank=True, null=True)
    landmark = models.TextField(blank=True, null=True)
    aadhar_image = models.ImageField(blank=True, null=True, upload_to="aadhar_images")
    aadhar_image_back = models.ImageField(blank=True, null=True, upload_to="aadhar_back_images")
    location = models.TextField(blank=True, null=True)

    # Third Page (Personal Details)
    educational_qualification = models.TextField(blank=True, null=True) # SSC, 12th, Under Graduate, Graduate, Post Graduate, Professional, Others
    designation = models.TextField(blank=True, null=True)
    family_members = models.IntegerField(blank=True, null=True)
    monthly_income = models.IntegerField(blank=True, null=True)

    #Sixth Page ( Bank Details)
    ifsc_code = models.TextField(blank=True, null=True)
    account_holder_first_name = models.TextField(blank=True, null=True)
    account_holder_middle_name = models.TextField(blank=True, null=True)
    account_holder_last_name = models.TextField(blank=True, null=True)
    account_number = models.TextField(blank=True, null=True)
    bank_name = models.TextField(blank=True, null=True)

    invoice_date = models.DateField(auto_now_add=True, null=True, blank=True)

class Employee(models.Model):
    first_name = models.TextField(blank=True, null=True)
    middle_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    mobile = models.IntegerField(blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.TextField(blank=True, null=True)
    applicant_photo = models.ImageField(upload_to='employee_image', null=True)
    father_name = models.TextField(blank=True, null=True)
    marital_status = models.TextField(blank=True, null=True)
    spouse_name = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    religion = models.TextField(blank=True, null=True)
    qualification = models.TextField(blank=True, null=True)
    employee_id = models.TextField(unique=True, blank=False)
    password = models.TextField()
    created_by = models.TextField(null=True, blank=True)
    franchisee = models.ForeignKey(Franchisee, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.employee_id

class Dealer(models.Model):
    dealer_id = models.TextField(unique=True, blank=False)
    password = models.TextField()
    first_name = models.TextField(blank=True, null=True)
    middle_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.TextField(blank=True, null=True)
    father_name = models.TextField(blank=True, null=True)
    marital_status = models.TextField(blank=True, null=True)
    spouse_name = models.TextField(blank=True, null=True)
    shop_name = models.TextField(blank=True, null=True)
    shop_location = models.TextField(blank=True, null=True)
    qualification = models.TextField(blank=True, null=True)
    applicant_photo = models.ImageField(upload_to="dealer_applicant_photo", blank=True, null=True)
    shop_photo = models.ImageField(upload_to="dealer_shop_photo", blank=True, null=True)
    aadhaar = models.ImageField(upload_to="dealer_aadhar", blank=True, null=True)
    aadhaar_back = models.ImageField(upload_to="dealer_aadhaar_back", blank=True, null=True)
    voter_id = models.ImageField(upload_to="dealer_voter_id", blank=True, null=True)
    pan_card = models.ImageField(upload_to="dealer_pan_card", blank=True, null=True)
    gst = models.ImageField(upload_to="dealer_gst", blank=True, null=True)
    bill_book = models.ImageField(upload_to="dealer_bill_book", blank=True, null=True)
    ifsc_code = models.TextField(blank=True, null=True)
    account_holder_first_name = models.TextField(blank=True, null=True)
    account_holder_middle_name = models.TextField(blank=True, null=True)
    account_holder_last_name = models.TextField(blank=True, null=True)
    account_number = models.TextField(blank=True, null=True)
    bank_name = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_by = models.TextField(null=True, blank=True)
    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.dealer_id

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    enrollment_id = models.TextField()
    password = models.TextField()
    total_amount = models.IntegerField(blank=True, null=True)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, null=True, blank=True)
    admin = models.TextField(null=True, blank=True)
    status = models.TextField(default="pending", blank=True)
    # First Page
    first_name = models.TextField(blank=True, null=True)
    middle_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    mobile_number = models.IntegerField(max_length=10, blank=True, null=True)
    maritial_status = models.TextField(blank=True, null=True)
    father_name = models.TextField(blank=True, null=True)
    spouse_name = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile_images", blank=True, null=True)
    # Second Page (KYC)
    id_proof = models.TextField(blank=True, null=True)
    pan = models.TextField(null=True, blank=True)
    pan_image = models.TextField(null=True, blank=True)
    voter_id = models.TextField(null=True, blank=True)
    voter_id_image = models.TextField(null=True, blank=True)
    driver_license = models.TextField(null=True, blank=True)
    driver_license_image = models.TextField(null=True, blank=True)
    consent = models.BooleanField(default=True)
    # Second (Address)
    address_1 = models.TextField(blank=True, null=True)
    address_2 = models.TextField(blank=True, null=True)
    address_3 = models.TextField(blank=True, null=True)
    pincode = models.IntegerField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    post_office = models.TextField(blank=True, null=True)
    landmark = models.TextField(blank=True, null=True)
    aadhar_image = models.ImageField(blank=True, null=True, upload_to="aadhar_images")
    aadhar_image_back = models.ImageField(blank=True, null=True, upload_to="aadhar_back_images")
    location = models.TextField(blank=True, null=True)

    # Third Page (Personal Details)
    educational_qualification = models.TextField(blank=True, null=True) # SSC, 12th, Under Graduate, Graduate, Post Graduate, Professional, Others
    designation = models.TextField(blank=True, null=True)
    family_members = models.IntegerField(blank=True, null=True)
    monthly_income = models.IntegerField(blank=True, null=True)

    # Fourth Page (Reference Details)
    reference_first_name = models.TextField(blank=True, null=True)
    reference_middle_name = models.TextField(blank=True, null=True)
    reference_last_name = models.TextField(blank=True, null=True)
    reference_mobile_number = models.TextField(blank=True, null=True)
    reference_relation = models.TextField(blank=True, null=True)

    # Fifth Page (Product Details) 
    product_type = models.TextField(blank=True, null=True)
    product_cost = models.IntegerField(blank=True, null=True)

    # Sixth Page (EMI Scheme)
    emi_plan = models.TextField(blank=True, null=True)
    down_payment = models.IntegerField(blank=True, null=True)
    down_payment_terms = models.IntegerField(blank=True, null=True)
    due_amount_terms = models.IntegerField(blank=True, null=True)
    total_terms = models.IntegerField(blank=True, null=True)
    margin_money = models.IntegerField(blank=True, null=True)
    due_payment = models.IntegerField(blank=True, null=True)
    emi = models.IntegerField(blank=True, null=True)
    card = models.IntegerField(blank=True, null=True)
    processing_fee = models.IntegerField(blank=True, null=True)
    insurance = models.IntegerField(blank=True, null=True)
    total_cost = models.IntegerField(blank=True, null=True)

    # Seventh Page (Producs Information)
    imei_product_image = models.ImageField(blank=True, null=True, upload_to="imei_product_image/")
    product_model_sl_no = models.TextField(blank=True, null=True)

    #Sixth Page ( Bank Details)
    ifsc_code = models.TextField(blank=True, null=True)
    urmn = models.TextField(blank=True, null=True)
    period_from = models.TextField(blank=True, null=True)
    period_to = models.TextField(blank=True, null=True)
    prospect_no = models.TextField(blank=True, null=True)
    account_holder_first_name = models.TextField(blank=True, null=True)
    account_holder_middle_name = models.TextField(blank=True, null=True)
    account_holder_last_name = models.TextField(blank=True, null=True)
    account_number = models.TextField(blank=True, null=True)
    bank_name = models.TextField(blank=True, null=True)

    invoice_date = models.DateField(auto_now_add=True, null=True, blank=True)

class Message(models.Model):
    name = models.TextField()
    subject = models.TextField()
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.subject + " - " + self.name

class EMI(models.Model):
    enrollment_id = models.TextField()
    amount = models.IntegerField(default=0)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, null=True, blank=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"{self.enrollment_id} - {self.amount}"

class UserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_dealer = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class EnrollmentAccount(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    amount_left = models.IntegerField()
    amount_paid = models.IntegerField()