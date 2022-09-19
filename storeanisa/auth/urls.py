from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import path, include
from httplib2 import Authentication
from store.views import hello_world
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/',include('store.urls', namespace='store')),
    path('auth/', include('django.contrib.auth.urls'))
]

app_name= 'anisaauth'
urlpatterns =[
    path('login/',views.LoginView.as_view(), {'template_name': 'registration/login.html'}, name='login'),
    path('signup/',views.SignupView.as_view(), name='signup'),
    path('activate/<str:otp>', views.ActivateView.as_view(), name='activate')
]