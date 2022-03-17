from currency import views as currency_views

from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', currency_views.hello_world),
    path('contact_us/list/', currency_views.contact_us_list),
    path('rate/list/', currency_views.rate_list),

]
