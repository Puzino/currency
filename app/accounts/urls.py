from django.urls import path

from accounts import views  # noqa: I100

app_name = 'accounts'

urlpatterns = [
    path('my-profile/', views.MyProfile.as_view(), name='my_profile'),

]
