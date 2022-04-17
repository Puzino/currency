from django.urls import path
from django.views.generic import TemplateView

from accounts import views  # noqa: I100

app_name = 'accounts'

urlpatterns = [
    path('my-profile/', views.MyProfile.as_view(), name='my_profile'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('activate/<uuid:username>/', views.ActivateUser.as_view(), name='activate_user'),
    path('activate-mail/', TemplateView.as_view(template_name="email_confirm.html"), name='email_confirm'),
    path('confirm/', TemplateView.as_view(template_name="confirm.html"), name='confirm'),

]
