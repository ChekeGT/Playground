from .forms import UserCreationFormWithEmail, EmailUpdateForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.models import User
from .models import Profile
# Create your views here.


class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail
    template_name = 'registration/signup.html'
    def get_success_url(self):
        return reverse_lazy('login') + '?registered'

    def get_form(self, form_class=None):
       form  =  super(SignUpView,self).get_form()
       form.fields['username'].widget = forms.TextInput(
           attrs={
               'class':'form-control mb-2',
               'placeholder':'Nombre de Usuario'
           }
       )
       form.fields['password1'].widget = forms.PasswordInput(
           attrs={
               'class':'form-control mb-2',
               'placeholder':'Introduce tu contraseña'
           }
       )
       form.fields['password2'].widget = forms.PasswordInput(
           attrs={
               'class':'form-control mb-3',
               'placeholder':'Introduce tu contraseña de nuevo'
           }
       )
       form.fields['email'].widget = forms.EmailInput(
           attrs={
               'class': 'form-control mb-2',
               'placeholder': 'Introduce tu email'
           }
       )
       return form

@method_decorator(login_required, name='dispatch')
class UpdateProfileView(UpdateView):
   template_name = 'registration/update_or_create_profile.html'
   fields = ['avatar','bio','page']
   model = Profile

   def get_success_url(self):
       return reverse_lazy('update_profile') + '?ok'

   def get_object(self,  queryset=None):
         profile, created = Profile.objects.get_or_create(user=self.request.user)
         return profile
   def get_form(self, form_class=None):
       form = super(UpdateProfileView, self).get_form()
       form.fields['bio'].widget = forms.Textarea(attrs={'class':'form-control mt-3 mb-3','placeholder':'Introduce una descripcion de ti, o tu biografia'})
       form.fields['page'].widget = forms.URLInput(attrs={'class':'form-control mb-3','placeholder':'Introduce la url a tu pagina web'})
       return form


@method_decorator(login_required, name='dispatch')
class UpdateEmailView(UpdateView):
    template_name = 'registration/update_email.html'
    model = User
    form_class = EmailUpdateForm
    def get_success_url(self):
        return  reverse_lazy('update_profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super(UpdateEmailView,self).get_form()
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control'})
        return form
