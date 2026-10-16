from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, CustomUserEditForm

class SignUpView(generic.CreateView):
    form_class    = CustomUserCreationForm
    success_url   = reverse_lazy('login')
    template_name = 'useradmin/signup.html'

class ProfileView(LoginRequiredMixin, generic.UpdateView):
    form_class    = CustomUserEditForm
    template_name = 'useradmin/profile.html'
    success_url   = reverse_lazy('profile')

    def get_object(self):
        return self.request.user