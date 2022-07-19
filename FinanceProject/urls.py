from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('dealer_dashboard/', include('dealer.urls')),
    path('admin_dashboard/', include('admin.urls')),
    path('customer_dashboard/', include('customer.urls')),
    path('employee_dashboard/', include('employee.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
