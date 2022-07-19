from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('enrollments/', views.enrollments, name="enrollments"),
    path('submit_emi/', views.submit_emi, name="submit_emi"),
    path('emi/', views.emi, name="emi"),
    path('get_otp/', views.get_otp, name="get_otp"),
    path('kyc/<int:id>', views.kyc, name="kyc"),
    path('check_otp/<int:otp>/<int:mobile_number>', views.check_otp, name="check_otp"),
    path('edit_enrollment/<int:id>', views.edit_enrollment, name="edit_enrollment"),
    path('edit_address/<int:id>', views.edit_address, name="edit_address"),
    path('edit_personal_information/<int:id>', views.edit_personal_information, name="edit_personal_information"),
    path('edit_reference_details/<int:id>', views.edit_reference_details, name="edit_reference_details"),
    path('edit_product_details/<int:id>', views.edit_product_details, name="edit_product_details"),
    path('edit_bank_details/<int:id>', views.edit_bank_details, name="edit_bank_details"),
    path('edit_emi_scheme/<int:id>', views.edit_emi_scheme, name="edit_emi_scheme "),
    path('edit_product_information/<int:id>', views.edit_product_information, name="edit_product_information"),
    path('create_enrollment/<int:mobile_number>', views.create_enrollment, name="create_enrollment"),
    path('address/<int:id>', views.address, name="address"),
    path('personal_information/<int:id>', views.personal_information, name="personal_information"),
    path('reference_details/<int:id>', views.reference_details, name="reference_details"),
    path('product_details/<int:id>', views.product_details, name="product_details"),
    path('bank_details/<int:id>', views.bank_details, name="bank_details"),
    path('emi_scheme/<int:id>', views.emi_scheme, name="emi_scheme"),
    path('product_information/<int:id>', views.product_information, name="product_information"),
    path('invoice/<int:id>', views.invoice, name="invoice"),
    path('preview_first/<int:id>', views.preview_first, name="preview_first"),
    #Asset Details
    #Surrogate Details
    path('enrollment_details/<int:id>', views.enrollment_details, name="enrollment_details"),
]
