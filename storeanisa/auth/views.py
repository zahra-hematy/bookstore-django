import email
from importlib.resources import path
from multiprocessing.sharedctypes import Value
from django.shortcuts import render,redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.contrib.auth import views as auth_view
from django.views import View
from auth.models import OTP
from django.contrib.auth import login
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.forms import UserCreationForm
from .forms import *
# Create your views here.

class LoginView(auth_view.LoginView):
    template_name = 'auth/registration/login.html'
    redirect_authenticated_user: True
    
    

class SignupView(View):
    def get(self, request):
        form = signupForm()
        return render(request,'auth/signup.html',{ 'form': form})


    def post(self, request):
        form = signupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            try:
                otp = OTP.objects.get(user=user)
            except OTP.DoesNotExist:
                otp = OTP(user=user)
                otp.save()
            otp.generate()
            otp.save()
            path = reverse('activate', otp = otp.value)
            domain =get_current_site(request).domain
            message = render_to_string('auth/activate_email.html',
                                       {
                                           'user' :request.user,
                                           'domain':domain,
                                           'otp':otp.value
                                       } )


            email = EmailMessage('Activation', message, to=[user.email])
            email.send()

            # login(request, user)
            return redirect(reverse('store:index'))
        return render(request,'auth/signup.html',{ 'form': form})


class ActivateView(View):
    def get(self, request, otp):
        try:
            otp = OTP.objects.get(Value=otp)
            if timezone.now() - otp.create_date  >timedelta(days=1):
                return render(request, 'auth/invalid_otp.html')
            user = otp.user
            otp.user.is_active = True
            otp.user.save()
            otp.delete()
            login(request, user)
            return redirect(reverse('store:index'))
        except OTP.DoesNotExist:
            return render(request, 'auth/invalid_otp.html')