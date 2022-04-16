from django.urls import path

from accounts import views  # noqa: I100

app_name = 'accounts'

urlpatterns = [
    path('my-profile/', views.MyProfile.as_view(), name='my_profile'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('activate/<uuid:username>/', views.ActivateUser.as_view(), name='activate_user'),

]
