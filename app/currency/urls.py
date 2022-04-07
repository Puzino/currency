from django.urls import path

from currency import views as currency_views  # noqa: I100

app_name = 'currency'

urlpatterns = [
    path('contact_us/list/', currency_views.ContactUsList.as_view(), name='contact_us_list'),
    path('rate/list/', currency_views.RateList.as_view(), name='rate_list'),
    path('source/list/', currency_views.SourceList.as_view(), name='source_list'),
    path('source/create/', currency_views.SourceCreate.as_view(), name='source_create'),
    path('source/edit/<int:pk>/', currency_views.SourceEdit.as_view(), name='source_edit'),
    path('source/detail/<int:pk>/', currency_views.SourceDetail.as_view(), name='source_detail'),
    path('source/delete/<int:pk>/', currency_views.SourceDelete.as_view(), name='source_delete'),

    path('contact-us/create/', currency_views.ContactUsCreateView.as_view(), name='contact_us_create')
]
