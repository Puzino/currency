from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, RedirectView, UpdateView

from accounts.froms import SignUpForm  # noqa: I100
from accounts.models import User  # noqa: I100


class MyProfile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'my_profile.html'
    success_url = reverse_lazy('index')
    fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'phone',
        'avatar',
    )

    def get_object(self, queryset=None):
        return self.request.user


class SignUp(CreateView):
    queryset = User.objects.all()
    template_name = 'signup.html'
    success_url = reverse_lazy('accounts:email_confirm')
    form_class = SignUpForm


class ActivateUser(RedirectView):
    url = reverse_lazy('accounts:confirm')

    def get_redirect_url(self, username):
        user = get_object_or_404(User, username=username)
        if user.is_active:
            messages.error(self.request, 'Аккаунт активирован!.')
        else:
            user.is_active = True
            user.save(update_fields=['is_active', ])
        return super().get_redirect_url()
