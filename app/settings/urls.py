from django.contrib import admin
from django.urls import path

from currency import views as currency_views  # noqa: I100

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', currency_views.hello_world),
    path('contact_us/list/', currency_views.contact_us_list),
    path('rate/list/', currency_views.rate_list),
    path('source/list/', currency_views.source_list),
    path('source/create/', currency_views.source_create),
    path('source/detail/<int:pk>/', currency_views.source_detail),
    path('source/delete/<int:pk>/', currency_views.source_delete),
    path('source/edit/<int:pk>/', currency_views.source_edit),
]
